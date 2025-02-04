from kivy.properties import StringProperty
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.app import App

from imutils.video import VideoStream
import numpy as np
import cv2

from enums.ModoSelecionadoEnum import ModoSelecionado
from rotinas.Monitoramento import RotinaMonitoramento
from rotinas.Relatorio import RotinaRelatorio
from rotinas.Deteccao import RotinaDeteccao
from rotinas.Alerta import RotinaAlerta
from util.evento import Evento
from util.tempo import *
from Interface import *

import datetime

Config.set('graphics', 'resizable', False)
rgba_divider = 255

class Aplicativo(App):
    tempo_execucao_digitado = StringProperty("01:00")
    horario_atual = StringProperty(datetime.datetime.now().strftime("%H:%M"))
    tempo_execucao_corrente = StringProperty("00:00:00")

    modo_selecionado = None
    rotina_alerta = RotinaAlerta()
    rotina_deteccao = RotinaDeteccao()
    rotina_monitoramento = RotinaMonitoramento(modo_selecionado)
    rotina_relatorio = RotinaRelatorio()

    ja_gerou_relatorio = False
    
    def build(self):
        Window.size = (600, 600)
        Window.clearcolor = (208/rgba_divider,244/rgba_divider,234/rgba_divider,1)
        self.gerenciador = Gerenciador()

        # variaveis para o opencv e camera
        self.captura = VideoStream(src=0).start()
        self.camera = self.gerenciador.ids['tela_deteccao'].ids['camera']

        return self.gerenciador

    def iniciarRotinaMonitoramento(self, modo_selecionado):
        def callback_horario(dt): self.horario_atual = datetime.datetime.now().strftime("%H:%M")
        self.atualiza_horario = Callback(callback_horario, 1)
        self.atualiza_horario.start()

        self.tempo_execucao = Tempo.get_sec(self.tempo_execucao_digitado)
        def callback_atualiza_tempo_restante(dt):
            self.tempo_execucao = self.tempo_execucao - 1
            self.tempo_execucao_corrente = str(datetime.timedelta(seconds=self.tempo_execucao))
            if self.tempo_execucao == 0:
                self.encerrarRotina()
            return not (self.rotina_monitoramento.pausado or self.rotina_monitoramento.finalizado)
        self.atualiza_tempo_restante = Callback(callback_atualiza_tempo_restante, 1)
        self.atualiza_tempo_restante.start()
        
        def callback_atualiza_camera(dt): 
            self.camera.texture = self.rotina_monitoramento.update(dt, self.captura)
            return not (self.rotina_monitoramento.pausado or self.rotina_monitoramento.finalizado)
        self.atualiza_camera = Callback(callback_atualiza_camera, 1.0/30.0)
        self.atualiza_camera.start()

        self.modo_selecionado = ModoSelecionado[modo_selecionado]
        self.rotina_monitoramento.incluirEvento(Evento("Inicio da rotina", self.horario_atual))
        self.gerenciador.current = "tela_deteccao"
        self.rotina_monitoramento.iniciarRotina(self.modo_selecionado, self.tempo_execucao_digitado)

    def pausarRotina(self):
        self.rotina_monitoramento.pausarRotina(self.horario_atual)

    def continuarRotina(self):
        self.rotina_monitoramento.continuarRotina()
        self.atualiza_camera.start()
        self.atualiza_tempo_restante.start()

    def encerrarRotina(self):
        self.rotina_monitoramento.encerrarRotina(self.horario_atual)
        self.gerenciador.current = "tela_fim_execucao"
        pass

    def gerarRelatorio(self):
        if not self.ja_gerou_relatorio:
            gerou_corretamente = self.rotina_relatorio.gerarRelatorio(self.rotina_monitoramento.eventos)
        
        if gerou_corretamente:
            TelaFimExecucao().dialogGerouPdf('PDF foi gerado corretamente')
            self.ja_gerou_relatorio = True
        else:
            TelaFimExecucao().dialogGerouPdf('PDF gerado incorretamente. Tente novamente')

try:
    Aplicativo().run()
except:
    pass