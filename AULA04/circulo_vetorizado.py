def main():
    print("Iniciando a síntese do círculo vetorial...")
    
    # Observe que as propriedades matemáticas continuam sendo exatamente as mesmas!
    largura_tela = 300
    altura_tela = 300
    centro_x = 150
    centro_y = 150
    raio = 50
    cor_preenchimento = "red"
    
    # O que muda é a construção do Vetor no lugar de  Pixels
    # Observe que não varremos uma grade. Nós escrevemos uma "formular" (XML/SVG) 
    # que os navegadores ou softwares de CAD/Design conseguem ler.
    codigo_vetorial_svg = f"""<svg width="{largura_tela}" height="{altura_tela}" xmlns="http://www.w3.org/2000/svg">
                                <rect width="100%" height="100%" fill="white" />
                                
                                <circle cx="{centro_x}" cy="{centro_y}" r="{raio}" fill="{cor_preenchimento}" />
                            </svg>"""

    # Agora só salvar  a string de texto com a extensão .svg
    nome_arquivo = "circulo_vetorizado.svg"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo_vetorial_svg)
        
    print(f"Arquivo vetorial gerado: '{nome_arquivo}'.")
    print("Só abrir este arquivo diretamente no navegador para ver o resultado!")

if __name__ == "__main__":
    main()