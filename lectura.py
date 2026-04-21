import pandas as pd
import os
import subprocess
import numpy as np

def procesar_archivos_rar(rar_path='senales.rar'):
    print(f"Extrayendo archivos de {rar_path}...")
    
    # Agregar la ruta local donde descargamos el binario para no requerir permisos sudo de apt
    import sys
    os.environ["PATH"] += os.pathsep + os.path.join(os.path.dirname(__file__), 'rar')

    try:
        # Intento de extracción usando el binario unrar (sistema o local)
        subprocess.run(['unrar', 'e', '-y', rar_path], check=True)
    except Exception as e:
        print(f"Error con unrar de sistema: {e}. Intentando otros métodos...")
        try:
            subprocess.run(['rar', 'e', '-y', rar_path], check=True)
        except Exception as e2:
            print(f"Fallo extracción rar por comando: {e2}. Usando rarfile si disponible.")
            try:
                from unrar import rarfile
                with rarfile.RarFile(rar_path) as rf:
                    rf.extractall()
            except:
                print("Asegúrate de tener rar instalado o los archivos ya extraídos en la carpeta.")

    # Procesar los 5 archivos CSV solicitados
    for i in range(1, 6):
        nombre_archivo = f'senal{i}.csv'
        nombre_salida = f'senal{i}_procesada.csv'
        
        if os.path.exists(nombre_archivo):
            print(f"--- Procesando {nombre_archivo} ---")
            
            # Cargamos el archivo. 
            df_raw = pd.read_csv(nombre_archivo, header=None)
            
            # Lógica de extracción de los canales
            # En EEG la cantidad de muestras de tiempo es mayor a la cantidad de canales (tiempo >> canales)
            if df_raw.shape[0] >= df_raw.shape[1]:
                # Los datos están en forma (Muestras, Canales)
                df_canales = df_raw.iloc[:, -9:]
            else:
                # Si los datos están transpuestos (Canales, Muestras), trasponemos para obtener columnas
                df_canales = df_raw.T.iloc[:, -9:]

            # Renombrar columnas para identificar el Canal (p.ej "Canal_8")
            df_canales.columns = [f'Canal_{j}' for j in range(1, 10)]
            
            # Guardamos una copia limpia para trabajar
            df_canales.to_csv(nombre_salida, index=False)
            
        else:
            print(f"Error: No se encontró {nombre_archivo}. Revisa la extracción del .rar.")

if __name__ == "__main__":
    procesar_archivos_rar()