from kivy.graphics.texture import Texture
from kivy.app import App

import cv2
import numpy as np

from enums.ModoSelecionadoEnum import ModoSelecionado
from util.evento import Evento

class RotinaMonitoramento():
    eventos = []

    def __init__(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado
        self.pausado = False
        self.finalizado = False
        pass

    def selecionarModo(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado

    def iniciarRotina(self, modo_selecionado, tempo_digitado):
        self.pausado = False
        self.modo_selecionado = modo_selecionado
        pass

    def artefatoDetectado(self, horario_atual):
        self.incluirEvento(Evento("Artefato identificado", horario_atual))
        self.pausado = True

    def pausarRotina(self, horario_pausa):
        self.incluirEvento(Evento("Rotina pausada", horario_pausa))
        self.pausado = True

    def continuarRotina(self):
        self.pausado = False

    def encerrarRotina(self, horario_encerramento):
        self.incluirEvento(Evento("Fim da rotina", horario_encerramento))
        self.finalizado = True
        pass

    def incluirEvento(self, evento):
        self.eventos.append(evento)
        App.get_running_app().gerenciador.ids['tela_deteccao'].ids['scroll_view_eventos'].incluirEvento(evento)

    def criaImagem(self, altura, largura, bits=np.uint8, canais=3, cor=(0, 0, 0)): # (cv.GetSize(frame), 8, 3)
        """Create new image(numpy array) filled with certain color in RGB"""
        # Create black blank image
        if bits == 8:
            bits = np.uint8
        elif bits == 32:
            bits = np.float32
        elif bits == 64:
            bits = np.float64
        image = np.zeros((altura, largura, canais), bits)
        if cor != (0, 0, 0):
            # Fill image with color
            image[:] = cor
        return image

    def update(self, dt, camera):
        # display image from cam in opencv window
        frame = camera.read()
        aplicativo = App.get_running_app()

        buf1 = aplicativo.rotina_deteccao.obterLandmarks(frame)
        buf1 = cv2.flip(buf1, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        aplicativo.rotina_deteccao.obterCoordenadasOlhos()
        teve_fadiga = aplicativo.rotina_deteccao.detectarFadiga()

        if teve_fadiga:
            self.incluirEvento(Evento("Fadiga detectada", aplicativo.horario_atual))
            aplicativo.gerenciador.ids['tela_deteccao'].dialogAlertaFadiga()
            self.pausado = True

        # display image from the texture
        return texture
