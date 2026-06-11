from PIL import Image


def main():
    print("Iniciando rasterização do círculo...")
    
    # Define a resolução da Tela    300 x 300
    largura_tela, altura_tela = 300, 300
    img = Image.new("RGB", (largura_tela, altura_tela), "white")

    # propriedades matemáticas do Círculo
    centro_x = 150
    centro_y = 150
    raio = 50
    
    raio_quadrado = raio ** 2

    # aqui to defiinindo apenas o quadrado onde o círculo pode existir.
    x_min = centro_x - raio
    x_max = centro_x + raio
    y_min = centro_y - raio
    y_max = centro_y + raio

    # Simulação do Processo de Rasterização
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            
            # Calcula a distancia
            distancia_quadrada = (x - centro_x)**2 + (y - centro_y)**2
            
             # Se a distância do pixel (x,y) até o centro for menor ou igual ao raio
            if distancia_quadrada <= raio_quadrado:
                # O pixel pertence ao círculo! Pinta de vermelho. RGB
                img.putpixel((x, y), (255, 0, 0))

    # Salva a imagem ba pasta de execução do script
    img.save("circulo_rasterizado.png")
    print("Círculo salvo como 'circulo_rasterizado.png'.")


if __name__ == "__main__":
    main()