class classeteste1():
    def __init__(self):
        self.variavel1 = "teste 1"

class classeteste2():
    def __init__(self):
        self.variavel2 = "teste 2"

def main():
    instancia_teste_1 = classeteste1()
    instancia_teste_2 = classeteste2()

    instancia_teste_1.variavel1 = instancia_teste_2.variavel2

    instancia_teste_2.variavel2 = "alterei o valor teste 2"
    pass

main()