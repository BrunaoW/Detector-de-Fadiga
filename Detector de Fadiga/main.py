from kivy.app import App
from Interface import Gerenciador
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.config import Config

Config.set('graphics', 'resizable', False)
rgba_divider = 255

class Aplicativo(App):
    def build(self):
        Window.size = (600, 600)
        Window.clearcolor = (208/rgba_divider,244/rgba_divider,234/rgba_divider,1)
        Builder.load_string(open("Aplicativo.kv", encoding='utf-8').read(), rulesonly=True)
        return Gerenciador()

Aplicativo().run()