import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image
import ctypes
import math
import os

cam_pos   = np.array([15.0, 6.0, 28.0], dtype=np.float32)
cam_front = np.array([0.0, -0.2, -1.0], dtype=np.float32)
cam_up    = np.array([0.0, 1.0, 0.0], dtype=np.float32)

yaw, pitch = -90.0, -10.0
primeiro_mouse = True
ultimo_x, ultimo_y = 500.0, 350.0

def mouse_callback(window, xpos, ypos):
    global primeiro_mouse, ultimo_x, ultimo_y, yaw, pitch, cam_front
    if primeiro_mouse:
        ultimo_x, ultimo_y = xpos, ypos
        primeiro_mouse = False

    xoffset = (xpos - ultimo_x) * 0.1
    yoffset = (ultimo_y - ypos) * 0.1
    ultimo_x, ultimo_y = xpos, ypos

    yaw += xoffset
    pitch = max(-89.0, min(89.0, pitch + yoffset))

    direcao = np.array([
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ], dtype=np.float32)
    cam_front = direcao / np.linalg.norm(direcao)

def processar_teclado(window, delta_time):
    global cam_pos
    velocidade = 12.0 * delta_time # Navegação rápida para percorrer o sistema solar

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    cam_right = np.cross(cam_front, cam_up)
    cam_right = cam_right / np.linalg.norm(cam_right)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:          cam_pos += velocidade * cam_front
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:          cam_pos -= velocidade * cam_front
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:          cam_pos -= velocidade * cam_right
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:          cam_pos += velocidade * cam_right
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:      cam_pos += velocidade * cam_up
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS: cam_pos -= velocidade * cam_up


def gerar_esfera_uv(raio=1.0, setores=48, pilhas=24):
    """
    Gera uma esfera paramétrica usando coordenadas esféricas
    Cada vértice contém 8 floats: [X, Y, Z, NX, NY, NZ, U, V]
    """
    vertices = []
    indices = []

    for i in range(pilhas + 1):
        # Ângulo vertical (latitude): vai de +pi/2 (Polo Norte) até -pi/2 (Polo Sul)
        phi = math.pi / 2.0 - i * (math.pi / pilhas)
        xy = raio * math.cos(phi)
        y  = raio * math.sin(phi)
        v  = i / pilhas # Coordenada V da textura (0 no topo, 1 na base)

        for j in range(setores + 1):
            # Ângulo horizontal (longitude): vai de 0 até 2*pi
            theta = j * (2.0 * math.pi / setores)
            x = xy * math.cos(theta)
            z = xy * math.sin(theta)
            u = j / setores # Coordenada U da textura (0 a 1 ao redor do equador)

            # Em uma esfera centrada na origem, a normal é a própria posição normalizada
            nx, ny, nz = x / raio, y / raio, z / raio
            vertices.extend([x, y, z, nx, ny, nz, u, v])

    for i in range(pilhas):
        k1 = i * (setores + 1)
        k2 = k1 + setores + 1
        for j in range(setores):
            if i != 0:
                indices.extend([k1, k2, k1 + 1])
            if i != (pilhas - 1):
                indices.extend([k1 + 1, k2, k2 + 1])
            k1 += 1
            k2 += 1

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def carregar_textura(caminho_relativo, cor_fallback):
    # Cria 1 identificador (ID) de textura na memória da GPU
    tex_id = glGenTextures(1)
    # Vincula esse ID como a textura 2D ativa para configurá-la
    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Define regras de repetição (WRAP) e filtragem/suavização (FILTER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    dir_base = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(dir_base, caminho_relativo)

    if os.path.exists(caminho_completo):
        img = Image.open(caminho_completo).convert("RGB")
        dados_img = img.tobytes()
        largura, altura = img.size
    else:
        # gera uma textura 2x2 com a cor sólida caso o arquivo .jpg não exista
        dados_img = np.array([cor_fallback] * 4, dtype=np.uint8).tobytes()
        largura, altura = 2, 2

    # Evita distorções caso a largura da imagem não seja múltipla de 4 bytes
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # Envia os bytes da imagem da RAM para a VRAM da GPU
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, dados_img)

    # Cria versões menores da textura automaticamente para evitar serrilhado à distância
    glGenerateMipmap(GL_TEXTURE_2D)

    return tex_id

def criar_programa_de_arquivos(caminho_vert, caminho_frag):
    dir_base = os.path.dirname(os.path.abspath(__file__))
    def compilar(caminho, tipo):
        with open(os.path.join(dir_base, caminho), "r", encoding="utf-8") as f:
            src = f.read()
        sh = glCreateShader(tipo)
        glShaderSource(sh, src)
        glCompileShader(sh)
        if not glGetShaderiv(sh, GL_COMPILE_STATUS):
            raise RuntimeError(f"Erro em {caminho}:\n{glGetShaderInfoLog(sh).decode()}")
        return sh

    vs = compilar(caminho_vert, GL_VERTEX_SHADER)
    fs = compilar(caminho_frag, GL_FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog

def matriz_perspectiva(fovy, aspecto, near, far):
    f = 1.0 / math.tan(math.radians(fovy) / 2.0)
    return np.array([
        [f / aspecto, 0.0, 0.0, 0.0],
        [0.0, f, 0.0, 0.0],
        [0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
        [0.0, 0.0, -1.0, 0.0]
    ], dtype=np.float32)

def matriz_look_at(eye, target, up):
    f = (target - eye); f /= np.linalg.norm(f)
    s = np.cross(f, up); s /= np.linalg.norm(s)
    u = np.cross(s, f)
    return np.array([
        [ s[0],  s[1],  s[2], -np.dot(s, eye)],
        [ u[0],  u[1],  u[2], -np.dot(u, eye)],
        [-f[0], -f[1], -f[2],  np.dot(f, eye)],
        [ 0.0,   0.0,   0.0,   1.0]
    ], dtype=np.float32)

def matriz_translacao_escala(tx, ty, tz, s):
    # Combina translação (tx, ty, tz) e escala uniforme (s) em uma única matriz 4x4
    return np.array([
        [  s, 0.0, 0.0,  tx],
        [0.0,   s, 0.0,  ty],
        [0.0, 0.0,   s,  tz],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def main():
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    largura, altura = 1000, 700
    window = glfw.create_window(largura, altura, "Sistema Solar", None, None)
    if not window: glfw.terminate(); return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glEnable(GL_DEPTH_TEST)

    shader = criar_programa_de_arquivos("shaders/planeta.vert", "shaders/planeta.frag")

    # Gera 1 única esfera unitária na VRAM para ser reutilizada por todos
    vertices, indices = gerar_esfera_uv(raio=1.0, setores=48, pilhas=24)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    stride = 8 * vertices.itemsize # 8 floats por vértice (32 bytes)
    # Posição (3 floats, início no byte 0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # Normal (3 floats, início no byte 12)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    # UV (2 floats, início no byte 24)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * vertices.itemsize))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)

    astros_config = [
        ("Sol",      "texturas/sol.jpg",      3.5,  0.0, (255, 200,  40), True),
        ("Mercúrio", "texturas/mercurio.jpg", 0.4,  6.0, (160, 155, 150), False),
        ("Vênus",    "texturas/venus.jpg",    0.7,  8.5, (220, 180, 110), False),
        ("Terra",    "texturas/terra.jpg",    0.75, 11.5, ( 40, 110, 210), False),
        ("Marte",    "texturas/marte.jpg",    0.55, 14.5, (200,  80,  50), False),
        ("Júpiter",  "texturas/jupiter.jpg",  2.0,  19.5, (210, 160, 120), False),
        ("Saturno",  "texturas/saturno.jpg",  1.7,  25.5, (225, 205, 150), False),
        ("Urano",    "texturas/urano.jpg",    1.1,  30.5, (120, 210, 225), False),
        ("Netuno",   "texturas/netuno.jpg",   1.1,  35.0, ( 50,  80, 210), False),
    ]

    # Carrega todas as texturas na GPU uma única vez antes do loop
    astros = []
    for nome, arq, raio, pos_x, cor, eh_sol in astros_config:
        tex_id = carregar_textura(arq, cor)
        model = matriz_translacao_escala(pos_x, 0.0, 0.0, raio)
        astros.append((tex_id, model, eh_sol))

    # Localizações dos Uniforms
    loc_model    = glGetUniformLocation(shader, "model")
    loc_view     = glGetUniformLocation(shader, "view")
    loc_proj     = glGetUniformLocation(shader, "projection")
    loc_eh_sol   = glGetUniformLocation(shader, "ehSol")
    loc_lightpos = glGetUniformLocation(shader, "lightPos")
    loc_viewpos  = glGetUniformLocation(shader, "viewPos")

    projection = matriz_perspectiva(45.0, largura / altura, 0.1, 200.0)
    ultimo_frame = 0.0

    while not glfw.window_should_close(window):
        tempo_atual = glfw.get_time()
        delta_time = tempo_atual - ultimo_frame
        ultimo_frame = tempo_atual

        processar_teclado(window, delta_time)

        # Espaço sideral (preto quase absoluto)
        glClearColor(0.01, 0.01, 0.02, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)
        view = matriz_look_at(cam_pos, cam_pos + cam_front, cam_up)

        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_proj, 1, GL_TRUE, projection)
        glUniform3f(loc_lightpos, 0.0, 0.0, 0.0) # Luz nasce no centro do Sol
        glUniform3f(loc_viewpos, *cam_pos)

        glBindVertexArray(VAO)

        # Desenha cada astro reaproveitando o mesmo VAO da esfera
        for tex_id, model, eh_sol in astros:
            # Seleciona a unidade de textura 0 antes de vincular a textura do astro
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, tex_id)

            glUniformMatrix4fv(loc_model, 1, GL_TRUE, model)
            # Envia 1 (True) ou 0 (False) para a variável bool no shader
            glUniform1i(loc_eh_sol, 1 if eh_sol else 0)

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