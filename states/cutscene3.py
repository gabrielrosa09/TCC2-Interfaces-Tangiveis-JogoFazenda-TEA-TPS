from core.cutscene_base import CutsceneBase

class Cutscene3(CutsceneBase):
    def __init__(self, game):
        text = (
            "Vaca fazendeira: Temos duas fontes de energia: vento e sol."
            "Quando há vento, temos energia eólica (1). Quando há sol, energia solar (1)."
            "Mas quando é noite e não venta, ambas são 0 e nada funciona!"
            "ETs: Podemos usar a nave NOT para transformar 0 em 1!"
        )
        super().__init__(game, text, next_state="cutscene4_tutorial")
