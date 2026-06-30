def main():
    print("Tela Vetorial em Modo Texto...")
    # Define o tamanho do "monitor"
    largura = 10
    altura = 10
    
    # Cria uma matriz (tela em branco, preenchida com um caractere de ponto '.')
    tela = [['.' for _ in range(largura)] for _ in range(altura)]
    
    # Definimos a primitiva de um retângulo
    inicio_x = 2
    fim_x = 7
    inicio_y = 3
    fim_y = 6
    
    # Processo de "rasterização simplificado"
    # percorrer a matriz e substituir o '.' por um bloco '#' onde o retângulo existe
    for y in range(altura):
        for x in range(largura):
            # Se a coordenada atual estiver dentro da caixa delimitadora do retângulo
            if inicio_x <= x <= fim_x and inicio_y <= y <= fim_y:
                tela[y][x] = '#'
                
    # Processo de renderização
    for linha in tela:
        # A função join() junta todos os itens da linha 
        # em uma única string separada por espaços
        print(" ".join(linha))
        
    print("\nFim do desenho.")

if __name__ == "__main__":
    main()