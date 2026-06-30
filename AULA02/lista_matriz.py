# Listas (Arrays)
cores = ["Vermelho", "Verde", "Azul"]
print(cores[0]) # primeiro elemento

cores.append("Amarelo") # Adiciona ao final da lista
print(f"Minha lista tem {len(cores)} cores.") # len() tamanho da lista

# Matrizes (Listas dentro de Listas)
# Isso é exatamente como uma tela de pixels funciona!
matriz_3x3 = [
    [1, 2, 3], # Linha 0
    [4, 5, 6], # Linha 1
    [7, 8, 9]  # Linha 2
]

# Pegar o número 6 
print(f"Elemento central direito: {matriz_3x3[1][2]}")