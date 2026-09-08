import numpy as np
import matplotlib.pyplot as plt

def desenhar_cenario(ax, matriz_trans, titulo, cor_trans, label_trans, matriz_vertices):
    # grade e eixos do plano Cartesianos
    ax.set_title(titulo, fontweight='bold', fontsize=12)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 8)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_aspect('equal')

    # retângulo Original (Azul Tracejado)
    x_orig, y_orig = matriz_vertices[0, :], matriz_vertices[1, :]
    ax.plot(x_orig, y_orig, color='blue', linestyle='--', 
            marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)

    # geometria Transformada (Cisilhada)
    x_trans, y_trans = matriz_trans[0, :], matriz_trans[1, :]
    ax.plot(x_trans, y_trans, color=cor_trans, linestyle='-', 
            marker='s', linewidth=2, label=label_trans)
    ax.fill(x_trans, y_trans, color=cor_trans, alpha=0.3)

    # legendas
    rotulos = ['A', 'B', 'C', 'D']
    for i in range(4): # 4 vértices
        # ponto superior/inferior para mostrar o deslocamento
        ax.annotate(f"{rotulos[i]}'({x_trans[i]:.1f}, {y_trans[i]:.1f})", 
                    (x_trans[i], y_trans[i]), xytext=(5, 5), 
                    textcoords="offset points", color=cor_trans, fontweight='bold')
        
        # desenha a seta cinza mostrando o empurrão do cisalhamento
        if x_orig[i] != x_trans[i] or y_orig[i] != y_trans[i]:
            ax.annotate("", xy=(x_trans[i], y_trans[i]), xytext=(x_orig[i], y_orig[i]),
                        arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, ls="--"))

    ax.legend(loc='upper left')

    # Fim da função desenhar_cenario

def plotar_cisalhamento():
    print("=== Cisalhamento (Shear) 2D ===\n")

    # geometria Original (Retângulo)
    # Vértices: A(0,0), B(4,0), C(4,3), D(0,3) e fechamento em A(0,0)
    matriz_vertices = np.array([
        [0, 4, 4, 0, 0], # Eixo X
        [0, 0, 3, 3, 0], # Eixo Y
        [1, 1, 1, 1, 1]  # Coordenada Homogênea (W)
    ], dtype=np.float32)

    # fatores de Cisalhamento
    sh_x = 1.5 # Para cada 1 unidade em Y, o X será empurrado 1.5 unidades
    sh_y = 1.0 # Para cada 1 unidade em X, o Y será empurrado 1.0 unidade

    M_Cisalhamento_X = np.array([
        [1, sh_x, 0],
        [0, 1,    0],
        [0, 0,    1]
    ])

    M_Cisalhamento_Y = np.array([
        [1,    0, 0],
        [sh_y, 1, 0],
        [0,    0, 1]
    ])

    # multiplicação de matrizes
    trans_X = M_Cisalhamento_X @ matriz_vertices
    trans_Y = M_Cisalhamento_Y @ matriz_vertices

    # renderização (1 Linha, 2 Colunas)
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # desenhando
    desenhar_cenario(axs[0], trans_X, f"1. Cisalhamento em X (Sh_x = {sh_x})", 
                     'purple', 'Cisalhado em X',matriz_vertices)
    desenhar_cenario(axs[1], trans_Y, f"2. Cisalhamento em Y (Sh_y = {sh_y})", 
                     'orange', 'Cisalhado em Y',matriz_vertices)

    plt.tight_layout()
    print("Renderizando o Cisalhamento...")
    plt.show()
    # Fim da função plotar_cisalhamento

if __name__ == "__main__":
    plotar_cisalhamento()