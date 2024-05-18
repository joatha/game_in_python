import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações de tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Tabuleiro de RPG")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA_CLARO = (200, 200, 200)

# Configurações do tabuleiro
tamanho_celula = 40
linhas = altura // tamanho_celula
colunas = largura // tamanho_celula

# Fonte para o score e mensagens
fonte_score = pygame.font.SysFont(None, 36)
fonte_game_over = pygame.font.SysFont(None, 72)
fonte_msg = pygame.font.SysFont(None, 36)

# Função para desenhar o tabuleiro
def desenhar_tabuleiro():
    for linha in range(linhas):
        for coluna in range(colunas):
            x = coluna * tamanho_celula
            y = linha * tamanho_celula
            pygame.draw.rect(tela, CINZA_CLARO, (x, y, tamanho_celula, tamanho_celula), 1)

# Função para carregar e redimensionar uma imagem
def carregar_imagem(caminho, tamanho):
    imagem = pygame.image.load(caminho)
    imagem = pygame.transform.scale(imagem, tamanho)
    return imagem

# Função para desenhar uma imagem no tabuleiro
def desenhar_imagem(linha, coluna, imagem):
    x = coluna * tamanho_celula
    y = linha * tamanho_celula
    tela.blit(imagem, (x, y))

# Função para mover o perseguidor em direção ao jogador
def mover_perseguidor(pos_perseguidor, pos_jogador):
    linha_perseguidor, coluna_perseguidor = pos_perseguidor
    linha_jogador, coluna_jogador = pos_jogador

    if linha_perseguidor < linha_jogador:
        linha_perseguidor += 1
    elif linha_perseguidor > linha_jogador:
        linha_perseguidor -= 1

    if coluna_perseguidor < coluna_jogador:
        coluna_perseguidor += 1
    elif coluna_perseguidor > coluna_jogador:
        coluna_perseguidor -= 1

    return (linha_perseguidor, coluna_perseguidor)

# Função para mostrar a mensagem de game over e reiniciar ou sair do jogo
def game_over(score):
    tela.fill(BRANCO)
    texto_game_over = fonte_game_over.render("Game Over", True, PRETO)
    texto_score = fonte_score.render(f"Pontuação Final: {score}", True, PRETO)
    texto_restart = fonte_msg.render("Pressione R para Reiniciar ou Q para Sair", True, PRETO)
    tela.blit(texto_game_over, (largura // 2 - texto_game_over.get_width() // 2, altura // 3))
    tela.blit(texto_score, (largura // 2 - texto_score.get_width() // 2, altura // 2))
    tela.blit(texto_restart, (largura // 2 - texto_restart.get_width() // 2, altura // 1.5))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    main()
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Função principal
def main():
    executando = True
    relogio = pygame.time.Clock()
    score = 0

    # Carregar e redimensionar imagens
    jogador_img = carregar_imagem("jogador.jpg", (tamanho_celula, tamanho_celula))
    perseguidor_img = carregar_imagem("perseguidor.jpg", (tamanho_celula, tamanho_celula))

    # Posição inicial do jogador e do perseguidor
    posicao_jogador = (5, 5)
    posicao_perseguidor = (0, 0)

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False

                # Movimento do jogador com setas do teclado
                linha, coluna = posicao_jogador
                if evento.key == pygame.K_UP and linha > 0:
                    posicao_jogador = (linha - 1, coluna)
                elif evento.key == pygame.K_DOWN and linha < linhas - 1:
                    posicao_jogador = (linha + 1, coluna)
                elif evento.key == pygame.K_LEFT and coluna > 0:
                    posicao_jogador = (linha, coluna - 1)
                elif evento.key == pygame.K_RIGHT and coluna < colunas - 1:
                    posicao_jogador = (linha, coluna + 1)

            # Movimento do jogador com cliques do mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique com o botão esquerdo do mouse
                    x, y = evento.pos
                    coluna = x // tamanho_celula
                    linha = y // tamanho_celula
                    if linha < linhas and coluna < colunas:
                        posicao_jogador = (linha, coluna)

        # Movendo o perseguidor em direção ao jogador
        posicao_perseguidor = mover_perseguidor(posicao_perseguidor, posicao_jogador)

        # Preenchendo a tela com branco
        tela.fill(BRANCO)

        # Desenhando o tabuleiro
        desenhar_tabuleiro()

        # Desenhando o jogador e o perseguidor
        desenhar_imagem(posicao_jogador[0], posicao_jogador[1], jogador_img)
        desenhar_imagem(posicao_perseguidor[0], posicao_perseguidor[1], perseguidor_img)

        # Desenhando o score
        texto_score = fonte_score.render(f"Score: {score}", True, PRETO)
        tela.blit(texto_score, (10, 10))

        # Verificando colisão entre perseguidor e jogador
        if posicao_jogador == posicao_perseguidor:
            game_over(score)
            executando = False

        # Atualizando a tela
        pygame.display.flip()
        relogio.tick(10)
        score += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
