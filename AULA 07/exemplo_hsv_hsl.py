import colorsys
from PIL import Image

def exemplo_hsv_para_rgb():
    """ Demonstra a facilidade de alterar uma cor girando seu Matiz (Hue) """
    print("--- Conversão HSV para RGB ---")
    
    # 1. Definimos um Matiz (120 graus = Verde). 
    # Em colorsys, Hue é normalizado de 0.0 a 1.0 (120/360 = 0.33)
    h, s, v = 120 / 360.0, 1.0, 1.0 
    
    # colorsys retorna floats entre 0 e 1
    r_float, g_float, b_float = colorsys.hsv_to_rgb(h, s, v)
    
    # Convertendo para a escala discreta de 8 bits (0-255) da memória de vídeo
    r, g, b = int(r_float * 255), int(g_float * 255), int(b_float * 255)
    print(f"O HSV ({h:.2f}, {s}, {v}) virou o RGB: ({r}, {g}, {b})")

