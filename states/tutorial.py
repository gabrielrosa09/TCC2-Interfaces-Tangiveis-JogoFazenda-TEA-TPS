import pygame
from config import *

class TutorialState:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font("assets/fonts/vcr.ttf", 40)
        self.font_text = pygame.font.Font("assets/fonts/vcr.ttf", 30)

        self.lines = [
            "",
            "Olá, aventureiro(a)! Bem-vindo(a) ao nosso mundo.",
            "Para uma experiência mágica e acessível, você usará gestos com as mãos para controlar tudo.",
            "É simples, veja só!",
            "",
            "NA TELA INICIAL:",
            "INICIAR O JOGO: Mantenha o gesto [EU TE AMO] firme por 2 segundos.",
            "VER O TUTORIAL: Mantenha o gesto [PUNHO] firme por 2 segundos para rever estas instruções.",
            "SAIR DO JOGO: Mantenha o gesto [PAZ] firme por 2 segundos.",
            "",
            "DURANTE O JOGO (EM UMA FASE):",
            "VALIDAR SUA JOGADA: Faça o gesto de [MÃO ABERTA] e depois feche-a [PUNHO].",
            "REPETIR A NARRAÇÃO DA FASE: Levante o dedo indicador [INDICADOR] por 2 segundos.",
            "VOLTAR AO MENU INICIAL: Faça o gesto [PAZ] por 2 segundos.",
            "",
            "NO TUTORIAL OU EM QUALQUER OUTRO MENU:",
            "VOLTAR AO MENU INICIAL: O gesto [PAZ] por 2 segundos sempre te levará ao menu.",
            "",
            "DICA: Mantenha sua mão firme em frente à câmera para que o reconhecimento seja perfeito.",
            "Agora você está pronto(a) para começar!"
        ]

        self.line_height = 30
        self.start_y = 50

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.state_manager.set_state("menu")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(PRETO)

        # Título centralizado
        title_surface = self.font_title.render("COMO JOGAR", True, (255, 255, 0))
        screen.blit(title_surface, (LARGURA // 2 - title_surface.get_width() // 2, 10))

        # Texto centralizado
        y = self.start_y
        for line in self.lines:
            text_surface = self.font_text.render(line, True, (255, 255, 255))
            x = LARGURA // 2 - text_surface.get_width() // 2
            screen.blit(text_surface, (x, y))
            y += self.line_height
