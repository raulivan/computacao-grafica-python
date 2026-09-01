import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

def plotar_rotacao_3d_eixo_z():
    print("=== Rotação 3D no Eixo Z ===\n")

    # Pirâmide de base quadrada centrada na origem
    # Vértices: A(Base Esq Frontal), B(Base Dir Frontal), C(Base Dir Tras), 
    # D(Base Esq Tras), E(Topo/Ápice)
    matriz_vertices = np.array([
        [-1,  1,  1, -1,  0],  # X
        [-1, -1,  1,  1,  0],  # Y
        [ 0,  0,  0,  0,  2],  # Z (A base está no chão Z=0, o topo está em Z=2)
        [ 1,  1,  1,  1,  1]   # W (Coordenada Homogênea)
    ], dtype=np.float32)

    # Matriz 4x4 de Rotação em Z
    angulo_graus = 45
    theta = np.radians(angulo_graus)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    matriz_rotacao_z = np.array([
        [ cos_t, -sin_t, 0, 0],
        [ sin_t,  cos_t, 0, 0],
        [     0,      0, 1, 0],
        [     0,      0, 0, 1]
    ])

    print(f"Matriz de Rotação 4x4 (Eixo Z, {angulo_graus}º):")
    print(np.round(matriz_rotacao_z, 4), "\n")

    # Multiplicação
    matriz_transformada = matriz_rotacao_z @ matriz_vertices

    # Renderização 3D
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Função auxiliar para desenhar as arestas do objeto
    def desenhar_wireframe(ax, matriz, cor, label, estilo):
        x, y, z = matriz[0, :], matriz[1, :], matriz[2, :]
        
        # Lista de conexões (índices dos vértices para desenhar as linhas)
        # Base: 0->1->2->3->0, Arestas laterais: 0->4, 1->4, 2->4, 3->4
        arestas = [
            (0, 1), (1, 2), (2, 3), (3, 0), # Base
            (0, 4), (1, 4), (2, 4), (3, 4)  # Laterais até o topo
        ]
        
        # Plota os vértices (Pontos)
        ax.scatter(x, y, z, color=cor, s=50)
        
        # Plota as arestas (Linhas)
        for i, (inicio, fim) in enumerate(arestas):
            lbl = label if i == 0 else "" # Evita repetir label na legenda
            ax.plot([x[inicio], x[fim]], 
                    [y[inicio], y[fim]], 
                    [z[inicio], z[fim]], 
                    color=cor, linestyle=estilo, linewidth=2, label=lbl)

    # Desenhando a Pirâmide Original (Azul, tracejada)
    desenhar_wireframe(ax, matriz_vertices, 'blue', 'Original SRO', '--')
    
    # Desenhando a Pirâmide Rotacionada (Vermelha, sólida)
    desenhar_wireframe(ax, matriz_transformada, 'red', 
                       f'Rotacionado Z ({angulo_graus}º)', '-')

    # Configuração do Espaço Cartesiano 3D
    ax.set_title("Transformação 3D: Rotação no Eixo Z", 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel("Eixo X (Largura)", fontweight='bold')
    ax.set_ylabel("Eixo Y (Profundidade)", fontweight='bold')
    ax.set_zlabel("Eixo Z (Altura)", fontweight='bold')
    
    # Travando a escala dos eixos 
    limite = 2.5
    ax.set_xlim([-limite, limite])
    ax.set_ylim([-limite, limite])
    ax.set_zlim([0, limite])
    
    # Definindo a câmera inicial
    ax.view_init(elev=30, azim=45)
    
    ax.legend()
    plt.show()

if __name__ == "__main__":
    plotar_rotacao_3d_eixo_z()