import spectral
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Cargar la imagen en formato ENVI
ruta = 'C:/Users/cignu/Desktop/2025-30-09 imago/Original/'
entrada = '001-2025-09-30-14hr58min_I-399.873ms'
salida = 'new_hyperspectral_image_RGB'

archivo_hdr = ruta + entrada + '.hdr'
archivo_raw = ruta + entrada + '.cube'

image = spectral.envi.open(archivo_hdr, archivo_raw)

#view = spectral.imshow(image, (53, 36, 20))

# Obtener una matriz numpy de la imagen
data = image.load()

# Mostrar información sobre la imagen
print('Dimensiones de la imagen:', data.shape)
print('Número de bandas:', image.nbands)
print('Número de filas:', image.nrows)
print('Número de columnas:', image.ncols)

# Elegir las bandas para la imagen RGB (ajusta los índices según tus necesidades)
#rgb_bands = [53, 36, 20]  # Ejemplo de bandas

rgb_bands = [90, 90, 90]  # Ejemplo de bandas


# Seleccionar las bandas RGB
rgb_image = data[:, :, rgb_bands].astype(np.float32)

# Calcular el mínimo y máximo de toda la imagen (no solo por canal)
min_val = 0
print(f"Valor mínimo: {min_val}")
max_val = 500
print(f"Valor máximo: {max_val}")

# Normalizar los valores usando el mismo mínimo y máximo para todos los canales
rgb_image -= min_val
rgb_image /= max_val

# Ajustar los coeficientes de ganancia para cada canal
#ganancia_r = 1.2  # Coeficiente de ganancia para el canal rojo
#ganancia_g = 1  # Coeficiente de ganancia para el canal verde
#ganancia_b = 1.4  # Coeficiente de ganancia para el canal azul


# Ajustar los coeficientes de ganancia para cada canal
ganancia_r = 1  # Coeficiente de ganancia para el canal rojo
ganancia_g = 1  # Coeficiente de ganancia para el canal verde
ganancia_b = 1  # Coeficiente de ganancia para el canal azul




# Aplicar los coeficientes de ganancia
rgb_image[:, :, 0] *= ganancia_r
rgb_image[:, :, 1] *= ganancia_g
rgb_image[:, :, 2] *= ganancia_b

# Asegurarse de que los valores estén en el rango [0, 1]
rgb_image = np.clip(rgb_image, 0, 1)

# Convertir la imagen a formato de 8 bits (0-255)
rgb_image = (rgb_image * 255).astype(np.uint8)


rgb_image_t = np.transpose(rgb_image, axes = (1,0,2))
# Rotar la imagen 90 grados en sentido horario
rgb_image_rotada = np.rot90(rgb_image_t, k=2)  # k=-1 para 90 grados en sentido horario

# Función para mostrar el espectro al hacer clic
def on_click(event):
    if event.inaxes is not None:
        x, y = int(event.xdata), int(event.ydata)
        print(x,y)
        if 0 <= x < data.shape[1] and 0 <= y < data.shape[0]:  # Verificar que el clic está dentro de la imagen
            espectro = data[y, x, :]  # Seleccionar el espectro del píxel
            varx = range(1,333,1)
            plt.figure()
            plt.plot(varx,espectro)
            plt.xlabel('Bandas')
            plt.ylabel('Reflectancia')
            plt.title(f'Espectro del píxel ({x}, {y})')
            plt.show()
        else:
            print(f"Clic fuera de los límites de la imagen: ({x}, {y})")

# Mostrar la imagen RGB ajustada en una ventana interactiva
fig, ax = plt.subplots()
ax.imshow(rgb_image_rotada)
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
