from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.clock import Clock

import cv2
import numpy as np

from Interface import *
from rotinas.Alerta import RotinaAlerta
from rotinas.Deteccao import RotinaDeteccao
from rotinas.Monitoramento import RotinaMonitoramento
from rotinas.Relatorio import RotinaRelatorio
from enums.ModoSelecionadoEnum import ModoSelecionado

from datetime import datetime

Config.set('graphics', 'resizable', False)
rgba_divider = 255
#Builder.load_string(open("Aplicativo.kv", encoding='utf-8').read(), rulesonly=True)

class Aplicativo(App):
    tempo_execucao = StringProperty("00:00")
    horario_atual = StringProperty(datetime.now().strftime("%H:%M"))

    modo_selecionado = None
    rotina_alerta = RotinaAlerta()
    rotina_deteccao = RotinaDeteccao()
    rotina_monitoramento = RotinaMonitoramento(modo_selecionado)
    rotina_relatorio = RotinaRelatorio()
    
    def build(self):
        Window.size = (600, 600)
        Window.clearcolor = (208/rgba_divider,244/rgba_divider,234/rgba_divider,1)
        self.gerenciador = Gerenciador()

        # variaveis para o opencv e camera
        self.captura = cv2.VideoCapture(0)
        ret, frame = self.captura.read()
        self.camera = self.gerenciador.ids['tela_deteccao'].ids['camera']

        return self.gerenciador

    def iniciarRotinaMonitoramento(self, modo_selecionado):
        def callback_horario(dt): self.horario_atual = datetime.now().strftime("%H:%M")
        Clock.schedule_interval(callback_horario, 1)

        def callback_atualiza_camera(dt): self.camera.texture = self.rotina_monitoramento.update(dt, self.captura)
        Clock.schedule_interval(callback_atualiza_camera, 1.0/30.0)
        
        self.modo_selecionado = ModoSelecionado[modo_selecionado]
        self.gerenciador.current = "tela_deteccao"
        self.rotina_monitoramento.iniciarRotina(self.modo_selecionado, self.tempo_execucao)


Aplicativo().run()

