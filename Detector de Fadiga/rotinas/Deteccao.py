from scipy.spatial import distance as dist
import dlib
import cv2
from imutils import face_utils

class RotinaDeteccao():
    EYE_AR_THRESH = 0.27
    EYE_AR_CONSEC_FRAMES = 45
    COUNTER = 0

    (inicio_esquerdo, fim_esquerdo) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (inicio_direito, fim_direito) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    razao_media_calculada = float('inf')

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.pausado = False
        pass
    
    def detectarFadiga(self):
        if self.razao_media_calculada < self.EYE_AR_THRESH:
            self.COUNTER += 1
            
            if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                self.COUNTER = 0
                return True
        else:
            self.COUNTER = 0
            return False

    def obterLandmarks(self, imagem_camera):
        imagem_em_cinza = cv2.cvtColor(imagem_camera, cv2.COLOR_BGR2GRAY)
        rects = self.detector(imagem_em_cinza, 0)

        for rect in rects:
            self.landmarks = self.predictor(imagem_em_cinza, rect)
            self.landmarks = face_utils.shape_to_np(self.landmarks)

            for (x, y) in self.landmarks:
                cv2.circle(imagem_camera, (x, y), 1, (0, 0, 255), -1)

        return imagem_camera
    
    def obterCoordenadasOlhos(self):
        self.olho_esquerdo = self.landmarks[self.inicio_esquerdo:self.fim_esquerdo]
        self.olho_direito = self.landmarks[self.inicio_direito:self.fim_direito]
        razao_palpebra_esquerda = self.calcularRazaoPalpebra(self.olho_esquerdo)
        razao_palpebra_direita = self.calcularRazaoPalpebra(self.olho_direito)

        self.razao_media_calculada = (razao_palpebra_direita + razao_palpebra_esquerda) / 2

        
    def calcularRazaoPalpebra(self, posicao_landmark_olhos):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(posicao_landmark_olhos[1], posicao_landmark_olhos[5])
        B = dist.euclidean(posicao_landmark_olhos[2], posicao_landmark_olhos[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(posicao_landmark_olhos[0], posicao_landmark_olhos[3])

        # compute the eye aspect ratio
        razao_aspecto_olho = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return razao_aspecto_olho

    def selecionarModo(self, modo_selecionado):
        self.modo_selecionado = modo_selecionado