
import pygame
import random
import math

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


LARGURA = 1000
ALTURA = 700

QUANTIDADE_PARTICULAS = 500

# Aceleracao gravitacional no eixo Y
GRAVIDADE = -9.8

# Coordenadas do emissor
EMISSOR_X = 0.0
EMISSOR_Y = 0.0
EMISSOR_Z = 0.0


class Particula:

    def __init__(self):
        # Inicializa a particula.
        self.reiniciar()

        # Distribui as idades iniciais para evitar que
        # todas as particulas aparecam simultaneamente.
        idade_inicial = random.uniform(0, self.vida)

        self.atualizar_posicao_inicial(idade_inicial)


    def reiniciar(self):
        # Posicao inicial da particula.
        self.x = EMISSOR_X
        self.y = EMISSOR_Y
        self.z = EMISSOR_Z

        # Pequena variacao na origem de emissao.
        self.x += random.uniform(-0.15, 0.15)
        self.z += random.uniform(-0.15, 0.15)

        self.origem_x = self.x
        self.origem_y = self.y
        self.origem_z = self.z

        # Velocidade inicial aleatoria
        self.vx_inicial = random.uniform(-2.5, 2.5)
        self.vy_inicial = random.uniform(5.0, 9.0)
        self.vz_inicial = random.uniform(-2.5, 2.5)

        # Velocidades atuais
        self.vx = self.vx_inicial
        self.vy = self.vy_inicial
        self.vz = self.vz_inicial

        # Aceleracao
        self.ax = 0.0
        self.ay = GRAVIDADE
        self.az = 0.0

        # Tempo de vida da particula
        self.vida = random.uniform(2.0, 3.5)

        # Idade atual
        self.idade = 0.0


    def atualizar_posicao_inicial(self, idade):
        # Inicializa a particula em um instante aleatorio
        # da sua trajetoria, utilizando as equacoes
        # do movimento uniformemente variado.
        self.idade = idade

        self.x = (
            self.origem_x +
            self.vx_inicial * idade
        )

        self.y = (
            self.origem_y +
            self.vy_inicial * idade +
            0.5 * GRAVIDADE * idade ** 2
        )

        self.z = (
            self.origem_z +
            self.vz_inicial * idade
        )

        self.vx = self.vx_inicial
        self.vy = self.vy_inicial + GRAVIDADE * idade
        self.vz = self.vz_inicial



    # Atualizacao das propriedades fisicas
    def atualizar(self, dt):
        # Incrementa a idade.
        self.idade += dt

        # Verifica se a particula terminou seu tempo de vida.
        if self.idade >= self.vida:
            # Reutiliza a particula.
            self.reiniciar()
            return

        # Metodo de Euler semi-implicito:
        # Primeiro atualizamos a velocidade:
        # v = v + a * dt
        #
        # Depois atualizamos a posicao:
        # p = p + v * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.vz += self.az * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

    # Calculo da cor e transparencia
    def obter_cor(self):
        # Calcula quanto do tempo de vida ja foi utilizado
        progresso = self.idade / self.vida

        # Vermelho permanece constante
        vermelho = 1.0

        # Verde diminui gradualmente
        verde = 1.0 - (progresso * 0.85)

        # Azul permanece praticamente constante
        azul = 0.05

        # A transparencia diminui conforme a particula envelhece
        alpha = 1.0 - progresso

        return vermelho, verde, azul, alpha


# CRIACAO DO SISTEMA DE PARTICULAS
particulas = []

for i in range(QUANTIDADE_PARTICULAS):

    particulas.append(Particula())


# CONFIGURACAO DO OPENGL
def configurar_opengl():
    # glViewport define a regiao da janela onde a cena
    # OpenGL sera desenhada
    glViewport(0, 0, LARGURA, ALTURA)

    # glMatrixMode seleciona qual matriz sera modificada
    # GL_PROJECTION seleciona a matriz de projecao
    glMatrixMode(GL_PROJECTION)

    # glLoadIdentity substitui a matriz atual pela
    # matriz identidade
    glLoadIdentity()

    # gluPerspective configura a projecao em perspectiva
    #
    # 45.0 = angulo de abertura da camera
    # largura/altura = proporcao da janela
    # 0.1 = distancia minima de visualizacao
    # 100.0 = distancia maxima de visualizacao
    gluPerspective(
        45.0,
        LARGURA / ALTURA,
        0.1,
        100.0
    )

    # GL_MODELVIEW seleciona a matriz de modelo e visualizacao
    glMatrixMode(GL_MODELVIEW)

    # glEnable ativa uma funcionalidade do OpenGL
    # GL_DEPTH_TEST ativa o teste de profundidade,
    # permitindo determinar quais objetos estao a frente
    glEnable(GL_DEPTH_TEST)

    # GL_BLEND habilita a mistura de cores
    glEnable(GL_BLEND)

    # glBlendFunc define como as cores serao combinadas
    #
    # GL_SRC_ALPHA considera a transparencia da origem
    # GL_ONE utiliza o valor 1 como fator de destino
    #
    # Essa combinacao produz um efeito luminoso aditivo
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    # GL_POINT_SMOOTH solicita o suavizamento dos pontos
    # quando suportado pelo contexto OpenGL
    glEnable(GL_POINT_SMOOTH)

    # glPointSize define o tamanho dos pontos em pixels
    glPointSize(7.0)

    # glClearColor define a cor utilizada para limpar
    # o fundo da janela
    # Neste caso, utilizamos preto
    glClearColor(0.0, 0.0, 0.0, 1.0)


# ATUALIZACAO DO SISTEMA
def atualizar_sistema(dt):
    for particula in particulas:
        particula.atualizar(dt)


# RENDERIZACAO DAS PARTICULAS
def desenhar_particulas():
    # GL_MODELVIEW seleciona a matriz utilizada
    # para posicionar e visualizar os objetos.
    glMatrixMode(GL_MODELVIEW)

    # glLoadIdentity reinicializa a matriz atual
    glLoadIdentity()

    # gluLookAt posiciona e orienta a camera virtual
    #
    # Primeiros tres parametros: posicao da camera
    # Segundos tres parametros: ponto observado
    # Ultimos tres parametros: direcao vertical da camera
    gluLookAt(
        0.0, 5.0, 18.0,
        0.0, 3.0, 0.0,
        0.0, 1.0, 0.0
    )

    # glBegin(GL_POINTS) inicia a construcao de primitivas
    # graficas do tipo ponto
    glBegin(GL_POINTS)

    for particula in particulas:
        # Recupera a cor e a transparencia
        r, g, b, alpha = particula.obter_cor()

        # glColor4f define a cor utilizando quatro componentes:
        # vermelho, verde, azul e alpha (transparencia)
        glColor4f(r, g, b, alpha)

        # glVertex3f informa a posicao tridimensional
        # do ponto que representa a particula
        glVertex3f(
            particula.x,
            particula.y,
            particula.z
        )

    # glEnd finaliza a construcao das primitivas
    glEnd()

def main():
    # pygame.init inicializa os modulos do Pygame
    pygame.init()

    # Cria uma janela com suporte a OpenGL
    # DOUBLEBUF habilita o uso de dois buffers de imagem
    pygame.display.set_mode(
        (LARGURA, ALTURA),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption(
        "Sistema de Particulas - Fonte 3D"
    )

    configurar_opengl()

    # Clock controla o tempo entre os quadros
    relogio = pygame.time.Clock()

    executando = True

    while executando:

        # Calcula o intervalo de tempo entre os quadros
        # O resultado e convertido de milissegundos para segundos
        dt = relogio.tick(60) / 1000.0

        # Limita o intervalo para evitar grandes saltos
        # na simulacao caso a aplicacao fique temporariamente parada
        dt = min(dt, 0.05)

        # Processamento dos eventos
        for evento in pygame.event.get():

            if evento.type == QUIT:
                executando = False

        # Atualiza a fisica das particulas
        atualizar_sistema(dt)

        # glClear limpa os buffers especificados
        # GL_COLOR_BUFFER_BIT limpa a imagem anterior
        # GL_DEPTH_BUFFER_BIT limpa as informacoes de profundidade
        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        # Renderiza as particulas
        desenhar_particulas()

        # pygame.display.flip troca os buffers,
        # apresentando na tela a imagem que acabou de ser desenhada
        pygame.display.flip()

    # Encerra o Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
