import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

modo_perspectiva = True

def callback_teclado(window, key, scancode, action, mods):
    global modo_perspectiva
    # Quando o ESPAÇO for pressionado
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        modo_perspectiva = not modo_perspectiva
        modo = "PERSPECTIVA (Olho Humano)" if modo_perspectiva else "ORTOGRÁFICA (matemática)"
        print(f"Câmera alterada para: {modo}")
    # Frim callback_teclado

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 MVP;

void main() {
    gl_Position = MVP * vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
uniform vec3 cor_cubo;

void main() {
    FragColor = vec4(cor_cubo, 1.0);
}
"""

def matriz_perspectiva(fov_graus, aspecto, perto, longe):
    """Visão humana, o tamanho depende da distância (Z)"""
    f = 1.0 / np.tan(np.radians(fov_graus) / 2.0)
    m = np.zeros((4, 4), dtype=np.float32)
    m[0,0] = f / aspecto
    m[1,1] = f
    m[2,2] = (longe + perto) / (perto - longe)
    m[2,3] = (2.0 * longe * perto) / (perto - longe)
    m[3,2] = -1.0 # joga o Z para o W!
    return m

def matriz_ortografica(esquerda, direita, base, topo, perto, longe):
    """Visão matemática,mapeamento linear. Tamanho constante."""
    m = np.zeros((4, 4), dtype=np.float32)
    m[0,0] = 2.0 / (direita - esquerda)
    m[1,1] = 2.0 / (topo - base)
    m[2,2] = -2.0 / (longe - perto)
    m[0,3] = -(direita + esquerda) / (direita - esquerda)
    m[1,3] = -(topo + base) / (topo - base)
    m[2,3] = -(longe + perto) / (longe - perto)
    m[3,3] = 1.0 # O W continua 1.0.
    return m

def matriz_translacao(x, y, z): 
    return np.array([
        [1,0,0,x], 
        [0,1,0,y], 
        [0,0,1,z], 
        [0,0,0,1]
    ], dtype=np.float32)

def matriz_rotacao_y(g): 
    c,s = np.cos(np.radians(g)), np.sin(np.radians(g))
    return np.array([
        [c,0,s,0], 
        [0,1,0,0], 
        [-s,0,c,0], 
        [0,0,0,1]
    ], dtype=np.float32)


def main():
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(800, 600, "Projeções Geométricas - Pressione ESPAÇO", None, None)
    if not janela: return glfw.terminate()
    glfw.make_context_current(janela)
    glfw.swap_interval(1)
    glEnable(GL_DEPTH_TEST)
    
    # Registra o gatilho do teclado
    glfw.set_key_callback(janela, callback_teclado)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Cubo 
    vertices = np.array([
        # Frontal
        -0.5,-0.5, 0.5,   
         0.5,-0.5, 0.5,   
         0.5, 0.5, 0.5,  
         -0.5, 0.5, 0.5,
        # Traseira
        -0.5,-0.5,-0.5,   
         0.5,-0.5,-0.5,   
         0.5, 0.5,-0.5,  
        -0.5, 0.5,-0.5  
    ], dtype=np.float32)

    # 12 triângulos
    indices = np.array([
        0,1,2, 
        2,3,0,  
        1,5,6, 
        6,2,1,  
        5,4,7, 
        7,6,5,  
        4,0,3, 
        3,7,4,  
        3,2,6, 
        6,7,3,  
        4,5,1, 
        1,0,4
    ], dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO); 
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO); 
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    # Ponteiros dos Uniforms
    loc_mvp = glGetUniformLocation(shader, "MVP")
    loc_cor = glGetUniformLocation(shader, "cor_cubo")

    # Move a câmera para trás
    view = matriz_translacao(0, 0, -2.0) 

    print("inicio...")
    print("pressione a tecla ESPAÇO para alternar a Projeção...")

    rot_y = 0.0

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader)

        if modo_perspectiva:
            projecao = matriz_perspectiva(60.0, 800/600, 0.1, 100.0)
        else:
            # Os parâmetros limitam o que a tela consegue ver fisicamente
            projecao = matriz_ortografica(-4.0, 4.0, -3.0, 3.0, 0.1, 100.0)

        rot_y += 0.5 # girar lento
        
        distancias = [-2.0, -5.0, -8.0, -11.0, -14.0]
        cores = [
            [1.0, 0.3, 0.3], # Vermelho (Mais perto)
            [0.3, 1.0, 0.3], # Verde
            [0.3, 0.3, 1.0], # Azul
            [1.0, 1.0, 0.3], # Amarelo
            [1.0, 0.5, 0.0]  # Laranja (Mais longe)
        ]

        i = 0 #configuração da visão

        glBindVertexArray(VAO)

        # Posiciona o cubo no Eixo Z
        model = matriz_translacao(0.0, 0.0, distancias[i]) @ matriz_rotacao_y(rot_y)
        MVP = projecao @ view @ model
        
        # Envia a matriz e a cor específica do cubo
        glUniformMatrix4fv(loc_mvp, 1, GL_FALSE, np.ascontiguousarray(MVP.T, dtype=np.float32))
        glUniform3f(loc_cor, cores[i][0], cores[i][1], cores[i][2])

        
        # desenhar a geometria
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(janela)
        # fim while

    glfw.terminate()
    # fim main

if __name__ == "__main__":
    main()