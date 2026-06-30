import cv2
import numpy as np
import math

def main():
    print("Gerando gabarito do Braço Robótico 2D...")

    # Configurações da "Tela" (Framebuffer)
    # Criamos uma matriz NumPy 500x500 RGB preenchida com zeros (preto)
    altura, largura = 500, 500
    img = np.zeros((altura, largura, 3), dtype=np.uint8)

    # Ponto de origem do robô na tela (x, y) - Canto inferior esquerdo
    origem_base = (70, 430)
    
    # Comprimento dos elos  em pixels
    comp_elo1 = 150 # Do ombro ao cotovelo
    comp_elo2 = 120 # Do cotovelo à garra
    
    # Ângulos das juntas em GRAUS (confortável para humanos)
    # Na CG, o Y cresce para BAIXO, então 0° é para a direita,
    # 90° é para CIMA (subtraindo do Y).
    angulo_ombro_deg = 60
    angulo_cotovelo_deg = -45 # Relativo ao primeiro elo

    # =================================================================
    # 3. CÁLCULO DE CINEMÁTICA DIRETA (Matemática Pura)
    # =================================================================
    # Convertemos graus para radianos para usar as funções math.cos/sin
    ang_ombro_rad = math.radians(angulo_ombro_deg)
    ang_cotovelo_rad = math.radians(angulo_cotovelo_deg)
    
    # JUNTA 1: O Cotovelo (pos_cotovelo)
    # Calculada em relação à Origem da Base
    # Subtraímos no Y para o robô "subir" na tela.
    cotovelo_x = origem_base[0] + comp_elo1 * math.cos(ang_ombro_rad)
    cotovelo_y = origem_base[1] - comp_elo1 * math.sin(ang_ombro_rad)
    pos_cotovelo = (int(cotovelo_x), int(cotovelo_y))
    
    # JUNTA 2: O Efetuador Final/Garra (pos_garra)
    # Calculada em relação à Posição do Cotovelo.
    # O ângulo total do segundo elo é a soma dos dois ângulos.
    ang_total_rad = ang_ombro_rad + ang_cotovelo_rad
    
    garra_x = pos_cotovelo[0] + comp_elo2 * math.cos(ang_total_rad)
    garra_y = pos_cotovelo[1] - comp_elo2 * math.sin(ang_total_rad)
    pos_garra = (int(garra_x), int(garra_y))

    # =================================================================
    # 4. DESENHO DAS PRIMITIVAS (OpenCV)
    # =================================================================
    # Cores (BGR - Blue, Green, Red)
    COR_ELO = (200, 200, 200) # Cinza claro
    COR_JUNTA = (0, 0, 255)    # Vermelho
    COR_GARRA = (0, 255, 255)  # Amarelo

    # A. Desenha a Base fixa do robô (Um retângulo preenchido)
    cv2.rectangle(img, (origem_base[0]-30, origem_base[1]), (origem_base[0]+30, altura), (100, 100, 100), -1)

    # B. Desenha os Elos (Linhas grossas entre as juntas calculadas)
    # Elo 1: Ombro -> Cotovelo
    cv2.line(img, origem_base, pos_cotovelo, COR_ELO, 8)
    # Elo 2: Cotovelo -> Garra
    cv2.line(img, pos_cotovelo, pos_garra, COR_ELO, 6)

    # C. Desenha as Juntas (Círculos nas posições calculadas)
    cv2.circle(img, origem_base, 12, COR_JUNTA, -1) # Ombro
    cv2.circle(img, pos_cotovelo, 10, COR_JUNTA, -1) # Cotovelo

    # D. Desenha uma garra simples no final (Um retângulo pequeno)
    cv2.circle(img, pos_garra, 8, COR_GARRA, -1) # Ponto final

    # 5. EXIBIÇÃO NATIVA (OpenCV `cv2.imshow`)
    # O nome da janela é o primeiro argumento
    cv2.imshow("Braco Robotico 2D - CEFET-MG", img)
    
    # IMPORTANTE: Mantém a janela aberta até que o usuário aperte QUALQUER tecla no teclado
    # Se você omitir isso, a janela abrirá e fechará em milissegundos.
    cv2.waitKey(0)
    
    # Boa prática para fechar todas as janelas ao encerrar
    cv2.destroyAllWindows()
    print("Programa encerrado.")

if __name__ == "__main__":
    main()