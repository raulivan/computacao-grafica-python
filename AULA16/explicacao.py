from OpenGL.GL import *
import numpy as np
# definindo a geometria do triângulo SRO
vertices = np.array([
    -0.5, -0.5,  # Vértice Esquerdo
        0.5, -0.5,  # Vértice Direito
        0.0,  0.5   # Vértice Topo
], dtype=np.float32)

# cria a Pasta (VAO) e o transporte (VBO)
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

# abre a Pasta para começar a armazenar (Bind)
glBindVertexArray(VAO)

# transporta os Bytes na memória
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# anota na Pasta 
# Conecte os dados começando do byte 0 à Porta 0 do Shader.
# Leia de 2 em 2 floats.
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * vertices.itemsize, ctypes.c_void_p(0))

# anota na Pasta:
# Ligue a Porta 0
glEnableVertexAttribArray(0)

# terminei, fecha a pasta
glBindVertexArray(0)