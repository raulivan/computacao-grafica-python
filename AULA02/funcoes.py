# Definindo Funções
def calcular_area_retangulo(base, altura):
    area = base * altura
    return area

# Método principal (Main)
def main():
    b = 10
    h = 5
    resultado = calcular_area_retangulo(b, h)
    print(f"A área de um retângulo {b}x{h} é {resultado}.")

if __name__ == "__main__":
    main()
