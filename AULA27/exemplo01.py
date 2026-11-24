import glfw
from OpenGL.GL import *
import numpy as np
import ctypes

# Roda uma vez para cada vértice do triângulo
VERTEX_SHADER_SRC = """
#version 330 core

// Atributos de entrada vindos do VBO (configurados pelo VAO)
layout (location = 0) in vec3 aPos;   // Posição (X, Y, Z)
layout (location = 1) in vec3 aColor; // Cor (R, G, B)

// Variável de saída: será interpolada e enviada ao Fragment Shader
out vec3 nossaCor;

// Uniform: valor enviado pela CPU (Python) a cada frame
uniform float angulo;

void main()
{
    // Rotação 2D simples no plano XY feita manualmente no shader
    float c = cos(angulo);
    float s = sin(angulo);
    vec2 posRotacionada = vec2(
        aPos.x * c - aPos.y * s,
        aPos.x * s + aPos.y * c
    );

    // gl_Position é a variável obrigatória de saída (Coordenadas Homogêneas: X, Y, Z, W)
    gl_Position = vec4(posRotacionada, aPos.z, 1.0);
    
    // Repassa a cor do vértice para o próximo estágio
    nossaCor = aColor;
}
"""

# Roda uma vez para cada pixel dentro do triângulo
FRAGMENT_SHADER_SRC = """
#version 330 core

// Recebe a cor já interpolada pelo hardware de rasterização
in vec3 nossaCor;

// Cor final que será pintada na tela (R, G, B, Alpha)
out vec4 FragColor;

void main()
{
    FragColor = vec4(nossaCor, 1.0);
}
"""

def compilar_shader(codigo_fonte, tipo_shader):
    # Cria um objeto shader vazio na GPU e retorna seu ID
    shader = glCreateShader(tipo_shader)
    
    # Anexa o código-fonte (string GLSL) ao objeto shader
    glShaderSource(shader, codigo_fonte)
    
    # Pede ao driver da placa de vídeo para compilar o GLSL
    glCompileShader(shader)
    
    # Verifica se houve erro de sintaxe no GLSL
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Erro ao compilar shader:\n{erro}")
    return shader

def criar_programa_shader(vertex_src, fragment_src):
    vs = compilar_shader(vertex_src, GL_VERTEX_SHADER)
    fs = compilar_shader(fragment_src, GL_FRAGMENT_SHADER)
    
    # Cria um "executável" completo de GPU que unirá os shaders
    programa = glCreateProgram()
    
    # Anexa os shaders compilados ao programa
    glAttachShader(programa, vs)
    glAttachShader(programa, fs)
    
    # Conecta as saídas (out) do Vertex às entradas (in) do Fragment
    glLinkProgram(programa)
    
    if not glGetProgramiv(programa, GL_LINK_STATUS):
        erro = glGetProgramInfoLog(programa).decode()
        raise RuntimeError(f"Erro ao linkar programa:\n{erro}")
        
    # liberar memória
    glDeleteShader(vs)
    glDeleteShader(fs)
    return programa

def main():
    if not glfw.init():
        return

    # Exige o OpenGL 3.3 Core Profile (desativa funções legadas)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "OpenGL 3.3+ Core Profile (GLSL)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Compila nosso pipeline programável
    shader_program = criar_programa_shader(VERTEX_SHADER_SRC, FRAGMENT_SHADER_SRC)

    # Dados intercalados (Interleaved): [X, Y, Z,  R, G, B] para cada vértice
    vertices = np.array([
        # Posição (X, Y, Z)    # Cor (R, G, B)
        -0.5, -0.5, 0.0,       1.0, 0.0, 0.0,  # Vértice Inferior Esquerdo (Vermelho)
         0.5, -0.5, 0.0,       0.0, 1.0, 0.0,  # Vértice Inferior Direito (Verde)
         0.0,  0.5, 0.0,       0.0, 0.0, 1.0   # Vértice Superior (Azul)
    ], dtype=np.float32)

    # Criação do VAO e VBO
    # Gera 1 ID para o VAO (o "manual de leitura" dos dados)
    VAO = glGenVertexArrays(1)
    # Gera 1 ID para o VBO (o buffer bruto na VRAM)
    VBO = glGenBuffers(1)

    # Ativa o VAO. Tudo o que configurar abaixo ficará salvo nele
    glBindVertexArray(VAO)

    # Ativa o VBO como o buffer de vértices atual (GL_ARRAY_BUFFER)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    
    # Copia os bytes do array NumPy (RAM) para o VBO (VRAM)
    # o GL_STATIC_DRAW avisa a GPU que esses dados não vão mudar todo frame
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # quantos bytes existem entre o início de um vértice e o início do próximo
    # 6 floats * 4 bytes cada = 24 bytes
    stride = 6 * vertices.itemsize

    # Ensina a GPU a ler o Atributo 0 (Posição: 3 floats, começa no byte 0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # Habilita o atributo de índice 0 no VAO
    glEnableVertexAttribArray(0)

    # Atributo 1 (Cor: 3 floats, começa após os 3 floats de posição = 12 bytes)
    offset_cor = ctypes.c_void_p(3 * vertices.itemsize)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, offset_cor)
    glEnableVertexAttribArray(1)

    # Desvincula o VAO por segurança (boas práticas)
    glBindVertexArray(0)

    # Busca o "endereço" da variável uniform 'angulo' dentro do shader
    loc_angulo = glGetUniformLocation(shader_program, "angulo")

    while not glfw.window_should_close(window):
        # Define a cor de fundo (Cinza escuro) e limpa a tela
        glClearColor(0.15, 0.15, 0.18, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Ativa o nosso conjunto de Shaders na GPU
        glUseProgram(shader_program)

        # Envia o tempo atual da GLFW como ângulo em radianos para o Vertex Shader
        # Envia 1 único float para uma variável uniform
        tempo = glfw.get_time()
        glUniform1f(loc_angulo, tempo)

        # Ativa o VAO (que já sabe qual VBO usar e como ler os atributos)
        glBindVertexArray(VAO)
        
        # Comanda a GPU a desenhar triângulos usando 3 vértices a partir do índice 0
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Limpeza da memória de vídeo ao encerrar
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)
    glfw.terminate()

if __name__ == "__main__":
    main()