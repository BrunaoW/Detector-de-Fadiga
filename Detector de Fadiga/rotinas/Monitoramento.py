from enums.ModoSelecionadoEnum import ModoSelecionado

class RotinaMonitoramento():
    def __init__(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado
        self.pausado = False
        pass

    def selecionarModo(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado

    def iniciarRotina(self, modo_selecionado):
        pass
