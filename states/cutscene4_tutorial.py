from core.cutscene_base import CutsceneBase

class Cutscene4_Tutorial(CutsceneBase):
    def __init__(self, game):
        text = (
            "Vaca fazendeira: E quando eu tiver só sol (1) e sem vento (0)?"
            "ETs: Use a nave OR! Ela ajuda quando apenas uma das fontes tem energia."
            "Vaca fazendeira: E quando tiver sol E vento ao mesmo tempo?"
            "ETs: Então use a nave AND para combinar as forças!"
        )
        super().__init__(game, text, next_state="cutscene5_tutorial_pratico")
