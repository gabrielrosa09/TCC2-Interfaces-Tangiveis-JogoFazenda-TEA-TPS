from core.cutscene_base import CutsceneBase

class Cutscene1(CutsceneBase):
    def __init__(self, game):
        text = (
            "A fama do Melhor Leite da Via Láctea atravessou o cosmos! "
            "Hoje, a Vaca Fazendeira recebeu visitas de outro mundo... "
            "Os ETs pousaram no pasto e querem conferir a lenda de perto..."
        )
        super().__init__(game, text, next_state="fase1")
