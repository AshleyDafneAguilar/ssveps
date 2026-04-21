import argparse
from lectura import procesar_archivos_rar
from preprocesamiento import preprocesar_senales
from plot import generar_graficas

def main():
    parser = argparse.ArgumentParser(description="Flujo de lectura y procesamiento de bioseñales.")
    parser.add_argument("rar_path", type=str, help="Ruta al archivo .rar con las señales CSV.")
    args = parser.parse_args()

    procesar_archivos_rar(args.rar_path)
    preprocesar_senales()
    generar_graficas()


if __name__ == "__main__":
    main()
