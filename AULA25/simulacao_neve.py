
import pygame
import random
import math

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

LARGURA = 1000
ALTURA = 700

QUANTIDADE_PARTICULAS = 600

FPS = 60

# Limites horizontais do emissor
EMISSOR_X_MIN = -10.0
EMISSOR_X_MAX = 10.0

# Altura de emissao
EMISSOR_Y = 10.0

# Limite inferior
LIMITE_INFERIOR = -10.0

# Gravidade reduzida para representar a queda lenta
GRAVIDADE = -0.5

# CLASSE PARTICULA
class Particula:

    def __init__(self):
        self.reiniciar()

        # Distribui inicialmente os flocos em diferentes alturas
        self.y = random.uniform(
            LIMITE_INFERIOR,
            EMISSOR_Y
        )


    def reiniciar(self):

        # Posicao inicial
        self.x = random.uniform(
            EMISSOR_X_MIN,
            EMISSOR_X_MAX
        )

        self.y = EMISSOR_Y
        self.z = random.uniform(-5.0, 5.0)

        # Velocidade vertical
        self.vy = random.uniform(-1.0, -0.3)

        # Velocidade horizontal de referencia
        self.vx = random.uniform(-0.4, 0.4)

        self.vz = 0.0

        # Aceleracao gravitacional
        self.ay = GRAVIDADE

        # Parametros da oscilacao
        self.amplitude = random.uniform(0.2, 1.0)
        self.frequencia = random.uniform(1.0, 3.0)
        self.fase = random.uniform(0, 2 * math.pi)

        # Tempo de vida
        self.vida = random.uniform(8.0, 15.0)
        self.idade = 0.0

        # Tamanho visual do floco
        self.tamanho = random.uniform(2.0, 7.0)

        # Intensidade luminosa
        self.alpha = random.uniform(0.6, 1.0)

        # Guarda a posicao horizontal de referencia
        self.x_inicial = self.x


    # ATUALIZACAO DA PARTICULA
    def atualizar(self, dt):

        # Incrementa a idade
        self.idade += dt

        # Verifica o tempo de vida
        if self.idade >= self.vida:
            self.reiniciar()
            return

        # Atualiza a velocidade vertical
        self.vy += self.ay * dt

        # Atualiza a posicao vertical
        self.y += self.vy * dt

        # Oscilacao horizontal
        #
        # A funcao seno produz um movimento lateral
        # Cada particula possui amplitude, frequencia
        # e fase diferentes
        oscilacao = self.amplitude * math.sin(
            self.frequencia * self.idade + self.fase
        )

        # Movimento horizontal
        self.x = (
            self.x_inicial +
            self.vx * self.idade +
            oscilacao
        )

        # Verifica se atingiu o limite inferior
        if self.y < LIMITE_INFERIOR:
            self.reiniciar()


    # CALCULO DA TRANSPARENCIA
    def obter_alpha(self):
        progresso = self.idade / self.vida
        # A particula desaparece gradualmente
        return self.alpha * (1.0 - progresso)


# CRIACAO DAS PARTICULAS
particulas = []
for i in range(QUANTIDADE_PARTICULAS):
    particulas.append(Particula())

def configurar_opengl():
    # Define a area de renderizacao
    glViewport(0, 0, LARGURA, ALTURA)

    # Seleciona a matriz de projecao
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Configura projecao em perspectiva
    gluPerspective(
        45,
        LARGURA / ALTURA,
        0.1,
        100
    )

    # Seleciona a matriz de modelo e visualizacao
    glMatrixMode(GL_MODELVIEW)

    # Habilita teste de profundidade
    glEnable(GL_DEPTH_TEST)

    # Habilita transparencia
    glEnable(GL_BLEND)

    # Mistura convencional
    glBlendFunc(
        GL_SRC_ALPHA,
        GL_ONE_MINUS_SRC_ALPHA
    )

    # Suaviza os pontos, quando suportado
    glEnable(GL_POINT_SMOOTH)

    # Define o tamanho padrao
    glPointSize(5.0)

    # Fundo azul escuro
    glClearColor(
        0.02,
        0.04,
        0.12,
        1.0
    )


# ATUALIZACAO DO SISTEMA
def atualizar_sistema(dt):
    for particula in particulas:
        particula.atualizar(dt)

# RENDERIZACAO
def desenhar_particulas():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Configuracao da camera
    gluLookAt(
        0, 0, 22,
        0, 0, 0,
        0, 1, 0
    )

    # Define o tamanho uniforme dos pontos
    glPointSize(5.0)

    # Inicia a renderizacao dos pontos
    glBegin(GL_POINTS)

    for particula in particulas:
        # Transparencia individual
        alpha = particula.obter_alpha()

        # Cor branca com leve tonalidade azul
        glColor4f(
            0.85,
            0.92,
            1.0,
            alpha
        )

        # Posicao tridimensional
        glVertex3f(
            particula.x,
            particula.y,
            particula.z
        )

    glEnd()

def main():
    pygame.init()
    pygame.display.set_mode(
        (LARGURA, ALTURA),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption(
        "Sistema de Particulas - Simulacao de Neve"
    )

    configurar_opengl()
    relogio = pygame.time.Clock()
    executando = True

    while executando:
        # Tempo entre os quadros
        dt = relogio.tick(FPS) / 1000.0
        dt = min(dt, 0.05)

        # Eventos
        for evento in pygame.event.get():

            if evento.type == QUIT:
                executando = False

            if evento.type == KEYDOWN:

                if evento.key == K_ESCAPE:
                    executando = False

        # Atualizacao.
        atualizar_sistema(dt)

        # Limpeza dos buffers
        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        # Renderizacao
        desenhar_particulas()

        # Apresentacao da imagem
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
