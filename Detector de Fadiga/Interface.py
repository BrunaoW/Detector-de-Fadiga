
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

class Gerenciador(ScreenManager):
    def mudaTela(self, tela_selecionada):
        self.current = tela_selecionada

class TelaInicial(Screen):
    pass

class ConfiguracaoRotina(Screen):
    pass

class TelaDeteccao(Screen):
    pass

class TelaFimExecucao(Screen):
    pass
