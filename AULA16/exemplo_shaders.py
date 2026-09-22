import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# VERTEX SHADER
# Pega as posições brutas da memória Vertex Buffer Object (Objeto de Buffer de Vértices)
# ou simplismente (VBO).  e as converte para Coordenadas Homogêneas
VERTEX_SHADER_CODIGO = """
#version 330 core
layout (location = 0) in vec2 aPos; // Recebe X e Y do Python (VBO)

uniform float u_tempo; // Recebe o tempo do Python

void main() {
    // O vértice vai contrair ou inflar baseado na função seno do tempo!
    float pulsacao = sin(u_tempo) * 0.2; 
    
    // gl_Position é uma variável nativa obrigatória (vec4: X, Y, Z, W)
    gl_Position = vec4(aPos.x + (aPos.x * pulsacao), 
                       aPos.y + (aPos.y * pulsacao), 
                       0.0, 1.0);
}
"""

# FRAGMENT SHADER
# Calcula a cor de um pixel específico na tela
FRAGMENT_SHADER_CODIGO = """
#version 330 core
out vec4 CorDoPixel; // Saída final para o monitor

uniform float u_tempo; // recebe o mesmo tempo aqui

void main() {
    // Usamos seno e cosseno para criar um RGB dinâmico
    // Normaliza para ficar entre 0.0 e 1.0
    float vermelho = (sin(u_tempo * 2.0) + 1.0) / 2.0; 
    float verde    = (cos(u_tempo * 1.5) + 1.0) / 2.0;
    float azul     = (sin(u_tempo * 3.0) + 1.0) / 2.0;
    
    // Pinta o pixel
    // O último 1.0 é o Alpha (Opacidade)
    CorDoPixel = vec4(vermelho, verde, azul, 1.0); 
}
"""

def main():
    print("Exemplo de usdo de Shaders...")
    
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(800, 600, "Shaders na prática", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)

    # pedindo à GPU para compilar o código em C
    programa_shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER_CODIGO, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER_CODIGO, GL_FRAGMENT_SHADER)
    )

    # definindo a geometria do triângulo SRO
    vertices = np.array([
        -0.5, -0.5,  # Vértice Esquerdo
         0.5, -0.5,  # Vértice Direito
         0.0,  0.5   # Vértice Topo
    ], dtype=np.float32)

    # Alocação Padrão de 
    # VBO (Vertex Buffer Object)/ VAO (Vertex Array Object )
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # definindo na GPU que cada vértice tem 2 floats (X e Y)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glBindVertexArray(0)

    # recuperando da GPU o endereço da variável 'u_tempo'"
    local_tempo = glGetUniformLocation(programa_shader, "u_tempo")

    print("calculando cores e tamanhos em tempo real...")

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        
        # limpa o frame
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # usa o shader
        glUseProgram(programa_shader)

        # recupera o tempo do SO em segundos
        tempo_atual = glfw.get_time()

        # passando os parâmetros
        # glUniform1f -> Passa um valor do tipo float
        glUniform1f(local_tempo, tempo_atual)

        # desenha
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(janela)
        # fim do loop

    glfw.terminate()
    # fim do método main

if __name__ == "__main__":
    main()