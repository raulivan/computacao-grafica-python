import numpy as np
import matplotlib.pyplot as plt

def escala_na_origem():
    print("=== Escala na Origem ===\n")

    # Geometria Original (Centrada na Origem)
    # Vértices: A(-2,-2), B(0,3), C(2,-2) e A(-2,-2) para fechar o polígono.
    matriz_vertices = np.array([
        [-2,  0,  2, -2], # Linha do Eixo X
        [-2,  3, -2, -2], # Linha do Eixo Y
        [ 1,  1,  1,  1]  # Linha do Eixo W
    ])

    print("Matriz de Vértices Original (SRO):")
    print(matriz_vertices, "\n")

    # Matriz de Transformação (Escala)
    sx = 2
    sy = 2
    
    matriz_escala = np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ])

    print(f"Matriz de Escala (Sx={sx}, Sy={sy}):")
    print(matriz_escala, "\n")

    # Multiplicação Matricial
    matriz_transformada = matriz_escala @ matriz_vertices

    print("Matriz de Vértices Escalada (Resultante):")
    print(matriz_transformada, "\n")

    # Renderização 2D
    fig, ax = plt.subplots(figsize=(10, 10))
    
    x_orig = matriz_vertices[0, :]
    y_orig = matriz_vertices[1, :]
    
    x_trans = matriz_transformada[0, :]
    y_trans = matriz_transformada[1, :]

    # Triângulo Original (Azul)
    ax.plot(x_orig, y_orig, color='blue', linestyle='--', 
            linewidth=2, marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.3)
    
    # Triângulo Escalado (Vermelho)
    ax.plot(x_trans, y_trans, color='red', linestyle='-', 
            linewidth=2, marker='s', label='Escalado (2,2)')
    ax.fill(x_trans, y_trans, color='red', alpha=0.1)

    # Rótulos A, B, C
    rotulos = ['A', 'B', 'C']
    for i in range(3):
        # original
        ax.annotate(f'{rotulos[i]}({x_orig[i]:.0f},{y_orig[i]:.0f})', 
                    (x_orig[i], y_orig[i]), textcoords="offset points", 
                    xytext=(-35, -5), color='blue', fontweight='bold')
        # escalado
        ax.annotate(f"{rotulos[i]}'({x_trans[i]:.0f},{y_trans[i]:.0f})", 
                    (x_trans[i], y_trans[i]), textcoords="offset points", 
                    xytext=(10, 5), color='darkred', fontweight='bold')

    # Desenhando linhas da origem até os vértices escalados
    for i in range(3):
        ax.plot([0, x_trans[i]], [0, y_trans[i]], color='gray', linestyle=':', alpha=0.7)

    # Plano Cartesiano (4 Quadrantes)
    ax.set_title("Transformação Escala na Origem", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eixo X", fontsize=12)
    ax.set_ylabel("Eixo Y", fontsize=12)
    
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 8)
    
    # Movendo as linhas do gráfico para o centro para formar uma cruz cartesiana real
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # Grade de 1 em 1
    ax.set_xticks(np.arange(-6, 7, 1))
    ax.set_yticks(np.arange(-6, 9, 1))
    ax.grid(True, linestyle=':', color='gray', alpha=0.7)
    
    ax.legend(loc='upper right', fontsize=12)
    
    print("[*] Renderizando o plano cartesiano...")
    plt.show()

if __name__ == "__main__":
    escala_na_origem()