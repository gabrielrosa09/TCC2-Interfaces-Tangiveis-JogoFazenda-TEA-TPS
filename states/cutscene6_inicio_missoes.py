from core.cutscene_base import CutsceneBase

class Cutscene6_InicioMissoes(CutsceneBase):
    def __init__(self, game):
        text = (
            "ETs: Este é o melhor leite da Via Láctea!"
            "Vaca fazendeira: Para uma produção maior, precisarei da ajuda de vocês."
            "ETs: Claro! Mas nem todas as naves estarão disponíveis o tempo todo."
            "Use a nave certa conforme as condições do dia."
            "Início das missões!"
        )
        super().__init__(game, text, next_state="fase1")
