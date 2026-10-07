import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

# Camera
camera_pos = np.array(
    [0.0, 1.0, 5.0]
, dtype=np.float32) # Olho (Eye)
camera_front = np.array(
    [0.0, 0.0, -1.0]
, dtype=np.float32) # Alvo (Direção)

camera_up = np.array(
    [0.0, 1.0, 0.0]
, dtype=np.float32) # Cima (Up)

# Delta Time (FPS)
tempo_anterior = 0.0

# Loo)

# rotação Esquerda/Direita, começa em -90 para olhar pro -Z
yaw = -90.0
# rotação Cima/Baixo
pitch = 0.0   
# Centro da tela (800x600)
ultimo_x = 400.0; ultimo_y = 300.0 
primeiro_mouse = True

def callback_mouse(window, xpos, ypos):
    global yaw, pitch, ultimo_x, ultimo_y, primeiro_mouse, camera_front
    
    if primeiro_mouse:
        ultimo_x = xpos; ultimo_y = ypos
        primeiro_mouse = False

    x_offset = xpos - ultimo_x
    #Windows cresce para baixo, e o OpenGL para cima
    y_offset = ultimo_y - ypos 
    ultimo_x = xpos; ultimo_y = ypos

    sensibilidade = 0.1
    yaw += x_offset * sensibilidade
    pitch += y_offset * sensibilidade

    # Trava do Pescoço, pra nãoquebrar a espinha)
    if pitch > 89.0: pitch = 89.0
    if pitch < -89.0: pitch = -89.0

    # converte Ângulos de Euler (Yaw/Pitch) em um Vetor de Direção (Frente)
    frente_x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
    frente_y = math.sin(math.radians(pitch))
    frente_z = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    
    vetor_frente = np.array([frente_x, frente_y, frente_z])
     # Normaliza (tamanho 1)
    camera_front = vetor_frente / np.linalg.norm(vetor_frente)

def processar_teclado(janela, delta_time):
    global camera_pos, camera_front, camera_up
    # Move 2.5 unidades por segundo
    velocidade = 2.5 * delta_time 

    # 'W' move o mundo para trás 
    if glfw.get_key(janela, glfw.KEY_W) == glfw.PRESS:
        camera_pos += velocidade * camera_front
    # 'S' move o mundo para frente
    if glfw.get_key(janela, glfw.KEY_S) == glfw.PRESS:
        camera_pos -= velocidade * camera_front
        
    # 'A' e 'D' (Esquerda/Direita)
    if glfw.get_key(janela, glfw.KEY_A) == glfw.PRESS:
        vetor_direita = np.cross(camera_front, camera_up)
        vetor_direita = vetor_direita / np.linalg.norm(vetor_direita)
        camera_pos -= velocidade * vetor_direita
        
    if glfw.get_key(janela, glfw.KEY_D) == glfw.PRESS:
        vetor_direita = np.cross(camera_front, camera_up)
        vetor_direita = vetor_direita / np.linalg.norm(vetor_direita)
        camera_pos += velocidade * vetor_direita

def matriz_lookat(eye, target, up):
    # Z-axis: Para trás
    z_axis = eye - target
    z_axis = z_axis / np.linalg.norm(z_axis)
    
    # X-axis: Direita
    x_axis = np.cross(up, z_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    
    # Y-axis: Cima
    y_axis = np.cross(z_axis, x_axis)

    # matriz de Rotação e Translação combinada
    matriz = np.identity(4, dtype=np.float32)
    matriz[0, 0:3] = x_axis
    matriz[1, 0:3] = y_axis
    matriz[2, 0:3] = z_axis
    matriz[0, 3] = -np.dot(x_axis, eye)
    matriz[1, 3] = -np.dot(y_axis, eye)
    matriz[2, 3] = -np.dot(z_axis, eye)
    return matriz

def matriz_perspectiva(fov, aspecto, perto, longe):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    m = np.zeros((4, 4), dtype=np.float32)
    m[0,0] = f / aspecto
    m[1,1] = f 
    m[2,2] = (longe+perto)/(perto-longe)
    m[2,3] = (2.0*longe*perto)/(perto-longe); m[3,2] = -1.0
    return m

def matriz_translacao(x, y, z): 
    return np.array([
        [1,0,0,x], 
        [0,1,0,y], 
        [0,0,1,z], 
        [0,0,0,1]
    ], dtype=np.float32)

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
uniform vec3 corObj;
void main() { 
    FragColor = vec4(corObj, 1.0); 
}
"""

def main():
    global tempo_anterior
    
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(800, 600, "Câmera Virtual", None, None)
    if not janela: return glfw.terminate()
    glfw.make_context_current(janela)
    
    # trava o mouse dentro da janela e o deixa invisível
    glfw.set_input_mode(janela, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(janela, callback_mouse)
    
    glEnable(GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Cubo
    vertices = np.array([
        -0.5,-0.5,0.5, 
         0.5,-0.5,0.5, 
         0.5,0.5,0.5, 
        -0.5,0.5,0.5, 
        -0.5,-0.5,-0.5, 
        0.5,-0.5,-0.5, 
        0.5,0.5,-0.5, 
        -0.5,0.5,-0.5
    ], dtype=np.float32)

    indices = np.array([
        0,1,2, 2,3,0, 
        4,5,6, 6,7,4, 
        4,0,3, 3,7,4, 
        1,5,6, 6,2,1, 
        3,2,6, 6,7,3, 
        4,5,1, 1,0,4
    ], dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3*4, ctypes.c_void_p(0))
    
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    # gerar as posições de 25 cubos espalhados no chão para formar uma "cidade"
    posicoes_cubos = []
    for x in range(-2, 3):
        for z in range(-2, 3):
            # tipo 3 em 3 metros
            posicoes_cubos.append((x * 3.0, 0.0, z * 3.0))

    loc_mvp = glGetUniformLocation(shader, "MVP")
    loc_cor = glGetUniformLocation(shader, "corObj")

    print("Iniciando Câmera...")
    print("Mova o Mouse para olhar e use W,A,S,D para andar.")
    print(" ESC para sair.")

    while not glfw.window_should_close(janela):
        # Delta Time
        tempo_atual = glfw.get_time()
        delta_time = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual

        # ESC, fecha
        if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(janela, True)

        processar_teclado(janela, delta_time)
        glfw.poll_events()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader)

        # Matriz LookAt e Perspectiva
        projecao = matriz_perspectiva(45.0, 800/600, 0.1, 100.0)
        
        # Recalcula a Matriz de View a CADA quadro
        alvo = camera_pos + camera_front 
        view = matriz_lookat(camera_pos, alvo, camera_up)

        # desenha a "Cidade" de 25 cubos
        glBindVertexArray(VAO)
        for i, pos in enumerate(posicoes_cubos):
            model = matriz_translacao(pos[0], pos[1], pos[2])
            MVP = projecao @ view @ model
            
            glUniformMatrix4fv(loc_mvp, 1, GL_FALSE, np.ascontiguousarray(MVP.T, dtype=np.float32))
            
            r = (pos[0] + 6.0) / 12.0
            b = (pos[2] + 6.0) / 12.0
            glUniform3f(loc_cor, r, 0.5, b)
            
            glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()