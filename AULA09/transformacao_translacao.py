import numpy as np
import matplotlib.pyplot as plt

def transformacao_translacao():
    print("=== Transformação de Translação ===\n")

    # Definição da Geometria Original (Coordenadas Homogêneas)
    # Vértices: A(1,3), B(3,7), C(5,3) e A(1,3) para fechar o polígono.
    # Cada coluna é um vértice: [X, Y, W]^T
    matriz_vertices = np.array([
        [1, 3, 5, 1], # Linha do Eixo X
        [3, 7, 3, 3], # Linha do Eixo Y
        [1, 1, 1, 1]  # Linha do Eixo W (Coordenada Homogênea)
    ])

    print("Matriz de Vértices Original (SRO):")
    print(matriz_vertices, "\n")

    # Matriz de Transformação (Translação)
    # Vamos transladar o triângulo 2 unidades para a Direita (+X)
    # e 2 unidades para Cima (+Y)
    tx = 2
    ty = 2
    
    matriz_translacao = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

    print(f"Matriz de Translação (tx={tx}, ty={ty}):")
    print(matriz_translacao, "\n")

    # Multiplicação Matricial
    matriz_transformada = matriz_translacao @ matriz_vertices

    print("Matriz de Vértices Transladada (SRU):")
    print(matriz_transformada, "\n")

    # Renderização 2D com o Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Extraindo as linhas (X e Y) 
    x_orig = matriz_vertices[0, :]
    y_orig = matriz_vertices[1, :]
    
    x_trans = matriz_transformada[0, :]
    y_trans = matriz_transformada[1, :]

    # Triângulo Original (Azul, tracejado)
    ax.plot(x_orig, y_orig, color='blue', linestyle='--', 
            linewidth=2, marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1) 
    
    # Triângulo Transladado (Vermelho, sólido)
    ax.plot(x_trans, y_trans, color='red', linestyle='-', 
            linewidth=2, marker='s', label='Transladado')
    ax.fill(x_trans, y_trans, color='red', alpha=0.3)

    # Rótulos A, B, C  para os pontos dos trinangulos
    rotulos = ['A', 'B', 'C']
    for i in range(3):
        # original
        ax.annotate(f'{rotulos[i]} {x_orig[i]:.0f},{y_orig[i]:.0f}', 
                    (x_orig[i], y_orig[i]), textcoords="offset points", 
                    xytext=(-15,-15), color='blue')
        # transladado
        ax.annotate(f"{rotulos[i]}' {x_trans[i]:.0f},{y_trans[i]:.0f}", 
                    (x_trans[i], y_trans[i]), textcoords="offset points", 
                    xytext=(-15,-15), color='darkred')

    # Plano Cartesiano (Grade, Eixos, Limites)
    ax.set_title("Exemplo Translação", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eixo X", fontsize=12)
    ax.set_ylabel("Eixo Y", fontsize=12)
    
    # limites da janela de visualização (Viewport)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 12)
    
    # Desenhando os eixos X=0 e Y=0 em negrito
    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)
    
    # Configurando a grade
    ax.set_xticks(np.arange(0, 16, 1))
    ax.set_yticks(np.arange(0, 13, 1))
    ax.grid(True, linestyle=':', color='gray', alpha=0.7)
    
    ax.legend(loc='upper left', fontsize=12)
    
    print("[*] Renderizando o plano cartesiano...")
    plt.show()

if __name__ == "__main__":
    transformacao_translacao()