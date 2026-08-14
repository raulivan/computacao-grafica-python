from PIL import Image

import colorsys
from PIL import Image

def criar_imagem_via_hsv(largura, altura, h_graus, s_pct, v_pct, nome_arquivo):
    """
    Cria uma imagem baseada no espaço HSV.
    :param h_graus: Matiz (Hue) de 0 a 360 graus.
    :param s_pct: Saturação (Saturation) de 0 a 100%.
    :param v_pct: Valor/Brilho (Value) de 0 a 100%.
    """
    # 1. Normalização do domínio físico para o domínio matemático [0.0, 1.0]
    h_norm = h_graus / 360.0
    s_norm = s_pct / 100.0
    v_norm = v_pct / 100.0

    # 2. Transformação do espaço cilíndrico (HSV) para vetorial (RGB)
    r_float, g_float, b_float = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)

    # 3. Conversão de ponto flutuante para inteiros de 8 bits (0-255)
    r = int(r_float * 255)
    g = int(g_float * 255)
    b = int(b_float * 255)

    # 4. Alocação de memória e salvamento
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
    # 1. Normalização para o intervalo [0.0, 1.0]
    h_norm = h_graus / 360.0
    s_norm = s_pct / 100.0
    l_norm = l_pct / 100.0

    # 2. Transformação do espaço cilíndrico (HLS/HSL) para vetorial (RGB)
    # Nota arquitetural: No Python, a função se chama hls_to_rgb (a ordem é Matiz, Luminosidade, Saturação)
    r_float, g_float, b_float = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)

    # 3. Conversão para inteiros de 8 bits
    r = int(r_float * 255)
    g = int(g_float * 255)
    b = int(b_float * 255)

    # 4. Alocação de memória e salvamento
    imagem = Image.new("RGB", (largura, altura), (r, g, b))
    imagem.save(nome_arquivo)
    print(f"[HSL] Imagem salva: {nome_arquivo} | RGB final: ({r}, {g}, {b})")


def criar_composicao_alpha():
    print("\n--- Composição com Canal Alpha (RGBA) ---")
    largura, altura = 400, 400

    # Fundo (Background) - Vermelho totalmente Opaco (Alpha=255)
    # RGBA = (R, G, B, Alpha)
    fundo = Image.new("RGBA", (largura, altura), (255, 0, 0, 255))
    fundo.save("fundo_alpha.png")
    print("[Sucesso] Imagem 'fundo_alpha.png' salva.")

    # Primeiro Plano (Foreground) - Azul 50%
    # Alpha = 127 (Aproximadamente 50% de 255)
    primeiro_plano = Image.new("RGBA", (largura, altura), (0, 0, 255, 127))
    primeiro_plano.save("primeiro_plano_alpha.png")
    print("[Sucesso] Imagem 'primeiro_plano_alpha.png' salva.") 

    # Aplica a equação de Porter-Duff
    resultado = Image.alpha_composite(fundo, primeiro_plano)
    resultado.save("resultado_alpha.png") 
    print("[Sucesso] Imagem 'resultado_alpha.png' salva.")

# --- Execução Principal ---
if __name__ == "__main__":
    LARGURA = 400
    ALTURA = 400

    print("=== Testes de Espaços Perceptuais de Cor ===\n")

    # TESTE 1: Ciano Vibrante em HSV
    # H = 180 (Ciano), S = 100% (Puro), V = 100% (Brilho máximo)
    criar_imagem_via_hsv(LARGURA, ALTURA, 180, 100, 100, "ciano_hsv.png")

    # TESTE 2: Ciano Vibrante em HSL
    # Note a diferença fundamental: Para obter a cor pura em HSL,
    # a Luminosidade (L) deve ser exatos 50%. Se for 100%, será totalmente branco.
    criar_imagem_via_hsl(LARGURA, ALTURA, 180, 100, 50, "ciano_hsl.png")

    # TESTE 3: Efeito "Pastel" (Desbotado) usando HSL
    # Mantemos o Ciano puro (H=180, S=100%), mas aumentamos a luminosidade para 80%
    # Isso mistura "tinta branca" à cor matematicamente.
    criar_imagem_via_hsl(LARGURA, ALTURA, 180, 100, 80, "ciano_pastel_hsl.png")
    
