import re

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class Gerenciador(ScreenManager):
    def mudaTela(self, tela_selecionada):
        self.current = tela_selecionada

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ConfiguracaoRotina(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TelaDeteccao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dialogPausa(self, *args):
        conteudo = BoxLayout(orientation = 'vertical')
        dialog = Popup(title='Rotina pausada.', content=conteudo, size_hint=(None, None), size=(250,130), auto_dismiss=False)
        def fecharDialog(*largs, **kwargs):
            aplicativo = App.get_running_app()
            aplicativo.continuarRotina()
            dialog.dismiss()
        botao = Button(text='Voltar', on_release=fecharDialog)

        conteudo.add_widget(botao)
        dialog.open()

    def dialogAlerta(self, *args):
        conteudo = BoxLayout(orientation = 'vertical')
        aplicativo = App.get_running_app()

        dialog = Popup(title='Fadiga detectada', content=conteudo, size_hint=(None, None), size=(250,130), auto_dismiss=False)
        def fecharDialog(*largs, **kwargs):
            aplicativo.continuarRotina()
            dialog.dismiss()
        botao = Button(text='Ok', on_release=fecharDialog)

        conteudo.add_widget(botao)
        dialog.open()

class TelaFimExecucao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fecharPrograma(self):
        App.get_running_app().stop()

class FloatInput(TextInput):
    padrao_numeros = re.compile('[^0-9]')
    
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == "backspace":
            self.insert_text('0')

    def insert_text(self, substring, from_undo=False):
        padrao = self.padrao_numeros
        s = re.sub(padrao, '', substring)
        
        if len(s) > 0:
            self.text = self.text.replace(':', '')
            self.text = self.text[1:]
            self.text = self.text[:2] + ':' + self.text[2:]
        
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

    def on_text_validate():
        pass

class CustomLabel(Label):
    def __init__(self, **kwargs):
        self.color = (0, 0, 0, 1)
        super().__init__(**kwargs)
