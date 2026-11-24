import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import math

VERTEX_SHADER_SRC = """
#version 330 core

layout (location = 0) in vec3 aPos;    // Posição local do vértice
layout (location = 1) in vec3 aNormal; // Vetor normal da face

// Dados enviados para o Fragment Shader (serão interpolados por pixel)
out vec3 FragPos;
out vec3 Normal;

// Matrizes MVP enviadas pela CPU
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // Posição do vértice no espaço do mundo (necessária para calcular a direção da luz)
    FragPos = vec3(model * vec4(aPos, 1.0));
    
    // Corrige a normal para acompanhar a rotação/escala do objeto
    Normal = mat3(transpose(inverse(model))) * aNormal;
    
    // Projeção final na tela
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
"""

FRAGMENT_SHADER_SRC = """
#version 330 core

in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

// Propriedades da cena enviadas via uniform
uniform vec3 lightPos;    // Posição da fonte de luz
uniform vec3 viewPos;     // Posição da câmera (observador)
uniform vec3 lightColor;  // Cor da luz
uniform vec3 objectColor; // Cor base do cubo

void main()
{
    // AMBIENTE
    float ambientStrength = 0.15;
    vec3 ambient = ambientStrength * lightColor;

    // DIFUSA (Lei de Lambert)
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // ESPECULAR (Brilho de Phong)
    float specularStrength = 0.8;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm); // Vetor de reflexão da luz
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64.0); // Shininess = 64
    vec3 specular = specularStrength * spec * lightColor;

    // Soma final multiplicada pela cor do objeto
    vec3 resultado = (ambient + diffuse + specular) * objectColor;
    FragColor = vec4(resultado, 1.0);
}
"""

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

def matriz_rotacao_y(angulo):
    c, s = math.cos(angulo), math.sin(angulo)
    return np.array([
        [ c,  0.0, s,  0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-s,  0.0, c,  0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

def matriz_rotacao_x(angulo):
    c, s = math.cos(angulo), math.sin(angulo)
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0,  c,  -s,  0.0],
        [0.0,  s,   c,  0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def compilar_shader(src, tipo):
    shader = glCreateShader(tipo)
    glShaderSource(shader, src)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def criar_programa(vs_src, fs_src):
    vs = compilar_shader(vs_src, GL_VERTEX_SHADER)
    fs = compilar_shader(fs_src, GL_FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog).decode())
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog

# CUBO (36 VÉRTICES = 6 FACES * 2 TRIÂNGULOS * 3 VÉRTICES)
# Formato intercalado: [Posição X, Y, Z,  Normal NX, NY, NZ]

cubo_vertices = np.array([
    # Face Traseira (Normal: 0, 0, -1)
    -0.5, -0.5, -0.5,   0.0,  0.0, -1.0,
     0.5, -0.5, -0.5,   0.0,  0.0, -1.0,
     0.5,  0.5, -0.5,   0.0,  0.0, -1.0,
     0.5,  0.5, -0.5,   0.0,  0.0, -1.0,
    -0.5,  0.5, -0.5,   0.0,  0.0, -1.0,
    -0.5, -0.5, -0.5,   0.0,  0.0, -1.0,

    # Face Frontal (Normal: 0, 0, 1)
    -0.5, -0.5,  0.5,   0.0,  0.0,  1.0,
     0.5, -0.5,  0.5,   0.0,  0.0,  1.0,
     0.5,  0.5,  0.5,   0.0,  0.0,  1.0,
     0.5,  0.5,  0.5,   0.0,  0.0,  1.0,
    -0.5,  0.5,  0.5,   0.0,  0.0,  1.0,
    -0.5, -0.5,  0.5,   0.0,  0.0,  1.0,

    # Face Esquerda (Normal: -1, 0, 0)
    -0.5,  0.5,  0.5,  -1.0,  0.0,  0.0,
    -0.5,  0.5, -0.5,  -1.0,  0.0,  0.0,
    -0.5, -0.5, -0.5,  -1.0,  0.0,  0.0,
    -0.5, -0.5, -0.5,  -1.0,  0.0,  0.0,
    -0.5, -0.5,  0.5,  -1.0,  0.0,  0.0,
    -0.5,  0.5,  0.5,  -1.0,  0.0,  0.0,

    # Face Direita (Normal: 1, 0, 0)
     0.5,  0.5,  0.5,   1.0,  0.0,  0.0,
     0.5,  0.5, -0.5,   1.0,  0.0,  0.0,
     0.5, -0.5, -0.5,   1.0,  0.0,  0.0,
     0.5, -0.5, -0.5,   1.0,  0.0,  0.0,
     0.5, -0.5,  0.5,   1.0,  0.0,  0.0,
     0.5,  0.5,  0.5,   1.0,  0.0,  0.0,

    # Face Inferior (Normal: 0, -1, 0)
    -0.5, -0.5, -0.5,   0.0, -1.0,  0.0,
     0.5, -0.5, -0.5,   0.0, -1.0,  0.0,
     0.5, -0.5,  0.5,   0.0, -1.0,  0.0,
     0.5, -0.5,  0.5,   0.0, -1.0,  0.0,
    -0.5, -0.5,  0.5,   0.0, -1.0,  0.0,
    -0.5, -0.5, -0.5,   0.0, -1.0,  0.0,

    # Face Superior (Normal: 0, 1, 0)
    -0.5,  0.5, -0.5,   0.0,  1.0,  0.0,
     0.5,  0.5, -0.5,   0.0,  1.0,  0.0,
     0.5,  0.5,  0.5,   0.0,  1.0,  0.0,
     0.5,  0.5,  0.5,   0.0,  1.0,  0.0,
    -0.5,  0.5,  0.5,   0.0,  1.0,  0.0,
    -0.5,  0.5, -0.5,   0.0,  1.0,  0.0
], dtype=np.float32)


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    largura, altura = 800, 600
    window = glfw.create_window(largura, altura, "Cubo 3D - OpenGL 3.3+ Core (MVP + Phong)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST) # Essencial em 3D para o Z-Buffer ocultar faces traseiras

    shader = criar_programa(VERTEX_SHADER_SRC, FRAGMENT_SHADER_SRC)

    # Configuração do VAO e VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cubo_vertices.nbytes, cubo_vertices, GL_STATIC_DRAW)

    stride = 6 * cubo_vertices.itemsize # 6 floats por vértice (24 bytes)

    # Atributo 0: Posição (X, Y, Z)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Atributo 1: Normal (NX, NY, NZ)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * cubo_vertices.itemsize))
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    # Busca as localizações das variáveis uniform uma única vez (boa prática de performance)
    loc_model = glGetUniformLocation(shader, "model")
    loc_view = glGetUniformLocation(shader, "view")
    loc_proj = glGetUniformLocation(shader, "projection")
    loc_light_pos = glGetUniformLocation(shader, "lightPos")
    loc_view_pos = glGetUniformLocation(shader, "viewPos")
    loc_light_color = glGetUniformLocation(shader, "lightColor")
    loc_obj_color = glGetUniformLocation(shader, "objectColor")

    # Configuração estática da câmera e perspectiva
    pos_camera = np.array([0.0, 1.5, 3.5], dtype=np.float32)
    alvo_camera = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    up_camera = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    view = matriz_look_at(pos_camera, alvo_camera, up_camera)
    projection = matriz_perspectiva(45.0, largura / altura, 0.1, 100.0)

    while not glfw.window_should_close(window):
        glClearColor(0.1, 0.1, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        # Matriz Model dinâmica: gira o cubo nos eixos Y e X conforme o tempo
        t = glfw.get_time()
        model = matriz_rotacao_y(t) @ matriz_rotacao_x(t * 0.6)

        # Envia uma matriz 4x4 para o shader.
        # Parâmetros: localização, quantidade (1), transpor (GL_TRUE pois NumPy é row-major e GLSL é column-major), dados
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view)
        glUniformMatrix4fv(loc_proj, 1, GL_TRUE, projection)

        # Envia um vetor vec3 (3 floats) para o Fragment Shader
        glUniform3f(loc_light_pos, 2.0, 2.0, 2.5)   # Luz posicionada acima e à direita
        glUniform3f(loc_view_pos, *pos_camera)      # Posição da câmera para o brilho especular
        glUniform3f(loc_light_color, 1.0, 1.0, 1.0) # Luz branca
        glUniform3f(loc_obj_color, 0.9, 0.35, 0.2)  # Cubo laranja/coral

        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36) # Desenha os 36 vértices do cubo

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader)
    glfw.terminate()

if __name__ == "__main__":
    main()