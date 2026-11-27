import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import math
import os

cam_pos   = np.array([0.0, 2.2, 7.5], dtype=np.float32)
cam_front = np.array([0.0, -0.25, -1.0], dtype=np.float32)
cam_up    = np.array([0.0, 1.0, 0.0], dtype=np.float32)

# Ângulos de Euler iniciais (em graus)
yaw   = -90.0  # -90° faz a câmera olhar para o eixo -Z
pitch = -15.0  # Levemente inclinada para baixo, olhando o lago

# Controle do mouse
primeiro_mouse = True
ultimo_x, ultimo_y = 450.0, 300.0
sensibilidade_mouse = 0.1

def mouse_callback(window, xpos, ypos):
    global primeiro_mouse, ultimo_x, ultimo_y, yaw, pitch, cam_front

    # tentando evita um movimebntos bruscos na câmera 
    # no primeiro frame em que o mouse entra na janela
    if primeiro_mouse:
        ultimo_x, ultimo_y = xpos, ypos
        primeiro_mouse = False

    xoffset = (xpos - ultimo_x) * sensibilidade_mouse
    # cuidado para não esquecer, inveter aqui pois Y cresce de cima para baixo na tela
    yoffset = (ultimo_y - ypos) * sensibilidade_mouse  
    ultimo_x, ultimo_y = xpos, ypos

    yaw   += xoffset
    pitch += yoffset

    # Trava o pitch entre -89° e +89° 
    pitch = max(-89.0, min(89.0, pitch))

    # Converte os ângulos esféricos (yaw, pitch) em um vetor 3D normalizado
    direcao = np.array([
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ], dtype=np.float32)
    cam_front = direcao / np.linalg.norm(direcao)


def processar_teclado(window, delta_time):
    global cam_pos
    velocidade = 5.0 * delta_time  # Velocidade constante independente do FPS do computador

    # Consulta o estado atual de uma tecla (pressionada ou solta) a cada frame.
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    # Vetor lateral (Direita) obtido pelo produto vetorial entre Frente e Cima
    cam_right = np.cross(cam_front, cam_up)
    cam_right = cam_right / np.linalg.norm(cam_right)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        cam_pos += velocidade * cam_front
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        cam_pos -= velocidade * cam_front
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        cam_pos -= velocidade * cam_right
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        cam_pos += velocidade * cam_right
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        cam_pos += velocidade * cam_up
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        cam_pos -= velocidade * cam_up

def ler_arquivo_shader(caminho):
    # tentando garantir que o caminho funcione 
    # independente de onde o script seja chamado
    dir_base = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(dir_base, caminho)
    with open(caminho_completo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()

def compilar_shader(caminho, tipo):
    codigo_fonte = ler_arquivo_shader(caminho)
    shader = glCreateShader(tipo)
    glShaderSource(shader, codigo_fonte)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Erro ao compilar {caminho}:\n{erro}")
    return shader

def criar_programa_de_arquivos(caminho_vert, caminho_frag):
    vs = compilar_shader(caminho_vert, GL_VERTEX_SHADER)
    fs = compilar_shader(caminho_frag, GL_FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog).decode())
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog

def gerar_malha_lago(tamanho=20.0, divisoes=100):
    vertices = []
    passo = tamanho / divisoes
    metade = tamanho / 2.0

    for z in range(divisoes + 1):
        for x in range(divisoes + 1):
            vertices.extend([-metade + x * passo, 0.0, -metade + z * passo])

    indices = []
    for z in range(divisoes):
        for x in range(divisoes):
            tl = z * (divisoes + 1) + x
            tr = tl + 1
            bl = (z + 1) * (divisoes + 1) + x
            br = bl + 1
            indices.extend([tl, bl, tr, tr, bl, br])

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def matriz_perspectiva(fovy_graus, aspecto, near, far):
    f = 1.0 / math.tan(math.radians(fovy_graus) / 2.0)
    return np.array([
        [f / aspecto, 0.0, 0.0, 0.0],
        [0.0, f, 0.0, 0.0],
        [0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
        [0.0, 0.0, -1.0, 0.0]
    ], dtype=np.float32)

def matriz_look_at(eye, target, up):
    f = target - eye
    f = f / np.linalg.norm(f)
    s = np.cross(f, up)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)
    return np.array([
        [ s[0],  s[1],  s[2], -np.dot(s, eye)],
        [ u[0],  u[1],  u[2], -np.dot(u, eye)],
        [-f[0], -f[1], -f[2],  np.dot(f, eye)],
        [ 0.0,   0.0,   0.0,   1.0]
    ], dtype=np.float32)

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    largura, altura = 900, 600
    window = glfw.create_window(largura, altura, "Lago 3D (ESC para sair)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Captura e oculta o cursor do mouse dentro da janela (padrão de jogos 3D)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Registra a função chamada sempre que o mouse se move
    glfw.set_cursor_pos_callback(window, mouse_callback)

    glEnable(GL_DEPTH_TEST)

    # Carrega os shaders diretamente dos arquivos .vert e .frag
    shader = criar_programa_de_arquivos("shaders/lago.vert", "shaders/lago.frag")
    vertices, indices = gerar_malha_lago(tamanho=24.0, divisoes=100)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    loc_model   = glGetUniformLocation(shader, "model")
    loc_view    = glGetUniformLocation(shader, "view")
    loc_proj    = glGetUniformLocation(shader, "projection")
    loc_tempo   = glGetUniformLocation(shader, "tempo")
    loc_viewpos = glGetUniformLocation(shader, "viewPos")
    loc_sundir  = glGetUniformLocation(shader, "sunDir")

    model = np.identity(4, dtype=np.float32)
    projection = matriz_perspectiva(45.0, largura / altura, 0.1, 100.0)

    ultimo_frame = 0.0

    while not glfw.window_should_close(window):
        # Cálculo do delta_time (tempo decorrido desde o último frame)
        tempo_atual = glfw.get_time()
        delta_time = tempo_atual - ultimo_frame
        ultimo_frame = tempo_atual

        # Atualiza a posição da câmera com base nas teclas pressionadas
        processar_teclado(window, delta_time)

        glClearColor(0.65, 0.80, 0.92, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        # Recalcula a matriz View a cada frame: a câmera sempre olha para (cam_pos + cam_front)
        view = matriz_look_at(cam_pos, cam_pos + cam_front, cam_up)

        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_proj, 1, GL_TRUE, projection)
        glUniform1f(loc_tempo, tempo_atual)
        glUniform3f(loc_viewpos, *cam_pos)
        glUniform3f(loc_sundir, 0.0, 0.25, -1.0)

        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader)
    glfw.terminate()

if __name__ == "__main__":
    main()