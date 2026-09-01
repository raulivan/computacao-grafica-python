import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def rotacao_centro_gravidade():
    print("=== Rotação no Centro de Gravidade ===\n")

    # Definição da Geometria Original
    # Vértices: A(2,2), B(4,5), C(6,2) e fechamento A(2,2)
    matriz_vertices = np.array([
        [2, 4, 6, 2], # Eixo X
        [2, 5, 2, 2], # Eixo Y
        [1, 1, 1, 1]  # Coordenada Homogênea (W)
    ], dtype=np.float32)

    # Cálculo do Centro de Gravidade (Baricentro)
    cx = np.mean(matriz_vertices[0, 0:3])
    cy = np.mean(matriz_vertices[1, 0:3])
    print(f"Centro de Gravidade Calculado (Cx, Cy): ({cx:.2f}, {cy:.2f})\n")

    # Construção das 3 Matrizes
    angulo_graus = 60
    theta = np.radians(angulo_graus)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    # Levar para a Origem (-Cx, -Cy)
    M_T1 = np.array([
        [1, 0, -cx],
        [0, 1, -cy],
        [0, 0,   1]
    ])

    # Rotacionar
    M_R = np.array([
        [cos_t, -sin_t, 0],
        [sin_t,  cos_t, 0],
        [    0,      0, 1]
    ])

    # Trazer de volta (Cx, Cy)
    M_T2 = np.array([
        [1, 0, cx],
        [0, 1, cy],
        [0, 0,  1]
    ])

    # Matriz Mestre
    # Dica: Ordem da Direita para a Esquerda! (M_T2 * M_R * M_T1)
    M_Composta = M_T2 @ M_R @ M_T1
    
    print("Matriz Composta Final (T2 * R * T1):")
    print(np.round(M_Composta, 4), "\n")

    # Multiplicando a matriz
    matriz_transformada = M_Composta @ matriz_vertices

    # Renderização Visual no Matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))
    
    x_orig, y_orig = matriz_vertices[0, :], matriz_vertices[1, :]
    x_trans, y_trans = matriz_transformada[0, :], matriz_transformada[1, :]

    # Plotando os triângulos
    ax.plot(x_orig, y_orig, color='blue', linestyle='--', 
            linewidth=2, marker='o', label='Original')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)
    
    ax.plot(x_trans, y_trans, color='green', linestyle='-', 
            linewidth=2, marker='s', label=f'Rotacionado ({angulo_graus}º) no Eixo')
    ax.fill(x_trans, y_trans, color='green', alpha=0.3)

    # Plotando e Anotando o Centro de Gravidade
    ax.plot(cx, cy, color='black', marker='X', markersize=10, label='Centro de Gravidade')
    ax.annotate(f" CG ({cx:.1f}, {cy:.1f})", (cx, cy), 
                textcoords="offset points", xytext=(5,-15), color='black', fontweight='bold')

    # Legendas
    rotulos = ['A', 'B', 'C']
    for i in range(3):
        ax.annotate(f"{rotulos[i]}", (x_orig[i], y_orig[i]), 
                    textcoords="offset points", xytext=(-15,-10), color='blue')
        ax.annotate(f"{rotulos[i]}'", (x_trans[i], y_trans[i]), 
                    textcoords="offset points", xytext=(5,5), color='darkgreen')

    # Desenhando um arco demonstrando o giro NO PRÓPRIO EIXO
    arco = Arc((cx,cy), 1.5, 1.5, angle=0, theta1=0, 
               theta2=angulo_graus, color='red', linewidth=3, linestyle='-')
    ax.add_patch(arco)
    # Ponta da seta do arco (aproximada)
    ax.plot([cx + 0.75*np.cos(theta)], 
            [cy + 0.75*np.sin(theta)], marker='^', color='red', markersize=8)

    # Configuração do Plano Cartesiano
    ax.set_title("Rotação no Centro de Gravidade", fontsize=14, fontweight='bold')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 8)
    
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 9, 1))
    ax.grid(True, linestyle=':', color='gray', alpha=0.5)
    
    ax.legend(loc='upper right', fontsize=12)
    
    print("Renderizando o plano cartesiano...")
    plt.show()

if __name__ == "__main__":
    rotacao_centro_gravidade()