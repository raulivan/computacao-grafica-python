import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import math

VERTEX_SHADER_SRC = """
#version 330 core

layout (location = 0) in vec3 aPos;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float tempo;

void main()
{
    vec3 pos = aPos;

    // SOMA DE ONDAS (Deslocamento em Y)
    // Misturamos 3 ondas em direções e frequências diferentes para parecer natural
    float w1 = 0.12 * sin(pos.x * 1.5 + tempo * 1.8);
    float w2 = 0.08 * cos(pos.z * 2.0 + tempo * 1.3);
    float w3 = 0.05 * sin((pos.x + pos.z) * 3.0 - tempo * 2.5);
    
    pos.y = w1 + w2 + w3;

    // NORMAIS ANALÍTICAS (Cálculo via Derivadas Parciais) 
    // dy/dx: derivada das ondas em relação a X
    float dydx = 0.12 * 1.5 * cos(pos.x * 1.5 + tempo * 1.8)
               + 0.05 * 3.0 * cos((pos.x + pos.z) * 3.0 - tempo * 2.5);
               
    // dy/dz: derivada das ondas em relação a Z
    float dydz = -0.08 * 2.0 * sin(pos.z * 2.0 + tempo * 1.3)
               + 0.05 * 3.0 * cos((pos.x + pos.z) * 3.0 - tempo * 2.5);

    // Vetor normal perpendicular à superfície curva: (-dy/dx, 1, -dy/dz)
    vec3 normalLocal = normalize(vec3(-dydx, 1.0, -dydz));

    FragPos = vec3(model * vec4(pos, 1.0));
    Normal = mat3(transpose(inverse(model))) * normalLocal;
    
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
"""

FRAGMENT_SHADER_SRC = """
#version 330 core

in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

uniform vec3 viewPos;
uniform vec3 sunDir; // Direção do Sol (vetor normalizado)

void main()
{
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    //  COR BASE DA ÁGUA
    vec3 corAguaFunda = vec3(0.01, 0.15, 0.25); // Azul petróleo escuro

    // REFLEXO PROCEDURAL DO CÉU 
    // Calcula para onde o raio da câmera rebate ao bater na onda
    vec3 reflectDir = reflect(-viewDir, norm);
    
    // Simula um degradê de céu: mais claro no horizonte (y baixo), mais azul no topo (y alto)
    float fatorCeu = clamp(reflectDir.y, 0.0, 1.0);
    vec3 corHorizonte = vec3(0.65, 0.80, 0.92);
    vec3 corTopoCeu   = vec3(0.15, 0.45, 0.85);
    vec3 corReflexoCeu = mix(corHorizonte, corTopoCeu, pow(fatorCeu, 0.6));

    // EFEITO FRESNEL (Aproximação de Schlick)
    // Ângulos rasantes refletem mais o céu; olhar de cima mostra mais a água funda
    float fresnel = 0.04 + 0.96 * pow(1.0 - max(dot(norm, viewDir), 0.0), 4.0);
    vec3 corFinal = mix(corAguaFunda, corReflexoCeu, fresnel);

    // BRILHO ESPECULAR DO SOL NAS ONDAS
    float spec = pow(max(dot(reflectDir, normalize(sunDir)), 0.0), 180.0);
    vec3 corSol = vec3(1.0, 0.95, 0.85); // Sol levemente dourado
    corFinal += corSol * spec * 1.5;

    FragColor = vec4(corFinal, 1.0);
}
"""

def gerar_malha_lago(tamanho=12.0, divisoes=60):
    """
    Cria uma grade plana no plano XZ com (divisoes+1)^2 vértices
    e uma lista de índices formando os triângulos.
    """
    vertices = []
    passo = tamanho / divisoes
    metade = tamanho / 2.0

    for z in range(divisoes + 1):
        for x in range(divisoes + 1):
            px = -metade + x * passo
            pz = -metade + z * passo
            vertices.extend([px, 0.0, pz])

    indices = []
    for z in range(divisoes):
        for x in range(divisoes):
            # Índices dos 4 cantos de cada célula quadrada
            top_left     = z * (divisoes + 1) + x
            top_right    = top_left + 1
            bottom_left  = (z + 1) * (divisoes + 1) + x
            bottom_right = bottom_left + 1

            # Divide o quadrado em 2 triângulos
            indices.extend([top_left, bottom_left, top_right])
            indices.extend([top_right, bottom_left, bottom_right])

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

def criar_programa(vs_src, fs_src):
    vs = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vs, vs_src)
    glCompileShader(vs)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(vs).decode())

    fs = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fs, fs_src)
    glCompileShader(fs)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(fs).decode())

    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    largura, altura = 900, 600
    window = glfw.create_window(largura, altura, "Simulação de Lago - GLSL (Ondas + Fresnel)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    shader = criar_programa(VERTEX_SHADER_SRC, FRAGMENT_SHADER_SRC)
    vertices, indices = gerar_malha_lago(tamanho=14.0, divisoes=80)

    # Criação do VAO, VBO e EBO (Element Buffer Object)
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1) # EBO armazena os índices dos triângulos para evitar duplicar vértices

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # GL_ELEMENT_ARRAY_BUFFER: Vincula o buffer de índices ao VAO atual
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Atributo 0: Posição (X, Y, Z)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    # Localizações dos Uniforms
    loc_model   = glGetUniformLocation(shader, "model")
    loc_view    = glGetUniformLocation(shader, "view")
    loc_proj    = glGetUniformLocation(shader, "projection")
    loc_tempo   = glGetUniformLocation(shader, "tempo")
    loc_viewpos = glGetUniformLocation(shader, "viewPos")
    loc_sundir  = glGetUniformLocation(shader, "sunDir")

    model = np.identity(4, dtype=np.float32)
    pos_camera = np.array([0.0, 2.2, 7.5], dtype=np.float32)
    view = matriz_look_at(pos_camera, np.array([0.0, 0.0, 0.0], dtype=np.float32), np.array([0.0, 1.0, 0.0], dtype=np.float32))
    projection = matriz_perspectiva(45.0, largura / altura, 0.1, 100.0)

    while not glfw.window_should_close(window):
        # Cor de fundo igual à cor do horizonte para integrar o lago ao céu
        glClearColor(0.65, 0.80, 0.92, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_proj, 1, GL_TRUE, projection)
        glUniform1f(loc_tempo, glfw.get_time())
        glUniform3f(loc_viewpos, *pos_camera)
        glUniform3f(loc_sundir, 0.0, 0.25, -1.0) # Sol baixo no horizonte, à frente da câmera

        glBindVertexArray(VAO)
        # glDrawElements: Desenha os triângulos usando os índices armazenados no EBO
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