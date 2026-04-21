import pandas as pd
import numpy as np
from scipy import signal
import os

# Mapeo de comandos según la frecuencia SSVEP
TARGET_FREQS = {
    6.0: "ON",
    6.6: "APAGAR",
    7.5: "SUBIR TEMPERATURA",
    8.5: "BAJA TEMPERATURA"
}

def analizar_senal(archivo, fs=250.0):
    """
    Calcula la Densidad Espectral de Potencia (PSD) y encuentra 
    la señal predominante relacionada con SSVEP para clasificarla.
    """
    try:
        df = pd.read_csv(archivo)
        # La señal está en la única columna disponible
        datos = df.iloc[:, 0].values
        
        # Calcular la FFT / PSD utilizando el método de Welch
        # Usamos ventanas largas para tener buena resolución frecuencial (~0.25Hz de resolución con 4 segs)
        nperseg = min(len(datos), int(fs * 4)) 
        f, pxx = signal.welch(datos, fs=fs, nperseg=nperseg)
        
        # Nos interesa buscar picos en el rango de frecuencias de nuestras luces (de 5.5 a 9.0 Hz)
        mascara = (f >= 5.5) & (f <= 9.0)
        f_rango = f[mascara]
        pxx_rango = pxx[mascara]
        
        # Encontrar la frecuencia con la mayor potencia en ese rango
        freq_predominante = f_rango[np.argmax(pxx_rango)]
        
        # Encontrar a qué frecuencia SSVEP se parece más
        closest_target = min(TARGET_FREQS.keys(), key=lambda k: abs(k - freq_predominante))
        comando = TARGET_FREQS[closest_target]
        
        return freq_predominante, closest_target, comando
        
    except Exception as e:
        print(f"Error procesando el archivo {archivo}: {e}")
        return None, None, None

def analisis_archivos():
    print("--- Análisis de Frecuencias SSVEP ---")
    
    for i in range(1, 6):
        archivo = f"senal{i}_ssvep.csv"
        if not os.path.exists(archivo):
            print(f"No se encontró: {archivo}")
            continue
            
        freq_exacta, target, comando = analizar_senal(archivo)
        
        if freq_exacta is not None:
            print(f"\nArchivo: {archivo}")
            print(f" Frecuencia Predominante detectada: {freq_exacta:.2f} Hz")
            print(f" Frecuencia Estímulo Asignada: {target} Hz")
            print(f" >>> COMANDO DE SALIDA: {comando} <<<")

if __name__ == "__main__":
    analisis_archivos()
