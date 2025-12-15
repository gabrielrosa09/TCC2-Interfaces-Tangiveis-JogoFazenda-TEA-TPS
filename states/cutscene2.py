from core.cutscene_base import CutsceneBase

class Cutscene2(CutsceneBase):
    def __init__(self, game):
        text = (
            "ET Líder: Saudações, ser bovino. Os rumores viajaram anos-luz até nós. "
            "Viemos coletar o lendário Melhor Leite da Via Láctea imediatamente."
        )
        super().__init__(
            game,
            text,
            next_state="cutscene3",
            background="assets/images/backgrounds/CenaNave.png"
        )
