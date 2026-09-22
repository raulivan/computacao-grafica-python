import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# SHADERS preparados para textura
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;     // PORTA 0: Recebe X, Y, Z
layout (location = 1) in vec2 aTexCord; // PORTA 1: Recebe U, V

out vec2 TexCord; // Variável para enviar o UV para o Fragment Shader

void main() {
    gl_Position = vec4(aPos, 1.0);
    TexCord = aTexCord; // Apenas repassa a coordenada UV
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 TexCord; // Recebe o UV interpolado da GPU
out vec4 FragColor;

// 'sampler2D' é um tipo especial do GLSL que acessa a memória de imagem da Placa de Vídeo
uniform sampler2D textura_xadrez; 

void main() {
    // A função texture() lê a cor exata do pixel da imagem naquela coordenada UV
    FragColor = texture(textura_xadrez, TexCord);
}
"""

# Um método que gerar uma imagem de tabuleiro de xadrez
def criar_imagem_xadrez():
    """Gera uma imagem de tabuleiro de xadrez 256x256 pixels em memória (RGB)"""
    tamanho = 256
    img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
    # criar o xadrez preto e branco
    for i in range(tamanho):
        for j in range(tamanho):
            # o operador // é a divisão inteira.
            # o operador % calcula o resto da divisão.
            # verifica se a soma é par ou ímpar.
            if (i // 32 + j // 32) % 2 == 0:
                img[i, j] = [255, 255, 255] # Branco
            else:
                img[i, j] = [0, 0, 0]       # Preto
    return img, tamanho, tamanho
    # Fim do método


def main():
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(800, 600, "Mapeamento UV de Texturas", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # QUADRADO SRO
    # Formato: [X, Y, Z,    U, V]
    vertices = np.array([
         0.5,  0.5, 0.0,    1.0, 1.0, # 0: Topo Direito    (UV: Canto Superior Direito da Imagem)
         0.5, -0.5, 0.0,    1.0, 0.0, # 1: Base Direita    (UV: Canto Inferior Direito)
        -0.5, -0.5, 0.0,    0.0, 0.0, # 2: Base Esquerda   (UV: Canto Inferior Esquerdo)
        -0.5,  0.5, 0.0,    0.0, 1.0  # 3: Topo Esquerdo   (UV: Canto Superior Esquerdo)
    ], dtype=np.float32)

    indices = np.array([0, 1, 3,  1, 2, 3], dtype=np.uint32)

    
    # glGenVertexArrays(1) -> O número 1 significa QUANTIDADE. 
    # a placa de vídeo, gere um ID numérico livre para eu usar como VAO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1) # Gere 1 ID para VBO
    EBO = glGenBuffers(1) # Gere 1 ID para EBO

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # cálculo do passo da memória: 
    # cada linha tem 5 floats (X,Y,Z, U,V). 5 * 4 bytes = 20 bytes.
    passo = 5 * vertices.itemsize

    # ATRIBUTO 0: POSIÇÃO GEOMÉTRICA (X, Y, Z)
    # Parâmetro 1 (0): É a Porta do Vertex Shader (layout location = 0)
    # Parâmetro 2 (3): lê 3 valores (X, Y, Z)
    # Parâmetro 6 (0): Offset. Quantos bytes pular para começar a ler
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(0))
    # ativa a Porta 0 do Shader
    glEnableVertexAttribArray(0) 

    # ATRIBUTO 1: COORDENADA DE TEXTURA (U, V)
    # Parâmetro 1 (1): É a Porta do Vertex Shader (layout location = 1)
    # Parâmetro 2 (2): lê 2 valores (U, V)
    # Parâmetro 6 (3 * 4 bytes): Offset. Pule o X,Y,Z (3 floats) para achar o U e V.
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(3 * vertices.itemsize))
    # ativa a Porta 1 do Shader
    glEnableVertexAttribArray(1)

    # Desvincula o VAO passando 0 (0 = Nulo/Desligado)
    glBindVertexArray(0)

    # definindo a textura
    # imagem gerada no Python (Matriz RGB)
    imagem_dados, largura, altura = criar_imagem_xadrez()

    # glGenTextures(1) -> Gere um ID numérico livre para Textura
    textura_id = glGenTextures(1)
    
    # liga a Textura 
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # configuração da textura
    # Como a imagem se comporta se o UV passar de 1.0? 
    # GL_REPEAT faz ela se repetir (como papel de parede)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Filtro: como a imagem se comporta ao darmos zoom? 
    # GL_NEAREST mantém o pixel quadriculado (estilo Minecraft)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # envia os bytes da imagem (RAM) para a Placa de Vídeo (VRAM)
    # o parâmetro '0' no meio: Level of Detail (LOD) ou Mipmap. 0 significa a imagem base principal.
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, imagem_dados)

    # desvincula a textura (Passando 0)
    glBindTexture(GL_TEXTURE_2D, 0)

    print("quadrado com mapeamento UV.")

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader)

        # a placa de vídeo tem várias portas físicas (Slots) para texturas simultâneas.
        # GL_TEXTURE0 é o Slot Físico número 0. 
        # existe o GL_TEXTURE1, 2, etc até 31.
        glActiveTexture(GL_TEXTURE0)
        # Coloccolocaamos a nossa textura xadrez no Slot Físico 0
        glBindTexture(GL_TEXTURE_2D, textura_id)

        # notificar o Shader: o sampler2D deve ler a imagem que está no Slot 0
        loc_textura = glGetUniformLocation(shader, "textura_xadrez")
        # "...1i" = envie 1 valor Inteiro (o número 0, referente ao Slot)
        glUniform1i(loc_textura, 0) 

        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(janela)
        # fim do while

    glfw.terminate()
    #Fim do main

if __name__ == "__main__":
    main()