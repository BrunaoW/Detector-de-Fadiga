import re

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.textinput import TextInput

from Interface import *
from rotinas.Alerta import RotinaAlerta
from rotinas.Deteccao import RotinaDeteccao
from rotinas.Monitoramento import RotinaMonitoramento
from rotinas.Relatorio import RotinaRelatorio
from enums.ModoSelecionadoEnum import ModoSelecionado

Config.set('graphics', 'resizable', False)
rgba_divider = 255
#Builder.load_string(open("Aplicativo.kv", encoding='utf-8').read(), rulesonly=True)

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class Aplicativo(App):
    def build(self):
        self.modo_selecionado = None

        self.rotina_alerta = RotinaAlerta()
        self.rotina_deteccao = RotinaDeteccao()
        self.rotina_monitoramento = RotinaMonitoramento(self.modo_selecionado)
        self.rotina_relatorio = RotinaRelatorio()

        Window.size = (600, 600)
        Window.clearcolor = (208/rgba_divider,244/rgba_divider,234/rgba_divider,1)
        self.gerenciador = Gerenciador()

        return self.gerenciador

    def iniciarRotinaMonitoramento(modo_selecionado):
        self.modo_selecionado = ModoSelecionado.VIGIA if modo_selecionado == "VIGIA" else ModoSelecionado.VIAGEM
        self.gerenciador.current = "tela_deteccao"

        self.rotina_monitoramento.iniciarRotina(self.modo_selecionado)

Aplicativo().run()

