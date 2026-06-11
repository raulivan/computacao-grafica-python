from PIL import Image

def renderizar_circulo(fator_qualidade):
    """
        O parâmetro O fator_qualidade vai funcionar como um multiplicador da resolução da imagem.
    
        A resolução padrão será: Tela de 300x300 e Raio 50.
        
        Se fator = 0.1 -> Tela vira 30x30, Raio vira 5 (Muito pixelado)
        Se fator = 1.0 -> Tela vira 300x300, Raio vira 50 (Normal)
        Se fator = 4.0 -> Tela vira 1200x1200, Raio vira 200 (Alta Definição)
    """
    largura_base = 300
    altura_base = 300
    raio_base = 50
    
    # calculando os parâmetros
    largura_tela = int(largura_base * fator_qualidade)
    altura_tela = int(altura_base * fator_qualidade)
    raio = int(raio_base * fator_qualidade)
    
    centro_x = int(largura_tela / 2)
    centro_y = int(altura_tela / 2)
    raio_quadrado = raio ** 2

    # Cria a tela
    img = Image.new("RGB", (largura_tela, altura_tela), "white")

    # Os limites de desenho da imawgem
    x_min, x_max = centro_x - raio, centro_x + raio
    y_min, y_max = centro_y - raio, centro_y + raio

    # Simulação do processo de Rasterização
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            
            distancia_quadrada = (x - centro_x)**2 + (y - centro_y)**2
            
            if distancia_quadrada <= raio_quadrado:
                img.putpixel((x, y), (255, 0, 0))

    return img

def main():
    print("Iniciando - Resolução e Aliasing...")
    
    # TESTE 1: BAIXÍSSIMA QUALIDADE (Escadinhas gigantes) significa que o círculo terá apenas 5 pixels de raio!
    img_baixa = renderizar_circulo(fator_qualidade=0.1)
    
    img_baixa_ampliada = img_baixa.resize((300, 300), Image.NEAREST)
    img_baixa_ampliada.save("circulo_1_baixa_qualidade.png")
    print("Gerado: circulo_1_baixa_qualidade.png (Escadinhas evidentes)")

    # TESTE 2: QUALIDADE NORMAL, A mesma do nosso exemplo criar_circulo_raterizado.py
    
    img_normal = renderizar_circulo(fator_qualidade=1.0)
    img_normal.save("circulo_2_qualidade_normal.png")
    print("Gerado: circulo_2_qualidade_normal.png (Borda padrão)")

    # TESTE 3: ALTA RESOLUÇÃO, Renderizado em 1200x1200, escadinha quase invisível
    img_alta = renderizar_circulo(fator_qualidade=4.0)
    
    img_alta_reduzida = img_alta.resize((300, 300), Image.LANCZOS)
    img_alta_reduzida.save("circulo_3_alta_qualidade.png")
    print("Gerado: circulo_3_alta_qualidade.png (Borda perfeitamente lisa)")

if __name__ == "__main__":
    main()