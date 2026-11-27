import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image
import ctypes
import math
import os
import random

cam_pos   = np.array([0.0, 18.0, 42.0], dtype=np.float32)
cam_front = np.array([0.0, -0.35, -1.0], dtype=np.float32)
cam_up    = np.array([0.0, 1.0, 0.0], dtype=np.float32)

yaw, pitch = -90.0, -22.0
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
    velocidade = 14.0 * delta_time

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
    vertices, indices = [], []
    for i in range(pilhas + 1):
        phi = math.pi / 2.0 - i * (math.pi / pilhas)
        xy = raio * math.cos(phi)
        y  = raio * math.sin(phi)
        v  = i / pilhas
        for j in range(setores + 1):
            theta = j * (2.0 * math.pi / setores)
            x = xy * math.cos(theta)
            z = xy * math.sin(theta)
            u = j / setores
            vertices.extend([x, y, z, x / raio, y / raio, z / raio, u, v])

    for i in range(pilhas):
        k1 = i * (setores + 1)
        k2 = k1 + setores + 1
        for j in range(setores):
            if i != 0:            indices.extend([k1, k2, k1 + 1])
            if i != (pilhas - 1): indices.extend([k1 + 1, k2, k2 + 1])
            k1 += 1
            k2 += 1

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

def gerar_estrelas(quantidade=1800, raio_min=110.0, raio_max=180.0):
    """
    Distribui pontos uniformemente em uma casca esférica ao redor da cena.
    Cada estrela tem 7 floats: [X, Y, Z, R, G, B, Tamanho]
    """
    estrelas = []
    # Tons sutis de estrelas reais (branco, azulado, amarelado)
    paleta = [
        (1.0, 1.0, 1.0),
        (0.8, 0.9, 1.0),
        (1.0, 0.95, 0.8),
        (0.7, 0.8, 1.0)
    ]

    for _ in range(quantidade):
        # Distribuição esférica uniforme (evita aglomeração nos polos)
        theta = random.uniform(0.0, 2.0 * math.pi)
        cos_phi = random.uniform(-1.0, 1.0)
        sin_phi = math.sqrt(1.0 - cos_phi * cos_phi)
        r = random.uniform(raio_min, raio_max)

        x = r * sin_phi * math.cos(theta)
        y = r * cos_phi
        z = r * sin_phi * math.sin(theta)

        cor = random.choice(paleta)
        intensidade = random.uniform(0.5, 1.0)
        tamanho = random.uniform(1.5, 4.0)

        estrelas.extend([x, y, z, cor[0]*intensidade, cor[1]*intensidade, cor[2]*intensidade, tamanho])

    return np.array(estrelas, dtype=np.float32)


def carregar_textura(caminho_relativo, cor_fallback):
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    dir_base = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(dir_base, caminho_relativo)

    if os.path.exists(caminho_completo):
        img = Image.open(caminho_completo).convert("RGB")
        dados_img, largura, altura = img.tobytes(), img.size[0], img.size[1]
    else:
        dados_img = np.array([cor_fallback] * 4, dtype=np.uint8).tobytes()
        largura, altura = 2, 2

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, dados_img)
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
    window = glfw.create_window(largura, altura, "Sistema Solar 3D + Estrelas (WASD + Mouse)", None, None)
    if not window: glfw.terminate(); return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    glEnable(GL_DEPTH_TEST)
    # Permite que o Vertex Shader controle o tamanho dos pontos via gl_PointSize
    glEnable(GL_PROGRAM_POINT_SIZE)

    # Compila os dois programas de shader independentes
    shader_planeta = criar_programa_de_arquivos("shaders/planeta.vert", "shaders/planeta.frag")
    shader_estrela = criar_programa_de_arquivos("shaders/estrela.vert", "shaders/estrela.frag")

    # VAO/VBO/EBO DOS PLANETAS
    vertices, indices = gerar_esfera_uv(raio=1.0, setores=48, pilhas=24)
    VAO_planeta = glGenVertexArrays(1)
    VBO_planeta = glGenBuffers(1)
    EBO_planeta = glGenBuffers(1)

    glBindVertexArray(VAO_planeta)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_planeta)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_planeta)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    stride_p = 8 * vertices.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride_p, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride_p, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride_p, ctypes.c_void_p(6 * vertices.itemsize))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)

    # VAO/VBO DAS ESTRELAS
    qtd_estrelas = 1800
    dados_estrelas = gerar_estrelas(quantidade=qtd_estrelas)
    VAO_estrelas = glGenVertexArrays(1)
    VBO_estrelas = glGenBuffers(1)

    glBindVertexArray(VAO_estrelas)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_estrelas)
    glBufferData(GL_ARRAY_BUFFER, dados_estrelas.nbytes, dados_estrelas, GL_STATIC_DRAW)

    stride_e = 7 * dados_estrelas.itemsize # 7 floats: [X, Y, Z, R, G, B, Size]
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride_e, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride_e, ctypes.c_void_p(3 * dados_estrelas.itemsize))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, stride_e, ctypes.c_void_p(6 * dados_estrelas.itemsize))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)

    # (Nome, Textura, Raio, Distância do Sol, Ângulo Heliocêntrico em graus, Inclinação Y, Cor Fallback, É o Sol?)
    astros_config = [
        ("Sol",      "texturas/sol.jpg",      3.5,  0.0,   0.0,  0.0, (255, 200,  40), True),
        ("Mercúrio", "texturas/mercurio.jpg", 0.4,  6.5,  35.0,  0.4, (160, 155, 150), False),
        ("Vênus",    "texturas/venus.jpg",    0.7,  9.5, 140.0, -0.3, (220, 180, 110), False),
        ("Terra",    "texturas/terra.jpg",    0.75, 13.0, 215.0,  0.0, ( 40, 110, 210), False),
        ("Marte",    "texturas/marte.jpg",    0.55, 16.5, 310.0,  0.3, (200,  80,  50), False),
        ("Júpiter",  "texturas/jupiter.jpg",  2.1,  22.5,  75.0, -0.5, (210, 160, 120), False),
        ("Saturno",  "texturas/saturno.jpg",  1.7,  29.0, 185.0,  0.8, (225, 205, 150), False),
        ("Urano",    "texturas/urano.jpg",    1.1,  35.0, 275.0, -0.4, (120, 210, 225), False),
        ("Netuno",   "texturas/netuno.jpg",   1.1,  41.0,  15.0,  0.6, ( 50,  80, 210), False),
    ]

    astros = []
    for nome, arq, raio, dist, angulo_graus, incl_y, cor, eh_sol in astros_config:
        tex_id = carregar_textura(arq, cor)
        rad = math.radians(angulo_graus)
        pos_x = dist * math.cos(rad)
        pos_z = dist * math.sin(rad)
        model = matriz_translacao_escala(pos_x, incl_y, pos_z, raio)
        astros.append((tex_id, model, eh_sol))

    # Uniforms do Shader de Planetas
    loc_p_model    = glGetUniformLocation(shader_planeta, "model")
    loc_p_view     = glGetUniformLocation(shader_planeta, "view")
    loc_p_proj     = glGetUniformLocation(shader_planeta, "projection")
    loc_p_eh_sol   = glGetUniformLocation(shader_planeta, "ehSol")
    loc_p_lightpos = glGetUniformLocation(shader_planeta, "lightPos")
    loc_p_viewpos  = glGetUniformLocation(shader_planeta, "viewPos")

    # Uniforms do Shader de Estrelas
    loc_e_view = glGetUniformLocation(shader_estrela, "view")
    loc_e_proj = glGetUniformLocation(shader_estrela, "projection")

    # Far plane aumentado para 300.0 para enxergar todas as estrelas distantes
    projection = matriz_perspectiva(45.0, largura / altura, 0.1, 300.0)
    ultimo_frame = 0.0

    while not glfw.window_should_close(window):
        tempo_atual = glfw.get_time()
        delta_time = tempo_atual - ultimo_frame
        ultimo_frame = tempo_atual

        processar_teclado(window, delta_time)

        glClearColor(0.005, 0.005, 0.015, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = matriz_look_at(cam_pos, cam_pos + cam_front, cam_up)

        # DESENHA AS ESTRELAS DE FUNDO
        glUseProgram(shader_estrela)
        glUniformMatrix4fv(loc_e_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_e_proj, 1, GL_TRUE, projection)

        glBindVertexArray(VAO_estrelas)
        # renderizar cada vértice do VBO como um ponto isolado
        glDrawArrays(GL_POINTS, 0, qtd_estrelas)

        # DESENHA O SOL E OS PLANETAS
        glUseProgram(shader_planeta)
        glUniformMatrix4fv(loc_p_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_p_proj, 1, GL_TRUE, projection)
        glUniform3f(loc_p_lightpos, 0.0, 0.0, 0.0)
        glUniform3f(loc_p_viewpos, *cam_pos)

        glBindVertexArray(VAO_planeta)
        for tex_id, model, eh_sol in astros:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glUniformMatrix4fv(loc_p_model, 1, GL_TRUE, model)
            glUniform1i(loc_p_eh_sol, 1 if eh_sol else 0)
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(2, [VAO_planeta, VAO_estrelas])
    glDeleteBuffers(3, [VBO_planeta, EBO_planeta, VBO_estrelas])
    glDeleteProgram(shader_planeta)
    glDeleteProgram(shader_estrela)
    glfw.terminate()

if __name__ == "__main__":
    main()