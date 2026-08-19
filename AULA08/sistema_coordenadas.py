import numpy as np

def imprimir_ponto(nome_espaco, vetor):
    """Imprimir o vetor formatado."""
    print(f"{nome_espaco}: (X: {vetor[0][0]:.2f}, Y: {vetor[1][0]:.2f}, W: {vetor[2][0]:.2f})")

def simulador_pipeline_grafico():
    print("SIMULAÇÃO DO PIPELINE GRÁFICO 2D\n")
    
    # SRO (Objeto)
    # Um vértice do Personagem (homem). O centro do carro é (0,0).
    # O Homem está 5 unidades à frente e 2 acima do eixo.
    # (X, Y, W) W (Weight ou Peso Homogêneo) funciona como uma "flag",
    #              que ensina à GPU a diferença entre um Ponto e um Vetor.
    P_SRO = np.array([[5.0], [2.0], [1.0]]) 
    imprimir_ponto("1. SRO (Objeto)", P_SRO)


    # SRU (Universo)
    # Vamos colocar o Personagem na posição (100, 50) no mundo virtual.
    Matriz_Model = np.array([
        [1, 0, 100],
        [0, 1, 50],
        [0, 0, 1]
    ])
    
    # Multiplicação matricial: P_SRU = Model * P_SRO
    P_SRU = Matriz_Model @ P_SRO
    imprimir_ponto("2. SRU (Universo)", P_SRU)

    # SRN - Normalizado
    # Nossa câmera enxerga uma "janela" do mundo: do X=0 a X=200, e Y=0 a Y=100.
    # É preciso mapear isso matematicamente para o cubo [-1, 1].
    # Matriz simplificada:
    largura_mundo = 200.0
    altura_mundo = 100.0
    
    Matriz_Normalizacao = np.array([
        [2.0/largura_mundo, 0, -1],
        [0, 2.0/altura_mundo, -1],
        [0, 0, 1]
    ])
    
    P_SRN = Matriz_Normalizacao @ P_SRU
    imprimir_ponto("3. SRN (Normalizado)", P_SRN)


    # SRD (Dispositivo / Screen Space)
    # O monitor tem uma janela (Viewport) de 800x600 pixels.
    # Mapeamos de [-1, 1] para [0, 800] no X, e [0, 600] no Y.
    # Não esquewce que o eixo Y do monitor é invertido (cresce para baixo).
    largura_tela = 800.0
    altura_tela = 600.0
    
    Matriz_Viewport = np.array([
        [largura_tela/2.0, 0,                 largura_tela/2.0],
        [0,                -altura_tela/2.0,  altura_tela/2.0],  # O negativo inverte o Y
        [0,                0,                 1]
    ])
    
    P_SRD = Matriz_Viewport @ P_SRN
    imprimir_ponto("4. SRD (Dispositivo/Tela)", P_SRD)

if __name__ == "__main__":
    simulador_pipeline_grafico()