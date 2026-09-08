import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def plotar_rotacao_composicao():
    print("=== Composição de Rotação ===\n")

    # geometria no 1º Quadrante
    # Vértices do Triângulo: A(4,2), B(6,6), C(8,2) e fechamento A(4,2)
    matriz_vertices = np.array([
        [4, 6, 8, 4], # Coordenadas X
        [2, 6, 2, 2], # Coordenadas Y
        [1, 1, 1, 1]  # Coordenadas Homogêneas (W)
    ], dtype=np.float32)

    # ponto Pivô (Pa)
    # calculo o Baricentro (Centro de Gravidade) 
    # somando X e Y e dividindo por 3.
    pa_x = np.mean(matriz_vertices[0, 0:3])
    pa_y = np.mean(matriz_vertices[1, 0:3])
    print(f"Centro do Triângulo: X={pa_x:.2f}, Y={pa_y:.2f}\n")

    # matrizes de tranformação
    angulo_graus = 90 
    theta = np.radians(angulo_graus)
    c, s = np.cos(theta), np.sin(theta)

    # MTC - Translação para a Origem (-pa_x, -pa_y)
    MTC = np.array([
        [1, 0, -pa_x],
        [0, 1, -pa_y],
        [0, 0,     1]
    ])

    # MR - Rotação
    MR = np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

    # MTO - Translação de Volta à Posição Original (+pa_x, +pa_y)
    MTO = np.array([
        [1, 0, pa_x],
        [0, 1, pa_y],
        [0, 0,    1]
    ])

    # Construção da Matriz de tranformação
    # no codigo A leitura e execução é da Direita para a Esquerda!
    M_Composta = MTO @ MR @ MTC
    
    print(f"Matriz Composta (MTO * MR * MTC:")
    print(np.round(M_Composta, 4), "\n")

    # Calculando os novos verticies ERRADO
    matriz_rotacao_errada = MR @ matriz_vertices
    
    # Calculando os novos verticies CORRETO
    matriz_rotacao_correta = M_Composta @ matriz_vertices

    # renderização
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # coordenadas para plotagem
    x_orig, y_orig = matriz_vertices[0, :], matriz_vertices[1, :]
    x_err, y_err = matriz_rotacao_errada[0, :], matriz_rotacao_errada[1, :]
    x_cor, y_cor = matriz_rotacao_correta[0, :], matriz_rotacao_correta[1, :]

    # objeto original
    ax.plot(x_orig, y_orig, color='blue', linestyle='--', linewidth=2, 
            marker='o', label='Original no 1º Quad')
    ax.fill(x_orig, y_orig, color='blue', alpha=0.1)

    # rotação errada
    ax.plot(x_err, y_err, color='gray', linestyle=':', linewidth=2, 
            label='Rotação SÓ com MR (Orbitou)')
    ax.fill(x_err, y_err, color='gray', alpha=0.15)
    
    # linhas ligando a origem ao ponto
    ax.plot([0, x_orig[0]], [0, y_orig[0]], color='gray', 
            linestyle=':', alpha=0.5)
    ax.plot([0, x_err[0]], [0, y_err[0]], color='gray', 
            linestyle=':', alpha=0.5)

    # rotação correta
    ax.plot(x_cor, y_cor, color='red', linestyle='-', linewidth=2, 
            marker='s', label=f'Rotação Correta ({angulo_graus}º)')
    ax.fill(x_cor, y_cor, color='red', alpha=0.3)

    # Marcando o Ponto Pivô (Pa)
    ax.plot(pa_x, pa_y, color='black', marker='X', markersize=10)
    ax.annotate(f"Pivô Pa\n({pa_x:.1f}, {pa_y:.1f})", (pa_x, pa_y), 
                xytext=(10, -15), textcoords="offset points", fontweight='bold')

    # legendas
    ax.annotate(f"A", (x_orig[0], y_orig[0]), xytext=(5,5), 
                textcoords="offset points", color='blue', fontweight='bold')
    ax.annotate(f"A' (Orbitou)", (x_err[0], y_err[0]), xytext=(-65,-15), 
                textcoords="offset points", color='gray')
    ax.annotate(f"A' (Eixo)", (x_cor[0], y_cor[0]), xytext=(5,5), 
                textcoords="offset points", color='red', fontweight='bold')

    # arco vermelho ao redor do pivô 
    arco = Arc((pa_x, pa_y), 2.5, 2.5, angle=0, theta1=0, 
               theta2=angulo_graus, color='red', linewidth=2, linestyle='--')
    ax.add_patch(arco)

    # plano Cartesiano
    ax.set_title("Matriz de tranformação (Composição)", fontsize=14, fontweight='bold')
    ax.set_xlim(-8, 10)
    ax.set_ylim(-2, 10)
    
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    ax.set_xticks(np.arange(-8, 11, 1))
    ax.set_yticks(np.arange(-2, 11, 1))
    ax.grid(True, linestyle=':', color='gray', alpha=0.6)
    
    ax.legend(loc='upper left', fontsize=11)
    
    print("[*] Renderizando o plano cartesiano...")
    plt.show()

if __name__ == "__main__":
    plotar_rotacao_composicao()