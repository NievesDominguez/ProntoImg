import pandas as pd
from modelos.producto import Producto
from firebase.productos import subir_producto
from utils.validaciones import validar_fila
import unicodedata

from utils.git_tools import subir_archivo_a_github
import os


# Carpeta donde están las imágenes locales
CARPETA_IMAGENES_LOCAL = "img"

# Ruta local al repositorio clonado, carpeta img
REPO_LOCAL_IMG = r"E:\DAM\Proyecto Final\ProntoImg-main\img"

# URL base RAW de GitHub para imágenes subidas
REPO_URL_BASE = "https://raw.githubusercontent.com/NievesDominguez/ProntoImg/main/img"


# ---------------------------------------------------------
# Procesar alérgenos desde el Excel
# ---------------------------------------------------------
def procesar_alergenos(texto):
    """
    Procesa el campo 'Alérgenos' del Excel.
    - Lo que va antes del punto son alérgenos que contiene.
    - Lo que va después del punto son trazas.
    - Las comas separan elementos.
    """
    if pd.isna(texto) or str(texto).strip() == "":
        return [], []

    texto = str(texto).strip()

    if "." in texto:
        parte_contiene, parte_trazas = texto.split(".", 1)
    else:
        parte_contiene = texto
        parte_trazas = ""

    contiene = [a.strip() for a in parte_contiene.split(",") if a.strip()]
    trazas = [a.strip() for a in parte_trazas.split(",") if a.strip()]

    return contiene, trazas


# Cargar datos desde Excel
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

    # Recorrer filas del Excel
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

        imagen_excel = row["imagen"]

        # Determinar si la imagen es URL o archivo local
        if imagen_excel.startswith("http://") or imagen_excel.startswith("https://"):
            # Si es URL, no se sube nada a GitHub
            print(f"Imagen es URL, no se sube a GitHub: {imagen_excel}")
            imagen_final = imagen_excel

        else:
            # Imagen local: se sube a GitHub si existe
            ruta_local = os.path.join(CARPETA_IMAGENES_LOCAL, imagen_excel)

            if os.path.exists(ruta_local):
                subir_archivo_a_github(
                    ruta_local=ruta_local,
                    repo_destino=REPO_LOCAL_IMG,
                    mensaje_commit=f"Subida automática de {imagen_excel}"
                )

                # Generar url  para Firestore
                imagen_final = f"{REPO_URL_BASE}/{imagen_excel}"
                print(f"URL RAW generada: {imagen_final}")

            else:
                print(f"La imagen local no existe: {ruta_local}")
                imagen_final = imagen_excel

        # Procesar alérgenos
        alergenos_contiene, alergenos_trazas = procesar_alergenos(row.get("alergenos"))
        
        # Procesar iva  
        iva_valor = row.get("iva")  
        if pd.isna(iva_valor):  
            iva = None  
        else:  
            # Convertir a entero  
            iva_str = str(iva_valor).replace("%", "").strip()  
            try:  
                iva = int(float(iva_str))  
            except:  
                iva = None  
                print(f"⚠️ IVA no válido en fila {index+2}: {iva_valor}")  
          
        # Procesar al_peso  
        alpeso_valor = row.get("alpeso")  
        if pd.isna(alpeso_valor):  
            al_peso = None  
        else:  
            alpeso_str = str(alpeso_valor).strip().lower()  
            if alpeso_str == "true":  
                al_peso = True  
            else:  
                al_peso = None  
          
        # Crear el producto con la URL final y los alérgenos  
        producto = Producto(  
            nombre=row["nombre"],  
            descripcion=row["descripcion"],  
            precio=float(str(row["precio"]).replace(",", ".")),  
            categoria=row["categoria"],  
            subcategoria=row["subcategoria"],  
            stock=int(row["stock"]),  
            imagen_url=imagen_final,  
            oferta=row["oferta"] if "oferta" in row and not pd.isna(row["oferta"]) else None,  
            cantidad=float(str(row["cantidad"]).replace(",", ".")),  
            unidad=row["unidad"],  
            ubicacion=row["ubicacion"] if "ubicacion" in row and not pd.isna(row["ubicacion"]) else None,  
            alergenos_contiene=alergenos_contiene,  
            alergenos_trazas=alergenos_trazas,  
            iva=iva,  
            al_peso=al_peso  
        )

        # Subir a Firestore
        subir_producto(producto, codigo)

    # ---------------------------------------------------------
    # Resumen final
    # ---------------------------------------------------------
    print("\n──────── RESULTADO FINAL ────────")

    if errores_globales:
        print("Algunos productos NO se subieron:")
        for e in errores_globales:
            print(f"  - Fila {e['fila']} ({e['nombre']}): {', '.join(e['errores'])}")
    else:
        print("Todos los productos se subieron correctamente")


if __name__ == "__main__":
    cargar_desde_excel("data/DatosFirestore.xlsx")
