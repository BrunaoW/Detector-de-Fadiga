from reportlab.pdfgen import canvas

from datetime import datetime

class RotinaRelatorio():
    def __init__(self):
        pass

    def gerarRelatorio(self, eventos):
        dia_atual = datetime.now()
        nome_relatorio = dia_atual.strftime("%d_%m_%Y %H_%M")
        relatorio = canvas.Canvas('{}.pdf'.format(nome_relatorio))
        posicao_vertical_lista_eventos = 720
        posicao_horizontal_lista_eventos = 50

        for evento in eventos:
            posicao_vertical_lista_eventos -= 20
            relatorio.drawString(posicao_horizontal_lista_eventos, posicao_vertical_lista_eventos, '{} - {}'.format(evento.hora, evento.texto))

        relatorio.setTitle(nome_relatorio)
        relatorio.setFont("Helvetica-Bold", 16)
        relatorio.drawString(posicao_horizontal_lista_eventos,750, 'Rotina de detecção de fadiga: {}'.format(dia_atual.strftime("%d/%m/%Y, %H:%M")))
        relatorio.save()
        return True
        