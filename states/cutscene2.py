from core.cutscene_base import CutsceneBase

class Cutscene2(CutsceneBase):
    def __init__(self, game):
        text = (
            "Vaca fazendeira: Infelizmente não posso atender o pedido... A fazenda está sem energia para fazer o ingrediente secreto do leite! Desde que mudei para energia sustentável, algo está faltando."
            "ETs: Talvez possamos ajudar com o poder da tecnologia!"
        )
        super().__init__(game, text, next_state="cutscene3")
