import pandas as pd
from modelos.producto import Producto
from firebase.productos import subir_producto
from utils.validaciones import validar_fila
from utils.git_tools import subir_archivo_a_github
import unicodedata
import os

CARPETA_IMAGENES_LOCAL = "img"
REPO_LOCAL_IMG = "C:\\Users\\mnieves.domnav\\DAM\\Proyecto_Python\\img"
REPO_URL_BASE = "https://github.com/NievesDominguez/ProntoImg/blob/main/img"

def cargar_desde_excel(ruta_excel):
    df = pd.read_excel(ruta_excel)

    def normalizar_columna(col):
        col = col.strip().lower().replace(" ", "")
        col = ''.join(
            c for c in unicodedata.normalize('NFD', col)
            if unicodedata.category(c) != 'Mn'
        )
        return col

    df.columns = [normalizar_columna(c) for c in df.columns]

    errores_globales = []
    codigos_existentes = set()

    for index, row in df.iterrows():
        codigo = str(row["codigobarras"]).strip()
        errores = validar_fila(row, codigos_existentes)

        if errores:
            errores_globales.append({
                "fila": index + 2,
                "errores": errores,
                "nombre": row.get("nombre", "Desconocido")
            })
            print(f"Producto en fila {index + 2} NO subido: {errores}")
            continue

        codigos_existentes.add(codigo)

        nombre_imagen = row["imagen"]
        ruta_local = os.path.join(CARPETA_IMAGENES_LOCAL, nombre_imagen)

        # Subir imagen a GitHub
        subida_ok = subir_archivo_a_github(
            ruta_local=ruta_local,
            repo_destino=REPO_LOCAL_IMG,
            mensaje_commit=f"Subida automática de {nombre_imagen}"
        )

        # Mostrar URL por consola
        if subida_ok:
            url_imagen = f"{REPO_URL_BASE}/{nombre_imagen}?raw=1"
            print(f"URL pública de la imagen: {url_imagen}")
        else:
            print(f"No se pudo subir la imagen {nombre_imagen}")

        # Crear producto SIN imagen_url
        producto = Producto(
            nombre=row["nombre"],
            descripcion=row["descripcion"],
            precio=float(str(row["precio"]).replace(",", ".")),
            categoria=row["categoria"],
            subcategoria=row["subcategoria"],
            stock=int(row["stock"]),
            oferta=row["oferta"] if "oferta" in row and not pd.isna(row["oferta"]) else None,
            cantidad=float(str(row["cantidad"]).replace(",", ".")),
            unidad=row["unidad"],
            ubicacion=row["ubicacion"] if "ubicacion" in row and not pd.isna(row["ubicacion"]) else None
        )

        subir_producto(producto, codigo)

    print("\n──────── RESULTADO FINAL ────────")

    if errores_globales:
        print("Algunos productos NO se subieron:")
        for e in errores_globales:
            print(f"  - Fila {e['fila']} ({e['nombre']}): {', '.join(e['errores'])}")
    else:
        print("Todos los productos se subieron correctamente")

if __name__ == "__main__":
    cargar_desde_excel("data/DatosFirestore.xlsx")
