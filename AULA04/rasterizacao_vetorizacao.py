import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Iniciando laboratório de Rasterização...")
    
    # Nessa linha estou definindo a resolução do "Monitor simulado" (15x15 pixels)
    largura, altura = 15, 15
    
    # Vou criar uma buffer, uma especie de Matriz de Pixels preenchida com zeros, que define a cor preta
    framebuffer = np.zeros((altura, largura))
    
    # Vou montar os pontos para definir a posição vetorial da linha
    # Ponto inicial e final geométricos
    x0, y0 = 2, 2
    x1, y1 = 12, 9
    
    # Aqui vai uma "simulação" BEEEEEEMMMMMMMMMM simplificada dO processo proposto por Bresenham
    passos = max(abs(x1 - x0), abs(y1 - y0))
    
    inc_x = (x1 - x0) / passos
    inc_y = (y1 - y0) / passos
    
    x_atual, y_atual = x0, y0
    
    for i in range(passos + 1):
        pixel_x = int(round(x_atual))
        pixel_y = int(round(y_atual))
        
        # Pinta o pixel na memória (Atribui valor 1 - Cor clara)
        framebuffer[pixel_y, pixel_x] = 1.0
        
        # Avança no vetor 
        x_atual += inc_x
        y_atual += inc_y

    # Só pra ficar legal a apresentação, vou colocar as duas imagens lado a lado. Criando uma figura lado a lado 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('#1e1e1e') # Só colocanod uma cor de fundo aqui

    # Agora vou desenhar o modelo Vetorial, o baseado em matematica
    ax1.set_facecolor('black')
    ax1.set_title("O Vetor (Matemática Contínua)", color='white')
    ax1.set_xlim(0, largura)
    ax1.set_ylim(0, altura)
    # Nesse ponto é desenhaod  uma linha matematicamente perfeita (flutuante)
    ax1.plot([x0, x1], [y0, y1], color='red', linewidth=2, label='Vetor Ideal')
    ax1.grid(True, color='white', alpha=0.2)
    ax1.legend()
    ax1.tick_params(colors='white')

    # Agora vou desenhar o modelo Rasterizado (Pixels) ---
    ax2.set_title("A Rasterização (Grade de Pixels)", color='white')
    # O cmap='gray' converte os 0s e 1s da matriz calculada acima em cores visíveis
    ax2.imshow(framebuffer, cmap='gray', origin='lower', extent=[0, largura, 0, altura])
    # Sobrepõe a linha vetorial por cima só pra para mostrar o mapeamento
    ax2.plot([x0, x1], [y0, y1], color='red', linewidth=2, linestyle='--', alpha=0.5)
    ax2.grid(True, color='white', alpha=0.2)
    ax2.tick_params(colors='white')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()