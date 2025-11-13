from core.cutscene_base import CutsceneBase

class Cutscene5_TutorialPratico(CutsceneBase):
    def __init__(self, game):
        text = (
            "ETs: Agora produza um copo de leite para testarmos!"
            "Vaca fazendeira: Mas está noite e sem vento!"
            "ETs: Para nossa sorte, a nave NOT está disponível!"
            "Ela transforma os 0s em 1 e gera energia."
            "Vaca fazendeira: Oba! Vamos testar!"
        )
        super().__init__(game, text, next_state="cutscene6_inicio_missoes")
