class Cobra:
    def __init__(self):
        self.corpo = [[100, 50], [90, 50], [80, 50]]
        self.direcao = 'DIREITA'
        self.crescer = False

    def muda_direcao(self, direcao):
        if direcao == 'DIREITA' and not self.direcao == 'ESQUERDA':
            self.direcao = 'DIREITA'
        if direcao == 'ESQUERDA' and not self.direcao == 'DIREITA':
            self.direcao = 'ESQUERDA'
        if direcao == 'CIMA' and not self.direcao == 'BAIXO':
            self.direcao = 'CIMA'
        if direcao == 'BAIXO' and not self.direcao == 'CIMA':
            self.direcao = 'BAIXO'

    def move(self, pos_comida):
        head = self.corpo[0][:]
        if self.direcao == 'DIREITA':
            head[0] += 10
        if self.direcao == 'ESQUERDA':
            head[0] -= 10
        if self.direcao == 'CIMA':
            head[1] -= 10
        if self.direcao == 'BAIXO':
            head[1] += 10

        if head == pos_comida:
            self.crescer = True
        else:
            self.corpo.pop()

        self.corpo.insert(0, head)

        if self.crescer:
            self.corpo.append(self.corpo[-1])
            self.crescer = False
            return True
        return False

    def colisao(self):
        head = self.corpo[0]
        if head in self.corpo[1:]:
            return True
        if head[0] >= 300 or head[0] < 0 or head[1] >= 400 or head[1] < 0:
            return True
        return False
