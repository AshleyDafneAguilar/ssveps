import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
import os

def aplicar_filtros(data, fs=250.0):
    # 1. Filtro Notch para eliminar los 60 Hz (Ruido eléctrico)
    f0 = 60.0  # Frecuencia a eliminar
    Q = 30.0   # Factor de calidad
    b_notch, a_notch = iirnotch(f0, Q, fs)
    filtrada_notch = filtfilt(b_notch, a_notch, data)
    
    # 2. Filtro Pasa-Altas (Butterworth) para eliminar de 0 a 5 Hz
    # El documento dice que el ruido está en ese rango, así que cortamos en 5Hz
    f_corte = 5.0
    nyquist = 0.5 * fs
    low = f_corte / nyquist
    b_hi, a_hi = butter(4, low, btype='high')
    senal_final = filtfilt(b_hi, a_hi, filtrada_notch)
    
    return senal_final

def preprocesar_senales():
    print("Iniciando preprocesamiento de las señales (Canal 8)...")
    # Procesar cada archivo generado en el paso anterior
    for i in range(1, 6):
        archivo_in = f'senal{i}_procesada.csv'
        if os.path.exists(archivo_in):
            print(f"--- Preprocesando {archivo_in} ---")
            df = pd.read_csv(archivo_in)
            
            # Extraemos el Canal 8 (Corteza Visual)
            señal_ssvep = df['Canal_8'].values
            
            # Aplicamos la limpieza
            señal_limpia = aplicar_filtros(señal_ssvep, fs=250.0)
            
            # Guardamos la señal filtrada para el análisis de frecuencia 
            np.save(f'senal{i}_filtrada.npy', señal_limpia)
            #print(f"Señal {i} filtrada y guardada como .npy")

if __name__ == "__main__":
    preprocesar_senales()