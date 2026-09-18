import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

is_dragging = False
last_x, last_y = 0.0, 0.0
rot_x, rot_y = 30.0, 45.0 # Ângulos iniciais para o cubo não nascer de frente
sensibilidade = 0.5       # Multiplicador para a velocidade do giro

def mouse_button_callback(window, button, action, mods):
    """Acordada pelo SO quando um botão do mouse é clicado ou solto"""
    global is_dragging, last_x, last_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            is_dragging = True
            # Captura a posição exata onde o arraste começou
            last_x, last_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            is_dragging = False

def cursor_position_callback(window, xpos, ypos):
    """Acordada pelo SO quando o mouse se move na janela"""
    global is_dragging, last_x, last_y, rot_x, rot_y
    if is_dragging:
        # Calcula a variação de movimento (Delta) desde o último frame
        dx = xpos - last_x
        dy = ypos - last_y
        
        # Atualiza a última posição conhecida
        last_x = xpos
        last_y = ypos
        
        # Mapeamento Cruzado (X da tela -> Eixo Y do mundo; Y da tela -> Eixo X do mundo)
        rot_y += dx * sensibilidade
        rot_x += dy * sensibilidade

# SHADERS (Código compilado para a GPU)
VERTEX_SHADER_CODIGO = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 vertexColor;
uniform mat4 MVP;

void main() {
    gl_Position = MVP * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""

FRAGMENT_SHADER_CODIGO = """
#version 330 core
in vec3 vertexColor;
out vec4 FragColor;

void main() {
    FragColor = vec4(vertexColor, 1.0);
}
"""

def criar_matriz_perspectiva(fov_graus, aspecto, perto, longe):
    f = 1.0 / np.tan(np.radians(fov_graus) / 2.0)
    matriz = np.zeros((4, 4), dtype=np.float32)
    matriz[0, 0] = f / aspecto
    matriz[1, 1] = f
    matriz[2, 2] = (longe + perto) / (perto - longe)
    matriz[2, 3] = (2.0 * longe * perto) / (perto - longe)
    matriz[3, 2] = -1.0
    return matriz

def criar_matriz_translacao(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def criar_matriz_rotacao_y(graus):
    c, s = np.cos(np.radians(graus)), np.sin(np.radians(graus))
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ], dtype=np.float32)

def criar_matriz_rotacao_x(graus):
    c, s = np.cos(np.radians(graus)), np.sin(np.radians(graus))
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ], dtype=np.float32)

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(800, 600, "Cubo Interativo: Arraste o Mouse", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)

    # CALLBACKS DE HARDWARE

    glfw.set_mouse_button_callback(janela, mouse_button_callback)
    glfw.set_cursor_pos_callback(janela, cursor_position_callback)

    glEnable(GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER_CODIGO, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER_CODIGO, GL_FRAGMENT_SHADER)
    )

    vertices = np.array([
        -0.5, -0.5, -0.5,   0.0, 0.0, 0.0,
         0.5, -0.5, -0.5,   1.0, 0.0, 0.0,
         0.5,  0.5, -0.5,   1.0, 1.0, 0.0,
        -0.5,  0.5, -0.5,   0.0, 1.0, 0.0,
        -0.5, -0.5,  0.5,   0.0, 0.0, 1.0,
         0.5, -0.5,  0.5,   1.0, 0.0, 1.0,
         0.5,  0.5,  0.5,   1.0, 1.0, 1.0,
        -0.5,  0.5,  0.5,   0.0, 1.0, 1.0
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        7, 6, 2, 2, 3, 7,
        5, 1, 2, 2, 6, 5,
        4, 0, 3, 3, 7, 4
    ], dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    passo = 6 * vertices.itemsize
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    matriz_projecao = criar_matriz_perspectiva(45.0, 800.0/600.0, 0.1, 100.0)
    matriz_view = criar_matriz_translacao(0, 0, -3.0) 
    loc_mvp = glGetUniformLocation(shader, "MVP")

    while not glfw.window_should_close(janela):
        glfw.poll_events() # Processa os inputs de hardware (Callbacks)
        
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)


        matriz_model = criar_matriz_rotacao_x(rot_x) @ criar_matriz_rotacao_y(rot_y)
        MVP = matriz_projecao @ matriz_view @ matriz_model
        
        MVP_transposta = np.ascontiguousarray(MVP.T, dtype=np.float32)
        glUniformMatrix4fv(loc_mvp, 1, GL_FALSE, MVP_transposta)

        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()