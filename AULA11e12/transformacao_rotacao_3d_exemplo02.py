import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plotar_rotacao_3d_eixo_z():
    print("=== Rotação 3D (Eixo Z)\n")

    # Definição Pirâmide no Espaço Homogêneo 4D
    # Vértices: Base (4 pontos no plano Z=0) e Ápice/Topo (Z=4)
    # Formato: [X, Y, Z, W]^T
    matriz_vertices = np.array([
        [-2,  2,  2, -2,  0], # Eixo X (Base esq, Base dir, Base dir, Base esq, Ápice)
        [-2, -2,  2,  2,  0], # Eixo Y
        [ 0,  0,  0,  0,  4], # Eixo Z (Base no chão, Ápice no alto)
        [ 1,  1,  1,  1,  1]  # Coordenada Homogênea (W)
    ], dtype=np.float32)

    print("Matriz de Vértices 3D Original (SRO):")
    print(matriz_vertices, "\n")

    # Matriz de Rotação no Eixo Z - 45 Graus
    angulo_graus = 45
    theta = np.radians(angulo_graus)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    matriz_rotacao_z = np.array([
        [cos_t, -sin_t, 0, 0],
        [sin_t,  cos_t, 0, 0],
        [    0,      0, 1, 0],
        [    0,      0, 0, 1]
    ])

    print(f"Matriz de Rotação Z ({angulo_graus}º):")
    print(np.round(matriz_rotacao_z, 4), "\n")

    # Processamento (Multiplicação 4x4)
    matriz_transformada = matriz_rotacao_z @ matriz_vertices

    # Renderização (Matplotlib 3D)
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d') # Habilita o contexto 3D

    # Função auxiliar para desenhar a malha do objeto
    def desenhar_piramide(matriz, cor, label, alpha=0.5):
        # Extraindo eixos
        x, y, z = matriz[0, :], matriz[1, :], matriz[2, :]
        
        # Definindo as faces (conexões entre os índices dos vértices)
        # Índices: 0,1,2,3 são a base. 4 é o Ápice.
        faces = [
            [0, 1, 2, 3], # Base
            [0, 1, 4],    # Face Frontal
            [1, 2, 4],    # Face Direita
            [2, 3, 4],    # Face Traseira
            [3, 0, 4]     # Face Esquerda
        ]
        
        # Construindo as coleções de polígonos
        poligonos = []
        for face in faces:
            poligono = [(x[i], y[i], z[i]) for i in face]
            poligonos.append(poligono)
            
        # Adicionando ao eixo 3D
        malha = Poly3DCollection(poligonos, linewidths=1.5, edgecolors=cor, alpha=alpha)
        malha.set_facecolor(cor)
        ax.add_collection3d(malha)
        
        # Plotando os pontos apenas para gerar a legenda corretamente
        ax.scatter(x, y, z, color=cor, s=50, label=label)

    # Desenhando o Original e o Rotacionado
    desenhar_piramide(matriz_vertices, 'blue', 'Original', alpha=0.1)
    desenhar_piramide(matriz_transformada, 'green', f'Rotacionado (Z) em {angulo_graus}º', alpha=0.3)

    # Adicionando um eixo visual (Z) atravessando a pirâmide
    ax.plot([0, 0], [0, 0], [-1, 6], color='red', linestyle='-.', linewidth=2, label='Eixo Z (Pivô)')

    # Configuração do Espaço 3D
    ax.set_title("Transformação 3D: Rotação no Eixo Z", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eixo X", fontsize=12)
    ax.set_ylabel("Eixo Y", fontsize=12)
    ax.set_zlabel("Eixo Z (Profundidade/Altura)", fontsize=12)

    # Limites estáticos
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([0, 6])

    # Melhorando o ângulo da "Câmera" do visualizador
    # elev = ângulo de elevação, azim = rotação azimutal
    ax.view_init(elev=30, azim=45) 
    
    ax.legend(loc='upper right', fontsize=12)
    plt.show()

if __name__ == "__main__":
    plotar_rotacao_3d_eixo_z()