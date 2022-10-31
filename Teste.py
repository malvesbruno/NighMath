import pygame
import time
import random

TELA_LARGURA = 500
TELA_ALTURA = 800
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 30)


help(pygame.mixer.init())

questoes = {'Figura Geométrica que representa\ngraficamente uma função\ndo 1º grau é chamada de:': 'Reta',
            'Qual o valor do coeficiente b\nna função de 2º grau\nf(x) = x² - 5x + 25?': '-5',
            'A parábola é a figura geométrica\nde qual função?': 'Função do 2º Grau',
            'Qual função que seu gráfico\nnunca toca o eixo x\ndo plano cartesiano?': 'Função Exponencial',
            'Em uma função, quando o valor de y\naumenta toda vez que o valor x\ntambém aumenta,\nchamamos essa função de:': 'Crescente'}


while True:
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    tela.fill((52, 78, 91))
    num = random.randint(0, len(questoes) - 1)
    questao = list(questoes.keys())[num]
    pergunta = questao.splitlines()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            pygame.quit()
            quit()
            break
    cont = 0
    for c in pergunta:
        print(f'{c}\n')
        texto = FONTE_PONTOS.render(f"{c}", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA//8, TELA_ALTURA//5 + cont*30))
        pygame.display.update()
        cont += 1
    time.sleep(200)


