import colorsys
from PIL import Image

def criar_imagem_via_hsv(largura, altura, h_graus, s_pct, v_pct, nome_arquivo):
    """
    Cria uma imagem baseada no espaço HSV.
    :param h_graus: Matiz (Hue) de 0 a 360 graus.
    :param s_pct: Saturação (Saturation) de 0 a 100%.
    :param v_pct: Valor/Brilho (Value) de 0 a 100%.
    """
    # Normalização do domínio físico para o domínio matemático [0.0, 1.0]
    h_norm = h_graus / 360.0
    s_norm = s_pct / 100.0
    v_norm = v_pct / 100.0

    # Transformação do espaço cilíndrico (HSV) para vetorial (RGB)
    r_float, g_float, b_float = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)

    # Converte de ponto flutuante para inteiros de 8 bits (0-255)
    r = int(r_float * 255)
    g = int(g_float * 255)
    b = int(b_float * 255)

    imagem = Image.new("RGB", (largura, altura), (r, g, b))
    imagem.save(nome_arquivo)
    print(f"[HSV] Imagem salva: {nome_arquivo} | RGB final: ({r}, {g}, {b})")

def criar_imagem_via_hsl(largura, altura, h_graus, s_pct, l_pct, nome_arquivo):
    """
    Cria uma imagem baseada no espaço HSL.
    :param h_graus: Matiz (Hue) de 0 a 360 graus.
    :param s_pct: Saturação (Saturation) de 0 a 100%.
    :param l_pct: Luminosidade (Lightness) de 0 a 100%.
    """
    # Mesma coisa, faz a normalização para o intervalo [0.0, 1.0]
    h_norm = h_graus / 360.0
    s_norm = s_pct / 100.0
    l_norm = l_pct / 100.0

    # tbm tranforma o espaço cilíndrico (HLS/HSL) para vetorial (RGB)
    r_float, g_float, b_float = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)

    # Converte para inteiros de 8 bits
    r = int(r_float * 255)
    g = int(g_float * 255)
    b = int(b_float * 255)

    imagem = Image.new("RGB", (largura, altura), (r, g, b))
    imagem.save(nome_arquivo)
    print(f"[HSL] Imagem salva: {nome_arquivo} | RGB final: ({r}, {g}, {b})")

def exemplo_hsv_para_rgb():
    """ Demonstra a facilidade de alterar uma cor girando seu Matiz (Hue) """
    print("--- Conversão HSV para RGB ---")
    
    # Matiz (120 graus = Verde). 
    # Em colorsys, Hue é normalizado de 0.0 a 1.0 (120/360 = 0.33)
    h, s, v = 120 / 360.0, 1.0, 1.0 
    
    # colorsys retorna floats entre 0 e 1
    r_float, g_float, b_float = colorsys.hsv_to_rgb(h, s, v)
    
    # Convertendo para a escala discreta de 8 bits (0-255) da memória de vídeo
    r, g, b = int(r_float * 255), int(g_float * 255), int(b_float * 255)
    print(f"O HSV ({h:.2f}, {s}, {v}) virou o RGB: ({r}, {g}, {b})")


if __name__ == "__main__":
    LARGURA = 400
    ALTURA = 400

    # Ciano Vibrante em HSV - H = 180 (Ciano), S = 100% (Puro), V = 100% (Brilho máximo)
    criar_imagem_via_hsv(LARGURA, ALTURA, 180, 100, 100, "ciano_hsv.png")

    # Ciano Vibrante em HSL - Se liga nessa dica:
    # Para obter a cor pura em HSL, a Luminosidade (L) deve ser exatos 50%. 
    # Se for 100%, será totalmente branco.
    criar_imagem_via_hsl(LARGURA, ALTURA, 180, 100, 50, "ciano_hsl.png")

    # Efeito desbotado Desbotado ("Pastel") usando HSL
    # Ciano puro (H=180, S=100%), e aumenta a luminosidade para 80%
    # Isso mistura "tinta branca" à cor matematicamente.
    criar_imagem_via_hsl(LARGURA, ALTURA, 180, 100, 80, "ciano_pastel_hsl.png")