from core.cutscene_base import CutsceneBase

class Cutscene3(CutsceneBase):
    def __init__(self, game):
        text = (
            "Vaca Fazendeira: Muuu... Sinto muito. A produção está totalmente parada. "
            "Sem energia, as máquinas da Fábrica não ligam..."
        )
        super().__init__(
            game,
            text,
            next_state="cutscene4",
            background="assets/images/backgrounds/CenaNave.png"  # ajuste o caminho conforme seu projeto
        )
