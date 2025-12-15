from core.cutscene_base import CutsceneBase

class Cutscene5(CutsceneBase):
    def __init__(self, game):
        text = (
            "ET Líder: Ineficiente! Nós dominamos a Tecnologia. "
            "Talvez possamos corrigir sua falha primitiva. "
            "Explique: como funciona esse seu sistema de energia?"
        )
        super().__init__(
            game,
            text,
            next_state="fase1",
            background="assets/images/backgrounds/CenaFazenda.png"  # ajuste o caminho conforme seu projeto
        )
