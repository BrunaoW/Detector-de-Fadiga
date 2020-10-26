from kivy.graphics.texture import Texture

import cv2
import numpy as np

from enums.ModoSelecionadoEnum import ModoSelecionado

class RotinaMonitoramento():
    def __init__(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado
        self.pausado = False
        pass

    def selecionarModo(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado

    def iniciarRotina(self, modo_selecionado, tempo_digitado):
        pass

    def pausarRotina(self):
        self.pausado = True

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
        ret, frame = camera.read()
        # cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        return texture
