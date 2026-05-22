import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    print("Iniciando a renderização gráfica...")

    # Cria uma figura e um plano cartesiano (Eixos)
    fig, ax = plt.subplots(figsize=(6, 6))

    # Configura os limites do "Plano 2D"
    ax.set_xlim(0, 15) # Eixo X
    ax.set_ylim(0, 15) # Eixo Y
    ax.set_title("Hello World - Computação Gráfica", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)

    # Desenhando uma figura Primitiva: Polígono (Triângulo)
    # Coordenadas dos vértices: (2,2), (8,2), (5,8)
    triangulo = patches.Polygon([[2,2], [8,2], [5,8]], closed=True, color='blue', alpha=0.7)
    ax.add_patch(triangulo)

    # Desenhando uma figura Primitiva: Círculo
    # Centro (10,8) com raio 1.5
    circulo = patches.Circle((10, 8), radius=1.5, color='orange', alpha=0.9)
    ax.add_patch(circulo)

    print("Abrindo a janela de visualização...")
    
    # Comando para renderizar
    plt.show()

    print("Processo concluído com sucesso.")

if __name__ == "__main__":
    main()