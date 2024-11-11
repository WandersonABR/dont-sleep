# Monitoramento de Olhos com Alerta de Áudio

Este projeto utiliza a câmera para monitorar os olhos de uma pessoa em tempo real e detecta quando os olhos estão fechados por mais de 2 segundos. Quando isso acontece, um áudio de alerta é tocado. Além disso, uma imagem de alerta é exibida na tela quando os olhos estão fechados. O sistema também interrompe o áudio quando os olhos são reabertos.

## Funcionalidades

- **Detecção de olhos fechados**: Usando a razão de aspecto dos olhos (EAR), o código detecta se os olhos estão fechados por mais de 2 segundos.
- **Áudio de alerta**: Quando os olhos estão fechados por mais de 2 segundos, um áudio é reproduzido. O áudio é interrompido automaticamente quando os olhos são reabertos.
- **Imagem de aviso**: Uma imagem personalizada é exibida sobre a tela quando os olhos estão fechados.
- **Desenho de pontos faciais**: A malha de pontos faciais (FaceMesh) é desenhada sobre a face detectada para ilustrar os pontos-chave da face.

## Requisitos

- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- Pygame

## Instalação

1. **Clone este repositório**:
   ```bash
   git clone https://github.com/seu-usuario/monitoramento-olhos.git
   cd monitoramento-olhos
   ```

2. **Instale as dependências**:
   Você pode instalar as dependências necessárias utilizando `pip`. Execute o seguinte comando:
   ```bash
   pip install opencv-python mediapipe numpy pygame
   ```

3. **Configuração do áudio**:
   O projeto está configurado para tocar um áudio localizado no caminho:
   ```
   "C:/Users/User/Desktop/camera-senai/dont-sleep/audios/batwave.mp3"
   ```
   Substitua esse caminho pelo local correto do arquivo de áudio em seu sistema.

4. **Configuração da imagem de alerta**:
   O projeto utiliza uma imagem de alerta codificada em base64. Você pode substituir a string `imagem_aviso_base64` com sua própria imagem codificada, ou modificar o código para carregar uma imagem diretamente do sistema de arquivos.

## Como Usar

1. **Execute o script**:
   Após configurar o áudio e a imagem, você pode iniciar o monitoramento executando o script Python:
   ```bash
   python monitoramento_olhos.py
   ```

2. **Interação**:
   - O programa inicia a captura da câmera e começa a processar os frames em tempo real.
   - Quando os olhos ficam fechados por mais de 2 segundos, o áudio de alerta será reproduzido.
   - A imagem de alerta será exibida na tela quando os olhos estiverem fechados.
   - O áudio é interrompido automaticamente quando os olhos se abrem por mais de 2 segundos.

3. **Finalizar**:
   - Para finalizar o programa, pressione a tecla 'c' na janela da câmera.

## Como Funciona

### Detecção dos Olhos

O código utiliza o **MediaPipe Face Mesh**, uma ferramenta avançada para detectar e rastrear pontos faciais. Ele calcula a **Razão de Aspecto dos Olhos (EAR)** para determinar se os olhos estão abertos ou fechados. O EAR é uma métrica que descreve a razão entre a largura e a altura dos olhos.

### Áudio de Alerta

Quando os olhos ficam fechados por mais de 2 segundos (determinado pela medição do EAR), o programa inicia a reprodução de um áudio. O áudio é interrompido automaticamente se os olhos se abrirem novamente.

### Imagem de Alerta

Uma imagem de alerta é exibida na tela quando os olhos estão fechados por um período de tempo contínuo. Esta imagem pode ser personalizada substituindo a string base64 ou alterando o código para carregar uma imagem local.

## Exemplo de Uso

![Exemplo de Uso](imagens/exemplo.jpg) *(Imagem ilustrativa)*

## Contribuições

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Para contribuir, basta fazer um fork deste repositório, criar uma nova branch, implementar suas modificações e enviar um pull request.

## Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.


