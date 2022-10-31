import pygame
import os
import random
import time
import sys

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'pipe.png')), (104, 640))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')), (500, 800))
IMAGENS_PASSARO = [
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird1.png')), (68, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird2.png')), (68, 48)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird3.png')), (68, 48)),
]
IMAGEM_QUESTAO = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'Questao.png'))), (500, 800))
IMAGEM_TITULO = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'menu.png'))), (530, 830))
IMAGEM_TITULO.set_alpha(20)
IMAGEM_NOTA = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'nota.png'))), (500, 800))
IMAGEM_REPROVADO = pygame.transform.scale((pygame.image.load(os.path.join('imgs', 'reprovado.png'))), (530, 830))
IMAGEM_REPROVADO.set_alpha(20)

pygame.mixer.init()
pygame.mixer.music.load(os.path.join('sfx', 'bg_music.mp3'))
pygame.mixer.music.set_volume(0.25)


pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)
FONTE_QUESTAO = pygame.font.SysFont('arial', 30)
FONTE_TITULO = pygame.font.SysFont('playbill', 100)
FONTE_APROVADO = pygame.font.SysFont('onyx', 70)
FONTE_REPROVADO = pygame.font.SysFont('playbill', 70)
FONTE_ENUNCIADO = pygame.font.SysFont('arial', 20)

pygame.display.set_caption('NightMATH')
icon = pygame.image.load(os.path.join('imgs', 'nightMATH.png'))
pygame.display.set_icon(icon)

nota = 0
menu_break = True

questoes = {'Figura Geométrica que representa\ngraficamente uma função\ndo 1º grau é chamada de:': 'Reta',
            'Qual o valor do coeficiente b\nna função de 2º grau\nf(x) = x² - 5x + 25?': '-5',
            'Qual o nome da figura geométrica\nque representa o gráfico\nde uma função de 2º grau?': 'Parabola',
            'Qual função que seu gráfico\nnunca toca o eixo x\ndo plano cartesiano?': 'Exponencial',
            'Em uma função, quando o valor de y\naumenta toda vez que o valor x\ntambém aumenta,\nchamamos essa função de:': 'Crescente',
            'A representação gráfica\nde uma função\né feita no plano...': 'Cartesiano',
            'Qual letra representa o eixo\ndas abcissas no plano cartesiano?': 'X',
            'Qual letra representa o eixo\ndas ordenadas no plano cartesiano?': 'Y',
            'Qual o valor do coeficiente c\nna função\nf(x) = 2x² + 5x + 25?': '25',
            'A função f(x) = -2x + 6\né crescente ou decrescente?': 'Decrescente',
            'A concavidade da parabola\nda função f(x) = x² - 9\né voltada para cima ou para baixo?': 'Cima',
            'O zero da função\ntambém é chamado de?': 'Raiz',
            'Qual a função que\na representação gráfica nunca toca\no eixo y do plano cartesiano?': 'Logarítmica'
            }




class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
        pygame.mixer.init()
        jump_sound = pygame.mixer.Sound(os.path.join('sfx', 'jump.mp3'))
        jump_sound.set_volume(0.01)
        jump_sound.play()

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0


        # se o passaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        global nota
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            colidir_sfx = pygame.mixer.Sound(os.path.join('sfx', 'colidir.mp3'))
            colidir_sfx.set_volume(0.01)
            colidir_sfx.play()
            nota = 0
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def checar_resposta(n_questao, resposta):
    global nota
    questao = list(questoes.values())[n_questao]
    resposta_ajustado = str(resposta.strip().lower().title())
    if questao == resposta_ajustado:
        nota += 2


def desenhar_questao(tela):
    global nota
    pygame.mixer.music.set_volume(0.05)

    questoes_u = []
    question_sfx = pygame.mixer.Sound(os.path.join('sfx', 'question.mp3'))
    question_sfx.set_volume(0.25)
    question_sfx.play()
    base_font = pygame.font.Font(None, 28)
    text_user = ''
    tela = tela
    color = pygame.Color('lightskyblue3')
    while True:
        teste = []
        if len(teste) == len(questoes):
            questoes_u.clear()
            teste.clear()
        num = random.randint(0, len(questoes) - 1)
        if num in questoes_u:
            teste.append(num)
            pass
        else:
            break
    v = True
    while v:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_user = text_user[:-1]
                elif event.key == 126:
                    pass
                else:
                    text_user += event.unicode
                if event.key == pygame.K_RETURN:
                    question_sfx.stop()
                    pygame.mixer.music.set_volume(0.25)
                    v = False
        tela.blit(IMAGEM_QUESTAO, (0, -70))
        questao = list(questoes.keys())[num]
        pergunta = questao.splitlines()
        cont = 0
        for c in pergunta:
            texto = FONTE_QUESTAO.render(f"{c}", 1, (0, 0, 0))
            tela.blit(texto, (TELA_LARGURA // 7, TELA_ALTURA // 5 + cont * 30))
            cont += 1
        input_rect = pygame.Rect(TELA_LARGURA // 7 - 10, TELA_ALTURA // 5 + (cont + 1) * 30 - 10, 300, 32)
        pygame.draw.rect(tela, (0, 0, 0), input_rect, 2)
        text_surface = base_font.render(text_user, True, (0, 0, 0))
        tela.blit(text_surface, (TELA_LARGURA // 7, TELA_ALTURA // 5 + (cont + 1) * 30))
        pygame.display.update()
    questoes_u.append(num)
    checar_resposta(n_questao=num, resposta=text_user)


def menu(tela):
    global menu_break
    tela = tela
    menu_paused = True
    sound_menu = pygame.mixer.Sound(os.path.join('sfx', 'menu.mp3'))
    sound_menu.set_volume(0.03)
    sound_menu.play()
    while menu_paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound_menu.stop()
                    pygame.mixer.music.play(-1)
                    menu_break = False
                    menu_paused = False
            if event.type == pygame.QUIT:
                menu_paused = False
                pygame.quit()
                sys.exit()
        tela.fill((0, 0, 0))
        tela.blit(IMAGEM_TITULO, (-10, -10))
        texto = FONTE_ENUNCIADO.render(f"E.E. Profº Idalina Ladeira apresenta...", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA / 4, 10))
        texto = FONTE_TITULO.render(f"NightMATH", 1, (201, 0, 0))
        tela.blit(texto, (TELA_LARGURA / 4, TELA_ALTURA // 5))
        border_rect = pygame.Rect(0, 0, TELA_LARGURA, TELA_ALTURA)
        pygame.draw.rect(tela, (201, 0, 0), border_rect, 2)
        texto = FONTE_QUESTAO.render(f"Press space", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA / 2.70, TELA_ALTURA // 5 + 10 * 30))
        pygame.display.update()


def nota_final(tela, nota):
    tela = tela
    nota = nota
    pygame.mixer.music.stop()
    v = True
    while v:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    v = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                v = False
        tela.fill((0, 0, 0))
        if nota >= 8:
            victory = pygame.mixer.Sound(os.path.join('sfx', 'victory.mp3'))
            victory.play()
            tela.blit(IMAGEM_NOTA, (0, 0))
            texto1 = FONTE_APROVADO.render(f"Aprovado", 1, (43, 186, 11))
            texto2 = FONTE_APROVADO.render(f"Sua nota foi de {nota}", 1, (43, 186, 11))

        else:
            loose = pygame.mixer.Sound(os.path.join('sfx', 'Loose.mp3'))
            loose.play()

            tela.fill((0, 0, 0))
            tela.blit(IMAGEM_REPROVADO, (0, 0))

            texto1 = FONTE_REPROVADO.render(f"Reprovado", 1, (201, 0, 0))
            texto2 = FONTE_REPROVADO.render(f"sua nota foi de {nota}", 1, (201, 0, 0))
        tela.blit(texto1, (TELA_LARGURA / 4 , TELA_ALTURA // 5))
        tela.blit(texto2, (TELA_LARGURA / 4, TELA_ALTURA // 5 + 80))

        pygame.display.update()
        time.sleep(4)
        v = False


def main(pontos=0):
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = pontos
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        if pontos == 26:
            nota_final(tela, nota)
            time.sleep(4)
            pontos += 1
            pygame.mixer.music.play()
            main()

        relogio.tick(30)
        if menu_break:
            menu(tela=tela)
        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if len(passaros) == 0:
                        while True:
                            time.sleep(1)
                            for evento in pygame.event.get():
                                if evento.type == pygame.KEYDOWN:
                                    if evento.key == pygame.K_SPACE:
                                        main()
                                    if evento.key == pygame.K_ESCAPE:
                                        rodando = False
                                        pygame.quit()
                                        sys.exit()
                                if evento.type == pygame.QUIT:
                                    rodando = False
                                    pygame.quit()
                                    sys.exit()
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)
        for i, passaro in enumerate(passaros):
            if pontos % 5 == 0 and pontos != 0:
                passaros.pop(i)
                if len(passaros) == 0:
                    while True:
                        time.sleep(1)
                        for evento in pygame.event.get():
                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_SPACE:
                                    desenhar_questao(tela=tela)
                                    main(pontos=pontos + 1)
                                if evento.key == pygame.K_ESCAPE:
                                    rodando = False
                                    pygame.quit()
                                    sys.exit()
                            if evento.type == pygame.QUIT:
                                rodando = False
                                pygame.quit()
                                sys.exit()
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if len(passaros) == 0:
                    while True:
                        time.sleep(1)
                        for evento in pygame.event.get():
                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_SPACE:
                                    main()
                                if evento.key == pygame.K_ESCAPE:
                                    rodando = False
                                    pygame.quit()
                                    sys.exit()
                            if evento.type == pygame.QUIT:
                                rodando = False
                                pygame.quit()
                                sys.exit()
        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()