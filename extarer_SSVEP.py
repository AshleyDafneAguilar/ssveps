import pandas as pd
import numpy as np
from scipy import signal
import os

def aplicar_filtros(data, fs=250.0):
    """
    Aplica filtros para limpiar la señal de SSVEP.
    1. Filtro Pasa-altos a 5 Hz (elimina deriva y bajas frecuencias).
    2. Filtro Notch a 60 Hz (elimina la interferencia de la red eléctrica).
    """
    # 1. Filtro pasa-altos (elimina frecuencias menores a 5 Hz)
    b_hp, a_hp = signal.butter(4, 5.0, btype='high', fs=fs)
    data_filt = signal.filtfilt(b_hp, a_hp, data)
    
    # 2. Filtro Notch (elimina ruido de línea de 60 Hz)
    q = 30.0 # Factor de calidad
    b_notch, a_notch = signal.iirnotch(60.0, q, fs=fs)
    data_filt = signal.filtfilt(b_notch, a_notch, data_filt)
    
    return data_filt

def extraer_ssvep():
    """
    Lee los 5 archivos CSV de 9 canales y extrae únicamente el canal que 
    contiene la señal de SSVEP. Luego, aplica filtros de limpieza.
    """
    # Asumimos 250 Hz (estándar para Cyton OpenBCI), modifícalo si tu equipo usa otra.
    frecuencia_muestreo = 250.0 
    
    for i in range(1, 6):
        archivo_entrada = f"senal{i}_9canales.csv"
        archivo_salida = f"senal{i}_ssvep.csv"
        
        if not os.path.exists(archivo_entrada):
            print(f"El archivo {archivo_entrada} no existe. Se omite.")
            continue
            
        try:
            df = pd.read_csv(archivo_entrada)
            
            # Buscar automáticamente el canal SSVEP
            canal_ssvep = "Canal_8"
            for col in df.columns:
                if col == "Canal_9":
                    continue
                datos = df[col].iloc[1:]
                if datos.median() > -100000 and datos.median() < 100000:
                    canal_ssvep = col
                    break
                    
            print(f"[{archivo_entrada}] Señal extraída del: {canal_ssvep}. Procesando y filtrando...")
            
            # Extraemos la señal del canal
            senal_cruda = df[canal_ssvep].values
            
            # Aplicamos los filtros
            senal_filtrada = aplicar_filtros(senal_cruda, fs=frecuencia_muestreo)
            
            # Formateamos el resultado
            df_ssvep = pd.DataFrame({canal_ssvep: senal_filtrada})
            
            # Guardamos el CSV ya limpio
            df_ssvep.to_csv(archivo_salida, index=False)
            
        except Exception as e:
            print(f"Hubo un error procesando {archivo_entrada}: {e}")

if __name__ == "__main__":
    extraer_ssvep()
