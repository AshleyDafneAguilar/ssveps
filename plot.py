import numpy as np
import matplotlib.pyplot as plt

def graficar_espectro(senal, fs=250.0, n_senal=1):
    muestras_a_ignorar = int(fs * 1.0) 
    senal_estable = senal[muestras_a_ignorar:]

    n = len(senal_estable)
    # Calcular la FFT
    freqs = np.fft.rfftfreq(n, d=1/fs)
    espectro = np.abs(np.fft.rfft(senal_estable))
    
    # Definir las frecuencias de interés
    f_objetivos = [6, 6.6, 7.5, 8.5]
    nombres = ['Encender (6Hz)', 'Apagar (6.6Hz)', 'Subir T (7.5Hz)', 'Bajar T (8.5Hz)']
    
    plt.figure(figsize=(12, 5))
    
    # Gráfica en el tiempo (Canal 8 filtrado)
    plt.subplot(1, 2, 1)
    t = np.arange(n) / fs
    plt.plot(t, senal_estable, color='blue')
    plt.title(f'Señal {n_senal} - Canal 8 (Corteza Visual)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud (uV)')
    
    # Gráfica en la frecuencia (Espectro)
    plt.subplot(1, 2, 2)
    plt.plot(freqs, espectro, color='red')
    
    # Resaltar área de interés (SSVEP suele estar en frecuencias bajas)
    plt.xlim(2, 15) 
    plt.title(f'Espectro de Frecuencia - Señal {n_senal}')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    
    # Dibujar líneas guía para las frecuencias del ejercicio
    for f, label in zip(f_objetivos, nombres):
        plt.axvline(x=f, color='green', linestyle='--', alpha=0.5)
        
    plt.tight_layout()
    nombre_imagen = f'señal_{n_senal}.png'
    plt.savefig(nombre_imagen, dpi=300)
    print(f"Gráfica guardada como: {nombre_imagen}")
    plt.close()

def generar_graficas():
    print("Generando gráficas espectrales...")
    # Ejecutar para las 5 señales
    for i in range(1, 6):
        try:
            # Cargamos el archivo .npy que generamos en el paso anterior
            data = np.load(f'senal{i}_filtrada.npy')
            graficar_espectro(data, n_senal=i)
        except FileNotFoundError:
            print(f"No se encontró el archivo filtrado para la señal {i}")

if __name__ == "__main__":
    generar_graficas()