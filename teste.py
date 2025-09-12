import pygame

pygame.init()

# --- Configurações da Tela ---
# Para pixel art, é comum trabalhar com uma resolução interna baixa
# e depois escalá-la para uma janela maior.
INTERNAL_WIDTH, INTERNAL_HEIGHT = 320, 180
SCALE_FACTOR = 4
WINDOW_WIDTH, WINDOW_HEIGHT = INTERNAL_WIDTH * SCALE_FACTOR, INTERNAL_HEIGHT * SCALE_FACTOR

# A tela que o jogador vê (janela final, escalada)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Posicionamento Pixel Perfect")

# A superfície interna onde desenhamos o jogo em sua resolução original
game_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))

clock = pygame.time.Clock()

# --- Elementos do Jogo ---
# Criando um "jogador" como um quadrado vermelho
player_image = pygame.Surface((16, 16))
player_image.fill((255, 0, 0)) # Cor vermelha

# 1. Posição LÓGICA usando floats para precisão
# Começa no centro da tela interna
player_pos_x = float(INTERNAL_WIDTH / 2)
player_pos_y = float(INTERNAL_HEIGHT / 2)

# 2. Posição de RENDERIZAÇÃO usando pygame.Rect
# O Rect será atualizado a cada frame com base na posição float
player_rect = player_image.get_rect(center=(round(player_pos_x), round(player_pos_y)))

player_speed = 100 # pixels por segundo

# --- Loop Principal ---
running = True
while running:
    # Delta time para movimento independente de frame rate
    dt = clock.tick(60) / 1000.0 # tempo em segundos desde o último frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Lógica de Movimento (usando floats) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos_x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        player_pos_x += player_speed * dt
    if keys[pygame.K_UP]:
        player_pos_y -= player_speed * dt
    if keys[pygame.K_DOWN]:
        player_pos_y += player_speed * dt

    # 3. ATUALIZAR o Rect (inteiro) a partir da posição (float) ANTES de desenhar
    # Usar round() pode dar uma sensação um pouco mais natural que int()
    player_rect.centerx = round(player_pos_x)
    player_rect.centery = round(player_pos_y)

    # --- Desenho (Renderização) ---
    # Limpa a superfície do jogo com uma cor de fundo
    game_surface.fill((20, 20, 80)) # Azul escuro

    # Desenha o jogador na sua posição "pixel perfect" no Rect
    game_surface.blit(player_image, player_rect)

    # 4. Escalar a superfície do jogo para a tela final
    # Isso preserva a aparência de pixel art, sem borrar
    scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))

    # Atualiza a tela para mostrar o que foi desenhado
    pygame.display.flip()

pygame.quit()