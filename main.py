import pandas as pd
from modelos.producto import Producto
from firebase.productos import subir_producto
from utils.validaciones import validar_fila
import unicodedata

from utils.git_tools import subir_archivo_a_github
import os

CARPETA_IMAGENES_LOCAL = "img"
REPO_LOCAL_IMG = r"C:\Users\mnieves.domnav\DAM\Proyecto_Python\img"
REPO_URL_BASE = "https://github.com/NievesDominguez/ProntoImg/blob/main/img"

def cargar_desde_excel(ruta_excel):
    df = pd.read_excel(ruta_excel)

    # Normalizar nombres de columnas
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

        subida_ok = subir_archivo_a_github(
            ruta_local=ruta_local,
            repo_destino=REPO_LOCAL_IMG,
            mensaje_commit=f"Subida automática de {nombre_imagen}"
        )

        if subida_ok:
            url_imagen = f"{REPO_URL_BASE}/{nombre_imagen}?raw=1"
            print(f"URL pública de la imagen: {url_imagen}")
        else:
            print(f"No se pudo subir la imagen {nombre_imagen}")

        producto = Producto(
            nombre=row["nombre"],
            descripcion=row["descripcion"],
            precio=float(str(row["precio"]).replace(",", ".")),
            categoria=row["categoria"],
            subcategoria=row["subcategoria"],
            stock=int(row["stock"]),
            imagen_url=row["imagen"],  # <-- LO DEJO TAL CUAL LO TENÍAS
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
