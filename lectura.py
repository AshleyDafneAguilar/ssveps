import pandas as pd

import os
import subprocess

def procesar_archivos_rar(rar_path='senales.rar'):
    # Extraer el contenido
    print(f"Extrayendo archivos de {rar_path}...")
    try:
        from unrar import rarfile
        with rarfile.RarFile(rar_path) as rf:
            rf.extractall()
    except Exception as e:
        print(f"Error detectado al intentar usar la librería python (puede faltar libunrar.so): {e}")
        print("Intentando extracción mediante comando por defecto en Bash...")
        try:
            subprocess.run(['unrar', 'e', '-y', rar_path], check=True)
        except Exception as e_sub:
            print("No se encontró comando de sistema unrar:", e_sub)
            try:
                subprocess.run(['./rar/unrar', 'e', '-y', rar_path], check=True)
            except Exception as e_local:
                pass
            print("Extracción finalizada (asumiendo que los archivos ya pueden estar en el directorio).")

    # Procesar los 5 archivos CSV
    for i in range(1, 6):
        nombre_archivo = f'senal{i}.csv'
        nombre_salida = f'senal{i}_9canales.csv'
        
        if os.path.exists(nombre_archivo):
            print(f"Procesando {nombre_archivo}...")
            # Leer el CSV sin encabezado. El original suele tener 10 filas continuas
            df = pd.read_csv(nombre_archivo, header=None)
            
            # Tomamos las últimas 9 filas (ignorando el tiempo/baseline) y trasponemos 
            # Si el csv vino con formato largo, tomamos las últimas 9 columnas.
            if df.shape[0] >= 9 and df.shape[1] > df.shape[0]:
                df_canales = df.iloc[-9:, :].T
            else:
                df_canales = df.iloc[:, -9:]
                
            # Nombrar los canales
            df_canales.columns = [f'Canal_{j}' for j in range(1, 10)]
            
            # Guardar el CSV procesado
            df_canales.to_csv(nombre_salida, index=False)
            print(f"Guardado exitosamente {nombre_salida} con {df_canales.shape[0]} datos por canal.")
        else:
            print(f"Archivo {nombre_archivo} no encontrado después de la extracción.")

if __name__ == "__main__":
    procesar_archivos_rar()
