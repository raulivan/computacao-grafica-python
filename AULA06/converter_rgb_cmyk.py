from PIL import Image

def criar_imagem_rgb(largura, altura, cor_rgb, nome_arquivo):
    """
    Cria uma imagem RGB com uma cor sólida e a salva em disco.
    """
    # Image.new aloca a matriz na memória. 
    imagem = Image.new("RGB", (largura, altura), cor_rgb)
    
    # Salva o arquivo
    imagem.save(f"{nome_arquivo}.png")
    print(f"[Sucesso] Imagem RGB {nome_arquivo} criada com sucesso.")

def criar_imagem_cmyk(largura, altura, cor_cmyk, nome_arquivo):
    """
    Cria uma imagem CMYK com uma cor sólida e a salva em disco.
    """
    c_int = int((cor_cmyk[0]/100) * 255)
    m_int = int((cor_cmyk[1]/100) * 255)
    y_int = int((cor_cmyk[2]/100) * 255)
    k_int = int((cor_cmyk[3]/100) * 255)

    # Alocamos a matriz agora no modo CMYK.
    imagem = Image.new("CMYK", (largura, altura), (c_int,m_int,y_int,k_int))

    # como JPEG ou TIFF. O formato PNG não suporta CMYK nativamente.
    imagem.save(f"{nome_arquivo}.jpg")
    print(f"[Sucesso] Imagem CMYK {nome_arquivo} criada com sucesso.")

def rgb_para_cmyk(r, g, b):
    # Condição de contorno para o preto absoluto,
    #  evitar erro de dividir por zero
    if (r == 0) and (g == 0) and (b == 0):
        return 0.0, 0.0, 0.0, 1.0
    
    # Normalização para o espaço float [0.0, 1.0]
    r_prime = r / 255.0
    g_prime = g / 255.0
    b_prime = b / 255.0

    # Cálculo do canal Key (Preto)
    k = 1.0 - max(r_prime, g_prime, b_prime)

    # Cálculo dos pigmentos subtrativos
    c = (1.0 - r_prime - k) / (1.0 - k)
    m = (1.0 - g_prime - k) / (1.0 - k)
    y = (1.0 - b_prime - k) / (1.0 - k)

    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

if __name__ == "__main__":
    # dimensões da imagem
    LARGURA = 400
    ALTURA = 400

    # Testando a cor Amarela: (255, 255, 0) RGB
    cor_amarela_rgb = (255, 255, 0)
    print(f"Cor Amarela em RGB: {cor_amarela_rgb}")
    criar_imagem_rgb(LARGURA, ALTURA, cor_amarela_rgb, "cor_rgb")

    # Testando a cor vermelha:  (0%, 97%, 89%, 6%) CMYK
    cor_vermelha_cmyk = (0, 97, 89, 6)
    criar_imagem_cmyk(LARGURA, ALTURA, cor_vermelha_cmyk, "cor_cmyk")

    # Calcula a cor correspondente em CMYK
    cor_amarelo_cmyk = rgb_para_cmyk(cor_amarela_rgb[0], cor_amarela_rgb[1], cor_amarela_rgb[2])
    print(f"Cor Amarela em CMYK: {cor_amarelo_cmyk}")

    c_int = int(cor_amarelo_cmyk[0] * 255)
    m_int = int(cor_amarelo_cmyk[1] * 255)
    y_int = int(cor_amarelo_cmyk[2] * 255)
    k_int = int(cor_amarelo_cmyk[3] * 255)
    
    # Agrupamos na tupla final
    cor_amarelo_cmyk_int = (c_int, m_int, y_int, k_int)
    criar_imagem_cmyk(LARGURA, ALTURA, cor_amarelo_cmyk_int, "cor_cmyk_conversao")

    print('Teste 2')

    vermelho_rgb = (255,0,0)
    print(f"Vermelho RGB: {vermelho_rgb}")
    vermelhor_cmyk = rgb_para_cmyk(vermelho_rgb[0], vermelho_rgb[1], vermelho_rgb[2])
    print(f"Vermelho CMYK sem normalizar: {vermelhor_cmyk}")

    c_int = int(vermelhor_cmyk[0] * 255)
    m_int = int(vermelhor_cmyk[1] * 255)
    y_int = int(vermelhor_cmyk[2] * 255)
    k_int = int(vermelhor_cmyk[3] * 255)

    vermelho_cmyk_int = (c_int, m_int, y_int, k_int)
    print(f"Vermelho CMYK normalizado")

    criar_imagem_rgb(LARGURA, ALTURA, vermelho_rgb, "cor_vermelho_rgb")
    criar_imagem_cmyk(LARGURA, ALTURA, vermelho_cmyk_int, "cor_vermelho_cmyk_conversao")
        