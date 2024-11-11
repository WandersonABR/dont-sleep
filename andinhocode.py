import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
import base64
from conversorImage import imagem_aviso_base64


# Inicializa o sistema de áudio do Pygame.
pygame.mixer.init()

# Audios
audio_files = [
    "C:/wandersonDOA/dont-sleep/audios/batwave.mp3"
]

# Pontos dos olhos
p_olho_esq = [385, 380, 387, 373, 362, 263]
p_olho_dir = [160, 144, 158, 153, 33, 133]
p_olhos = p_olho_esq + p_olho_dir

# Função EAR(Eye Aspect Ratio)
def calculo_ear(face, p_olho_dir, p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq, :]
        face_dir = face[p_olho_dir, :]

        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * (np.linalg.norm(face_esq[4] - face_esq[5])))

        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * (np.linalg.norm(face_dir[4] - face_dir[5])))

    except:
        ear_esq = 0.0
        ear_dir = 0.0
    
    media_ear = (ear_esq + ear_dir) / 2
    return media_ear

# Limiares
ear_limiar = 0.27

# Inicializa a câmera
cap = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


# Decodificando a string base64 e convertendo para uma imagem OpenCV
imagem_aviso_bytes = base64.b64decode(imagem_aviso_base64)
imagem_aviso_array = np.frombuffer(imagem_aviso_bytes, np.uint8)
imagem_aviso = cv2.imdecode(imagem_aviso_array, cv2.IMREAD_COLOR)
imagem_aviso = cv2.resize(imagem_aviso, (300, 150))  # Redimensiona a imagem

# Estado do som
som_tocando = False
audio_olhos_fechados = False
tempo_olhos_fechados = 0
tempo_olhos_abertos = 0

# Inicializa o FaceMesh
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print('Ignorando o frame vazio da câmera.')
            continue
        
        comprimento, largura, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame_rgb)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        

        # Desenho e detecção de olhos
        if saida_facemesh.multi_face_landmarks:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame_bgr,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1)
                )
                
                face = face_landmarks.landmark
                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                        cv2.circle(frame_bgr, coord_cv, 2, (255, 0, 0), -1)

                # Chamada do EAR
                ear = calculo_ear(face, p_olho_dir, p_olho_esq)

                # Definir estado do olho
                estado_olho = "Aberto" if ear >= ear_limiar else "Fechado"

                # Detecção de olhos fechados por mais de 2 segundos
                if ear < ear_limiar:
                    if not audio_olhos_fechados:
                        tempo_olhos_fechados = time.time()
                        audio_olhos_fechados = True
                    elif time.time() - tempo_olhos_fechados >= 2:
                        if not som_tocando:
                            pygame.mixer.music.load(audio_files[0])
                            pygame.mixer.music.play()
                            som_tocando = True
                else:
                    audio_olhos_fechados = False
                    if som_tocando:
                        # Inicia o temporizador de olhos abertos
                        if tempo_olhos_abertos == 0:
                            tempo_olhos_abertos = time.time()
                        elif time.time() - tempo_olhos_abertos >= 2:
                            pygame.mixer.music.stop()
                            som_tocando = False
                    else:
                        # Reseta o temporizador quando os olhos estão fechados novamente
                        tempo_olhos_abertos = 0

                # Exibição do valor EAR e estado do olho
                #cv2.rectangle(frame_bgr, (0, 1), (350, 80), (58, 58, 55), -1)
                cv2.putText(frame_bgr, f"EAR: {round(ear, 2)}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                cv2.putText(frame_bgr, f"Olho: {estado_olho}", (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                
                if estado_olho == "Fechado":
                    # Define a posição onde a imagem será exibida
                    x_offset, y_offset = 10, 100
                    frame_bgr[y_offset:y_offset+imagem_aviso.shape[0], x_offset:x_offset+imagem_aviso.shape[1]] = imagem_aviso


        cv2.imshow('Camera', frame_bgr)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break

cap.release()
cv2.destroyAllWindows()
