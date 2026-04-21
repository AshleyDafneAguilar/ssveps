import pandas as pd
import matplotlib.pyplot as plt
import os

def plotear_senales():
    # Creamos una figura con 5 subgráficas (una por cada señal)
    fig, axs = plt.subplots(5, 1, figsize=(12, 12), sharex=True)
    fig.suptitle("Señales SSVEP Filtradas (Canal 8)", fontsize=16)
    
    fs = 250.0  # Frecuencia de muestreo asumida
    
    for i in range(1, 6):
        archivo = f"senal{i}_ssvep.csv"
        ax = axs[i-1]
        
        if os.path.exists(archivo):
            try:
                df = pd.read_csv(archivo)
                datos = df.iloc[:, 0].values
                # Crear vector de tiempo (en segundos)
                tiempo = [t / fs for t in range(len(datos))]
                
                ax.plot(tiempo, datos, color='tab:blue', linewidth=0.8)
                ax.set_title(f"Archivo: {archivo}")
                ax.set_ylabel("Amplitud")
                ax.grid(True, linestyle='--', alpha=0.7)
            except Exception as e:
                ax.text(0.5, 0.5, f"Error leyendo {archivo}: {e}", 
                        ha='center', va='center', transform=ax.transAxes)
        else:
            ax.text(0.5, 0.5, f"Archivo {archivo} no encontrado", 
                    ha='center', va='center', transform=ax.transAxes)
    
    axs[-1].set_xlabel("Tiempo (segundos)")
    plt.tight_layout()
    # Ajustamos para el título superior
    plt.subplots_adjust(top=0.95)
    
    # Guardar en caso de no tener interfaz gráfica disponible
    nombre_salida = "plot_senales_ssvep.png"
    plt.savefig(nombre_salida, dpi=300)
    print(f"Gráfica general guardada como: {nombre_salida}")
    
    # Mostrar en ventana interactiva
    try:
        print("Mostrando gráfica en ventana interactiva (cierra la ventana para continuar)...")
        plt.show()
    except Exception as e:
        print(f"No se pudo mostrar la interfaz gráfica ({e}). Pero la imagen ha sido guardada.")

if __name__ == "__main__":
    plotear_senales()
