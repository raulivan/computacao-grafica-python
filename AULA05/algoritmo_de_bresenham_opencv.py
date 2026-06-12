import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Cria a tela (matriz NumPy)
    tela = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Primitiva: Linha
    # cv2.line(imagem, ponto_inicial, ponto_final, cor_rgb, espessura)
    cv2.line(tela, (50, 50), (250, 50), (0, 255, 0), 3) # Linha Verde
    
    # Primitiva: Círculo
    # cv2.circle(imagem, centro, raio, cor_rgb, espessura (-1 preenche tudo))
    cv2.circle(tela, (150, 150), 60, (255, 0, 0), -1) # Círculo Vermelho
    
    # Primitiva: Polígono (Triângulo)
    pontos_triangulo = np.array([[150, 200], [100, 280], [200, 280]], np.int32)
    
    # Spo toma cuidado nessa parte pq
    # O OpenCV precisa que o array de pontos tenha o formato (número_pontos, 1, 2)
    pontos_triangulo = pontos_triangulo.reshape((-1, 1, 2))
    cv2.fillPoly(tela, [pontos_triangulo], (0, 255, 255)) # Triângulo Amarelo
    
    # Exibe a imagem
    plt.imshow(tela)
    plt.title("Primitivas com OpenCV")
    plt.show()

if __name__ == "__main__":
    main()