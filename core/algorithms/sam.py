from core import np,Image,plt,sp, envi, pl
from core.path import getPath
import os
import math
class SAM:
    def __init__(self, pathFiles:list, bands:tuple):
        self.umbral_angulos = [0.12, 0.12]  # Umbrals
        self.colores_rgb = [[1, 0, 0], [0, 1, 0]]  # RGB colors
        self.inputFiles = pathFiles
        self.hdr = None
        self.float = None
        self.pigments = None
        self.bands = bands
        self.data = []
        self.numberBand = 30
        self.band = None
        self.result_img = None
    def setup_angles(self,*args) ->list:
        if len(args) == len(self.colores_rgb):
            self.umbral_angulos = []
            for i in args:
                self.umbral_angulos.append(i)
        return self.umbral_angulos
    def setup_rgb_colors(self,dim:int):
        if dim >0:
            self.colores_rgb = []
            pass # To do

    def showGray(self, image):
        self.band = image.read_band(self.numberBand)
        plt.imshow(self.band, cmap='gray')
        plt.title(f"Banda {self.numberBand}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.savefig("gray.png")
        plt.show()

    def showRGB(self, image):
        rgb = image.read_bands(self.bands)
        sp.imshow(rgb)
        plt.title(f'Imagen RGB (Bandas {self.bands})')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.savefig("rgb.png")
        plt.show()

    def calculate_angular_spectral(self, pixel_spectrum, reference_spectrum):
        min_len = min(len(pixel_spectrum), len(reference_spectrum)) 
        pixel_spectrum = pixel_spectrum[:min_len] 
        reference_spectrum = reference_spectrum[:min_len]
        dot_product = np.dot(pixel_spectrum, reference_spectrum)
        norm_pixel = np.linalg.norm(pixel_spectrum)
        norm_ref = np.linalg.norm(reference_spectrum)
        if norm_pixel == 0 or norm_ref == 0:
            return np.pi
        return math.acos(dot_product / (norm_pixel * norm_ref))

    def spectral_angle_mapper_cpu(self, img_data, reference_spectra):
        alto, ancho, _ = img_data.shape
        self.result_img = np.zeros((alto, ancho, 3), dtype=np.float32)

        for i in range(alto):
            for j in range(ancho):
                pixel_spectrum = img_data[i, j]
                for s, reference_spectrum in enumerate(reference_spectra):
                    angle = self.calculate_angular_spectral(pixel_spectrum, reference_spectrum)
                    if angle < self.umbral_angulos[s]:
                        self.result_img[i, j] = self.colores_rgb[s]
                        break
        return self.result_img

    def samMethodShow(self):
        path = getPath()
        a,b,csv_file= path.SAMInputFiles(self.inputFiles)
        a,b,csv_file = "".join(a),"".join(b),"".join(csv_file)
        img = envi.open(a, image=b)
        print("Imagen cargada:", img)
        self.showGray(img)
        self.showRGB(img)

        spectro_csv = csv_file
        df = pl.read_csv(spectro_csv, has_header=False)
        reference_spectra = df.to_numpy().T
        reference_spectra = np.ascontiguousarray(reference_spectra)

        img_data = img.load().astype(np.float32)
        self.result_img = self.spectral_angle_mapper_cpu(img_data, reference_spectra)

        plt.imshow(self.result_img)
        plt.title('Mapeo por Ángulo Espectral (SAM)')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

        result_img_uint8 = (self.result_img * 255).astype(np.uint8)
        result_image_pil = Image.fromarray(result_img_uint8)
        output_path = path.unionPath('resultado_SAM.png')
        result_image_pil.save(output_path)
        print(f'Imagen resultado guardada en: {output_path}')
