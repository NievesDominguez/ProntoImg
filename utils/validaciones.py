import pandas as pd

def validar_fila(row, codigos_existentes):
    errores = []

    # Código de barras
    codigo = str(row["codigobarras"]).strip()
    if not codigo.isdigit():
        errores.append("Código de barras no válido")
    if codigo in codigos_existentes:
        errores.append("Código de barras duplicado")

    # Nombre
    if pd.isna(row["nombre"]) or str(row["nombre"]).strip() == "":
        errores.append("Nombre vacío")

    # Descripción
    if pd.isna(row["descripcion"]) or str(row["descripcion"]).strip() == "":
        errores.append("Descripción vacía")

    # Precio
    try:
        precio = float(str(row["precio"]).replace(",", "."))
        if precio <= 0:
            errores.append("Precio debe ser mayor que 0")
    except:
        errores.append("Precio no es un número válido")

    # Categoría
    if pd.isna(row["categoria"]) or str(row["categoria"]).strip() == "":
        errores.append("Categoría vacía")

    # Subcategoría
    if pd.isna(row["subcategoria"]) or str(row["subcategoria"]).strip() == "":
        errores.append("Subcategoría vacía")

    # Stock
    try:
        stock = int(row["stock"])
        if stock < 0:
            errores.append("Stock no puede ser negativo")
    except:
        errores.append("Stock no es un número válido")

    # Imagen
    #if pd.isna(row["imagen"]) or not str(row["imagen"]).startswith("http"):
        #errores.append("URL de imagen inválida")
        
    # Cantidad
    try:
        cantidad = float(row["cantidad"])
        if cantidad < 0:
            errores.append("Cantidad no puede ser negativo")
    except:
        errores.append("Cantidad no es un número válido")

    return errores
