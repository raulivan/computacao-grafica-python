import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from PIL import Image

#  SHADERS com Suporte a Textura
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;     // Porta 0: Geometria (X, Y, Z)
layout (location = 1) in vec2 aTexCord; // Porta 1: Mapeamento (U, V)

out vec2 TexCord; // Passa o UV para o Fragment Shader
uniform mat4 MVP; // Matriz Mestre

void main() {
    gl_Position = MVP * vec4(aPos, 1.0);
    TexCord = aTexCord;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 TexCord;
out vec4 FragColor;

// Slot de memória da GPU onde a imagem estará vinculada
uniform sampler2D textura_bloco;

void main() {
    // Lê a cor exata do pixel da textura naquela coordenada UV
    FragColor = texture(textura_bloco, TexCord);
}
"""

def carregar_textura_do_disco(caminho_arquivo):
    print(f"[*] Tentando ler a imagem: {caminho_arquivo}...")
    
    try:

        imagem = Image.open(caminho_arquivo)
        imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

        imagem_dados = imagem.convert("RGBA").tobytes()
        largura, altura = imagem.size
        print(f"    [+] Sucesso! Resolução: {largura}x{altura}")
        
    except FileNotFoundError:
        print(" deu erro ...")
        largura, altura = 2, 2
        imagem_dados = np.array([
            255, 0, 255, 255,   0, 0, 0, 255, # Linha inferior (Rosa, Preto)
            0, 0, 0, 255,       255, 0, 255, 255  # Linha superior (Preto, Rosa)
        ], dtype=np.uint8).tobytes()

    textura_id = glGenTextures(1)
    
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, imagem_dados)
    
    glBindTexture(GL_TEXTURE_2D, 0)

    return textura_id

def matriz_perspectiva(fov, aspecto, perto, longe):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    m = np.zeros((4, 4), dtype=np.float32)
    m[0,0] = f / aspecto; m[1,1] = f; m[2,2] = (longe + perto) / (perto - longe)
    m[2,3] = (2.0 * longe * perto) / (perto - longe); m[3,2] = -1.0
    return m

def matriz_translacao(x, y, z): 
    return np.array([[1,0,0,x], [0,1,0,y], [0,0,1,z], [0,0,0,1]], dtype=np.float32)

def matriz_rotacao_x(g): 
    c,s = np.cos(np.radians(g)), np.sin(np.radians(g)); 
    return np.array([[1,0,0,0], [0,c,-s,0], [0,s,c,0], [0,0,0,1]], dtype=np.float32)

def matriz_rotacao_y(g): 
    c,s = np.cos(np.radians(g)), np.sin(np.radians(g)); 
    return np.array([[c,0,s,0], [0,1,0,0], [-s,0,c,0], [0,0,0,1]], dtype=np.float32)

def main():
    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(800, 600, "Cubo Minecraft: Textura de Arquivo e Teclado", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)
    glfw.swap_interval(1) # VSync
    glEnable(GL_DEPTH_TEST) # Z-Buffer ativado (esconde a face de trás)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # 24 Vértices (4 por face) 
    # Formato: [ X, Y, Z,   U, V ]
    vertices = np.array([
        # Face Frontal (Z = 0.5)
        -0.5, -0.5,  0.5,   0.0, 0.0, # Canto Inferior Esquerdo
         0.5, -0.5,  0.5,   1.0, 0.0, # Canto Inferior Direito
         0.5,  0.5,  0.5,   1.0, 1.0, # Canto Superior Direito
        -0.5,  0.5,  0.5,   0.0, 1.0, # Canto Superior Esquerdo

        # Face Traseira (Z = -0.5)
        -0.5, -0.5, -0.5,   1.0, 0.0,
         0.5, -0.5, -0.5,   0.0, 0.0,
         0.5,  0.5, -0.5,   0.0, 1.0,
        -0.5,  0.5, -0.5,   1.0, 1.0,

        # Face Esquerda (X = -0.5)
        -0.5, -0.5, -0.5,   0.0, 0.0,
        -0.5, -0.5,  0.5,   1.0, 0.0,
        -0.5,  0.5,  0.5,   1.0, 1.0,
        -0.5,  0.5, -0.5,   0.0, 1.0,

        # Face Direita (X = 0.5)
         0.5, -0.5, -0.5,   1.0, 0.0,
         0.5, -0.5,  0.5,   0.0, 0.0,
         0.5,  0.5,  0.5,   0.0, 1.0,
         0.5,  0.5, -0.5,   1.0, 1.0,

        # Face Superior (Y = 0.5)
        -0.5,  0.5, -0.5,   0.0, 1.0,
         0.5,  0.5, -0.5,   1.0, 1.0,
         0.5,  0.5,  0.5,   1.0, 0.0,
        -0.5,  0.5,  0.5,   0.0, 0.0,

        # Face Inferior (Y = -0.5)
        -0.5, -0.5, -0.5,   0.0, 0.0,
         0.5, -0.5, -0.5,   1.0, 0.0,
         0.5, -0.5,  0.5,   1.0, 1.0,
        -0.5, -0.5,  0.5,   0.0, 1.0,
    ], dtype=np.float32)

    # Conectando os vértices em triângulos 
    indices = np.array([
        0, 1, 2,  2, 3, 0,       # Frontal
        4, 5, 6,  6, 7, 4,       # Traseira
        8, 9, 10, 10, 11, 8,     # Esquerda
        12, 13, 14, 14, 15, 12,  # Direita
        16, 17, 18, 18, 19, 16,  # Superior
        20, 21, 22, 22, 23, 20   # Inferior
    ], dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)


    passo = 5 * vertices.itemsize
    
    # Atributo 0: Geometria (3 floats). Offset = 0.
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Atributo 1: Textura UV (2 floats). Offset = Pule os 3 primeiros floats.
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, passo, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0) 

    matriz_proj = matriz_perspectiva(45.0, 800/600, 0.1, 100.0)
    matriz_view = matriz_translacao(0, 0, -3.0) 
    
    # Lendo o arquivo do disco! 
    textura_id = carregar_textura_do_disco("C:\workspace\computacao-grafica-python\madeira.jpeg")

    loc_mvp = glGetUniformLocation(shader, "MVP")
    loc_tex = glGetUniformLocation(shader, "textura_bloco")

    rot_x, rot_y = 25.0, -30.0
    velocidade = 2.0

    print("[*] Tudo pronto. Use as Setas do Teclado para explorar o bloco 3D.")

    while not glfw.window_should_close(janela):
        glfw.poll_events()

        if glfw.get_key(janela, glfw.KEY_RIGHT) == glfw.PRESS: rot_y += velocidade
        if glfw.get_key(janela, glfw.KEY_LEFT) == glfw.PRESS:  rot_y -= velocidade
        if glfw.get_key(janela, glfw.KEY_DOWN) == glfw.PRESS:  rot_x += velocidade
        if glfw.get_key(janela, glfw.KEY_UP) == glfw.PRESS:    rot_x -= velocidade

        glClearColor(0.5, 0.8, 1.0, 1.0) 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        # Atualizando a Matriz MVP
        matriz_model = matriz_rotacao_x(rot_x) @ matriz_rotacao_y(rot_y)
        MVP = matriz_proj @ matriz_view @ matriz_model
        glUniformMatrix4fv(loc_mvp, 1, GL_FALSE, np.ascontiguousarray(MVP.T, dtype=np.float32))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textura_id)
        glUniform1i(loc_tex, 0) 

        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()