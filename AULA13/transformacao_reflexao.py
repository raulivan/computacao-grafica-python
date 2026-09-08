import numpy as np
import matplotlib.pyplot as plt

# Essa função serve para desenhar em cada subplot (cada plano)
def desenhar_cenario(ax, matriz_trans, titulo, cor_trans, label_trans, matriz_vertices):
    # deixando os eixos centralizados
    ax.set_title(titulo, fontweight='bold', fontsize=12)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_xticks(np.arange(-10, 11, 2))
    ax.set_yticks(np.arange(-10, 11, 2))
    ax.set_aspect('equal')

    # triangulo o Original (Azul, sempre no 1º Quadrante)
    x_orig, y_orig = matriz_vertices[0, :], matriz_vertices[1, :]
    ax.plot(x_orig, y_orig, color='blue', linestyle='--',
             marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)

    # triangulo transformado
    x_trans, y_trans = matriz_trans[0, :], matriz_trans[1, :]
    ax.plot(x_trans, y_trans, color=cor_trans, linestyle='-', 
            marker='s', label=label_trans)
    ax.fill(x_trans, y_trans, color=cor_trans, alpha=0.3)

    # legendas
    ax.annotate(f"A(2, 2)", (x_orig[0], y_orig[0]), xytext=(5, 5), 
                textcoords="offset points", color='blue')
    ax.annotate(f"A'({x_trans[0]:.1f}, {y_trans[0]:.1f})", 
                (x_trans[0], y_trans[0]), xytext=(5, 5), 
                textcoords="offset points", color=cor_trans)
    
    ax.legend(loc='upper left', fontsize=9)
    # Fim da função desenhar_cenario
    
def plotar_reflexao():
    print("=== Reflexão ===\n")

    # Geometria Original
    # Triângulo: A(2,2), B(4,5), C(6,2) e fechamento A(2,2)
    matriz_vertices = np.array([
        [2, 4, 6, 2], # Eixo X
        [2, 5, 2, 2], # Eixo Y
        [1, 1, 1, 1]  # W
    ], dtype=np.float32)

    # Matrizes de Transformação
    
    # Reflexão no Eixo X (Inverte Y)
    M_RefX = np.array([
        [ 1,  0, 0],
        [ 0, -1, 0],
        [ 0,  0, 1]
    ])

    # Reflexão no Eixo Y (Inverte X)
    M_RefY = np.array([
        [-1,  0, 0],
        [ 0,  1, 0],
        [ 0,  0, 1]
    ])

    # Reflexão na Origem XY (Inverte ambos)
    M_RefXY = np.array([
        [-1,  0, 0],
        [ 0, -1, 0],
        [ 0,  0, 1]
    ])

    # Rotação de 60 graus
    theta = np.radians(60)
    c, s = np.cos(theta), np.sin(theta)
    M_Rot60 = np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

    # Agora, aplica as transformações
    trans_X  = M_RefX @ matriz_vertices
    trans_Y  = M_RefY @ matriz_vertices
    trans_XY = M_RefXY @ matriz_vertices
    
    # aplicar a rotação, pois da ter 
    # o mesmo resultado da reflexão em algunas casos
    trans_Rot = M_Rot60 @ matriz_vertices

    # ajustando a renderização (Grid 2x2)
    fig, axs = plt.subplots(2, 2, figsize=(14, 14))

    # colocar lado a lado na tela
    desenhar_cenario(axs[0, 0], trans_X, "1. Reflexão no Eixo X (Y invertido)",
                      'red', 'Refletido X', matriz_vertices)
    desenhar_cenario(axs[0, 1], trans_Y, "2. Reflexão no Eixo Y (X invertido)", 
                     'green', 'Refletido Y', matriz_vertices)
    desenhar_cenario(axs[1, 0], trans_XY, "3. Reflexão nos Eixos XY (Origem)", 
                     'purple', 'Refletido XY', matriz_vertices)
    desenhar_cenario(axs[1, 1], trans_Rot, "4. Rotação de 60º na Origem", 
                     'orange', 'Rotacionado 60º', matriz_vertices)

    plt.tight_layout()
    print("Renderizando Reflexões...")
    plt.show()
    # fim da função plotar_reflexao

if __name__ == "__main__":
    plotar_reflexao()