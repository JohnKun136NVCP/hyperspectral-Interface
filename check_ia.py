import psutil
import torch

def check_resources():
    ram_gb = psutil.virtual_memory().total / (1024**3)
    print(f"RAM disponible: {ram_gb:.2f} GB")
    if ram_gb < 8:
        print("❌ Se requieren al menos 8GB de RAM.")
        return False

    if torch.cuda.is_available():
        print("✅ GPU CUDA detectada.")
    else:
        print("⚠️ No se detectó GPU, el rendimiento será limitado.")

    return True

if __name__ == "__main__":
    if not check_resources():
        exit(1)
