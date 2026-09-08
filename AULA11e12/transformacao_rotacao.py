import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def transformacao_rotacao():
    print("=== Rotação 2D ===\n")

    # Definição od triângulo
    # Vértices: A(2,2), B(4,5), C(6,2) e fechamento em A(2,2)
    matriz_vertices = np.array([
        [2, 4, 6, 2], # Eixo X
        [2, 5, 2, 2], # Eixo Y
        [1, 1, 1, 1]  # Coordenada Homogênea (W)
    ], dtype=np.float32)

    print("Matriz de Vértices Original:")
    print(matriz_vertices, "\n")

    # Definição do Ângulo e Conversão para Radianos
    angulo_graus = 60
    theta = np.radians(angulo_graus) 

    # Construção da Matriz de Rotação
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    matriz_rotacao = np.array([
        [ cos_t, -sin_t, 0],
        [ sin_t,  cos_t, 0],
        [     0,      0, 1]
    ])

    print(f"Matriz de Rotação ({angulo_graus} graus / {theta:.4f} radianos):")
    print(np.round(matriz_rotacao, 4), "\n")

    # Multiplicação
    matriz_transformada = matriz_rotacao @ matriz_vertices

    print("Matriz de Vértices Rotacionada:")
    print(np.round(matriz_transformada, 4), "\n")

    # Renderização no Matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))
    
    x_orig, y_orig = matriz_vertices[0, :], matriz_vertices[1, :]
    x_trans, y_trans = matriz_transformada[0, :], matriz_transformada[1, :]

    # Plotando os triângulos
    ax.plot(x_orig, y_orig, color='blue', linestyle='--', 
            linewidth=2, marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)
    
    ax.plot(x_trans, y_trans, color='green', linestyle='-', 
            linewidth=2, marker='s', label=f'Rotacionado ({angulo_graus}º)')
    ax.fill(x_trans, y_trans, color='green', alpha=0.3)

    # Legendas
    rotulos = ['A', 'B', 'C']
    for i in range(3):
        ax.annotate(f"{rotulos[i]}", (x_orig[i], y_orig[i]), 
                    textcoords="offset points", xytext=(5,5), color='blue')
        ax.annotate(f"{rotulos[i]}'", (x_trans[i], y_trans[i]), 
                    textcoords="offset points", xytext=(5,5), color='darkgreen')

    # Desenhando as linhas de raio e o arco de órbita do Vértice A
    raio_a = np.sqrt(x_orig[0]**2 + y_orig[0]**2) # Distância da origem usando TeoremaPitágoras
    ax.plot([0, x_orig[0]], [0, y_orig[0]], color='gray', linestyle=':', alpha=0.7)
    ax.plot([0, x_trans[0]], [0, y_trans[0]], color='gray', linestyle=':', alpha=0.7)
    
    # Desenhando o arco para mostrar o movimento angular (A até A')
    arco = Arc((0,0), raio_a*2, raio_a*2, angle=0, 
               theta1=np.degrees(np.arctan2(y_orig[0], x_orig[0])), 
               theta2=np.degrees(np.arctan2(y_trans[0], x_trans[0])), 
               color='orange', linewidth=2, linestyle='--')
    ax.add_patch(arco)
    ax.text(0.5, 1.5, f"{angulo_graus}º", color='orange', fontweight='bold')

    # Configuração do Plano Cartesiano
    ax.set_title("Rotação 2D Orbital", fontsize=14, fontweight='bold')
    
    # Ajustando limites para mostrar a rotação (quadrante negativo de X)
    ax.set_xlim(-6, 8)
    ax.set_ylim(-2, 10)
    
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    ax.set_xticks(np.arange(-6, 9, 1))
    ax.set_yticks(np.arange(-2, 11, 1))
    ax.grid(True, linestyle=':', color='gray', alpha=0.5)
    
    ax.legend(loc='upper right', fontsize=12)
    
    print("Renderizando o plano cartesiano...")
    plt.show()

if __name__ == "__main__":
    transformacao_rotacao()