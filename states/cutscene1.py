from core.cutscene_base import CutsceneBase

class Cutscene1(CutsceneBase):
    def __init__(self, game):
        text = (
            "A vaca fazendeira recebeu uma visita dos ETs..."
            "Eles ouviram dizer que o leite produzido aqui é o melhor da Via Láctea!"
            "ETs: Gostaríamos de levar os leites produzidos aqui."
        )
        super().__init__(game, text, next_state="cutscene2")
