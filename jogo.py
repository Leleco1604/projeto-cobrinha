import pygame
import sys
import time
import random
from moviepy.editor import VideoFileClip
from cobrinha import Cobra
from comida import Comida

# Função para reproduzir vídeo na tela inicial
def play_video(video_path, screen, start_button, button_text):
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=30, dtype="uint8"):
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(frame_surface, screen.get_size()), (0, 0))
        
        # Desenha o botão "Start" sobre o vídeo
        pygame.draw.rect(screen, (0, 128, 0), start_button)
        screen.blit(button_text, (start_button.x + 10, start_button.y + 10))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return True
    return False

# Função para mostrar a tela inicial
def show_start_screen(screen):
    start_button = pygame.Rect(100, 300, 100, 50)
    font = pygame.font.SysFont('Ubuntu', 30)
    button_text = font.render('Start', True, (255, 255, 255))

    # Reproduz o vídeo e desenha o botão "Start" em loop
    while True:
        if play_video('video_fundo.mp4', screen, start_button, button_text):
            return

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

# Função principal do jogo
def main():
    # Inicia o pygame
    pygame.init()
    TAM_TELA = (300, 400)
    tela = pygame.display.set_mode(TAM_TELA)

    # Carrega o fundo do jogo
    fundo = pygame.image.load("fundo.jpg")
    fundo = pygame.transform.scale(fundo, TAM_TELA)

    # Para colocar uma fonte
    pygame.font.init()
    minha_font = pygame.font.SysFont('Ubuntu', 20)

    # Cronômetro
    tempo = pygame.time.Clock()

    # Som de comer
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    def playNotificationSound():
        sound = pygame.mixer.Sound("som.ogg")
        sound.play()

    # Música de fundo
    pygame.mixer.music.load("TA VENDO AQUELA LUA - EXALTASAMBA.mid")
    pygame.mixer.music.play(-1)  # O parâmetro -1 faz a música tocar em loop

    cobra = Cobra()
    comida = Comida()
    posicao_comida = comida.posicao

    pontuacao = 0

    # Tela inicial
    show_start_screen(tela)

    # Para ficar atualizando a tela
    while True:
        # Desenha o fundo do jogo
        tela.blit(fundo, (0, 0))

        for event in pygame.event.get():
            # escuta - mouse ou teclado, for igual a sair
            if event.type == pygame.QUIT:
                # Interrompe o jogo
                pygame.quit()
                print('falou')
                # Fecha a janela
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    cobra.muda_direcao('DIREITA')
                if event.key == pygame.K_UP:
                    cobra.muda_direcao('CIMA')
                if event.key == pygame.K_DOWN:
                    cobra.muda_direcao('BAIXO')
                if event.key == pygame.K_LEFT:
                    cobra.muda_direcao('ESQUERDA')

        posicao_comida = comida.gera_nova_posicao()

        # Se a posição da cobra for igual à da comida
        if cobra.move(posicao_comida):
            comida.devorada = True
            playNotificationSound()
            pontuacao += 1

        # Verifica colisão
        if cobra.colisao():
            pontos = minha_font.render(f'Você perdeu! Pontos: {pontuacao}', True, (255, 255, 255))
            tela.blit(pontos, (50, 180))
            pygame.display.flip()
            time.sleep(1)
            pygame.quit()
            sys.exit()

        # Texto da pontuação
        pontos = minha_font.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        tela.blit(pontos, (10, 10))

        # Desenha a cobra na tela
        for pos in cobra.corpo:
            pygame.draw.rect(tela, pygame.Color(67, 145, 0),
                            pygame.Rect(pos[0], pos[1], 10, 10))

        # Desenha a comida na tela
        pygame.draw.rect(tela, pygame.Color(150, 200, 100),
                        pygame.Rect(posicao_comida[0], posicao_comida[1], 10, 10))

        # Atualiza a tela a cada frame
        pygame.display.update()

        # Define os frames do jogo
        tempo.tick(16)

if __name__ == "__main__":
    main()
