from firebase.conexion import db

def subir_producto(producto, codigo_barras):
    db.collection("productos").document(codigo_barras).set(producto.to_dict())
    print(f"Producto subido: {producto.nombre} (ID: {codigo_barras})")
