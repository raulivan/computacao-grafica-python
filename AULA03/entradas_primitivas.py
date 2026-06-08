"""
Este código tem como objetivo riar  um script Python que escuta o Dispositivo de Entrada (Mouse),
extrai as coordenadas, e quando obtiver três pontos, o sistema calculará 
as Primitivas (Linhas/Polígono) e enviará para o Dispositivo de Saída (Tela).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def construir_plano_cartesiado(eixo_x:float, eixo_y:float, title:str):
    # Criando o plano cartesiano
    fig, ax = plt.subplots(figsize=(7, 7))

    # Fundo da janela externa (Figure) em preto
    fig.patch.set_facecolor('black') 
    
    # Fundo da malha interna (Axes) em preto
    ax.set_facecolor('black')
    
    # Cor do Título em branco para contrastar
    ax.set_title("Dispositivo Lógico: Clique 3 vezes", color='white', fontsize=14)
    
    # Configura a malha (Grid)
    ax.grid(True, color='white', linestyle='--', alpha=0.3)
    
    # Configura as marcações de números (Ticks) em branco
    ax.tick_params(colors='white')
    
    # Configura a cor da borda do gráfico em branco
    for spine in ax.spines.values():
        spine.set_color('white')


    ax.set_xlim(0, eixo_x)
    ax.set_ylim(0, eixo_y)
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")

    return fig, ax

def main():
    print("Dispositivos de Entrada...")
    
    fig, ax = construir_plano_cartesiado(eixo_x=100, eixo_y=100, title="Clique 3 vezes para gerar a Primitiva Gráfica")
    
    # Lista para armazenar as coordenadas de entrada
    coordenadas_entrada = []

    # Callback quando o mouse dispara um evento
    def ao_clicar(event):
        # Ignora o clique se for fora da malha do plano
        if event.xdata is None or event.ydata is None:
            return 
        
        # Captura da Entrada (Dispositivo Localizador)
        x, y = event.xdata, event.ydata
        coordenadas_entrada.append([x, y])
        print(f"Entrada do Mouse --> Coordenada : ({x:.2f}, {y:.2f})")
        
        # Desenha o Ponto onde o usuário clicou
        ax.plot(x, y, 'ro') # 'ro' = Red circle (ponto vermelho)
        fig.canvas.draw() # Atualiza o Framebuffer (Saída)

        # Se encontrar os 3 pontos, desenha o Polígono (Triângulo)
        if len(coordenadas_entrada) == 3:
            print("3 pontos lidos! Desenhando a primitiva de Polígono...")
            
            triangulo = patches.Polygon(
                coordenadas_entrada, 
                closed=True, 
                fill=True, 
                color='green', 
                alpha=0.6,
                edgecolor='red',
                linewidth=3
            )
            
            ax.add_patch(triangulo)
            fig.canvas.draw()
            
            # Limpa a memória para desenhar o próximo triângulo
            coordenadas_entrada.clear()

    # Aqui Cria o "Ouvinte" que conecta o mouse à função ao_clicar
    fig.canvas.mpl_connect('button_press_event', ao_clicar)

    print("Aguardando entrada do usuário na interface gráfica...")
    plt.show()

if __name__ == "__main__":
    main()