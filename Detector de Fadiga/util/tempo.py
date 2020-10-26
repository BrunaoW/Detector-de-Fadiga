from kivy.clock import Clock

class Tempo():

    def get_sec(time_str):
        h, m = time_str.split(':')
        return int(h) * 3600 + int(m) * 60

class Callback():
    def __init__(self, callback, intervalo):
        self.callback = callback
        self.intervalo = intervalo

    def start(self):
        Clock.schedule_interval(self.callback, self.intervalo)