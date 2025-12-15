from core.cutscene_base import CutsceneBase

class Cutscene4(CutsceneBase):
    def __init__(self, game):
        text = (
            "Vaca Fazendeira: Tentei modernizar a fazenda com Energia Sustentável, mas o sistema pifou. "
            "A energia existe, mas não chega onde devia. Ainda falta algo para conectar tudo..."
        )
        super().__init__(
            game,
            text,
            next_state="cutscene5",
            background="assets/images/backgrounds/CenaFazenda.png"  # ajuste o caminho conforme seu projeto
        )
