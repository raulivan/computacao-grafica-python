import matplotlib.pyplot as plt
import time

def main():
    print("=== Simulador de FPS (Frames Por Segundo) ===")
    print("Valores: 5 (Travado), 24 (Cinema), 60 (Fluido)")
    
    try:
        # Solicita a entrada do FPS desejado para a simulação
        fps_alvo = int(input("Digite o FPS desejado para a simulação: "))
    except ValueError:
        fps_alvo = 30

    # Calcula o tempo que o processador deve "dormir" entre cada quadro
    delta_time = 1.0 / fps_alvo
    print(f"Iniciando simulação a {fps_alvo} FPS.")
    print(f"Tempo de atualização (Delta Time): {delta_time:.4f} segundos por quadro.")

    # Ativa o Modo Interativo do Matplotlib para permitir atualizar a janela sem travar
    plt.ion()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Criando um plano escuro para a animação
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.set_title(f"Simulação Gráfica rodando a {fps_alvo} FPS", color='white', fontsize=14)
    ax.grid(True, color='white', linestyle='--', alpha=0.3)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    # Limites da tela. Coloquei o X de 0 a 100m que será o caminho da animação e Y fica fixo.
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)

    # Cria Um Ponto ou cirbulo na tela
    objeto, = ax.plot([], [], marker='o', color='red', markersize=20)

    # Aqui começa o laço de rendereização do FPS (GAME LOOP)
    posicao_x = 0
    velocidade = 50 # O objeto anda 50 unidades de espaço por segundo real
    
    # registra o tempo exato em que a animação começa
    tempo_anterior = time.time()

    while posicao_x <= 100:
        # Calcula o tempo real que passou desde o último quadro
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual

        # ATUALIZA A FÍSICA: Posição = Velocidade * Tempo (S = S0 + V*t)
        # Esse ajuste garangte que a velocidade real do objeto seja a mesma, independente do FPS do seu monitor
        posicao_x += velocidade * tempo_decorrido
        """
        ATENÇÃO AQUI NESSA PARTE:
        Na linha= posicao_x += velocidade * tempo_decorrido
        Se não calcular o deslocamento multiplicando pelo tempo_decorrido real da CPU,
        um jogo rodando a 60 FPS faria o personagem correr duas vezes mais rápido do que o mesmo jogo 
        rodando em um computador velho a 30 FPS. 
        Multiplicar pela variação do tempo garante que, matematicamente, a velocidade da geometria 
        no espaço virtual seja idêntica em qualquer hardware, 
        mudando apenas a quantidade de "fotos" (quadros) renderizadas no trajeto.
        """
        
        # Define a nova coordenada do objeto, odne será desenhando o circulo
        objeto.set_data([posicao_x], [5]) # X avança, Y é travado no meio da tela (5)
        
        # RENDERIZA E PAUSA
        # O plt.pause atualiza o Framebuffer na tela e para o loop pelo Delta Time calculado
        plt.pause(delta_time)

    print("Animação concluída.")
    
    # Desliga o modo interativo e mantém a janela aberta no final
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()