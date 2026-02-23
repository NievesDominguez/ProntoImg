from datetime import datetime

class Producto:
    def __init__(self, nombre, descripcion, precio, categoria, subcategoria, stock, imagen_url, oferta, cantidad, unidad, ubicacion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.stock = stock
        self.imagen_url = imagen_url
        self.fecha = datetime.now()
        self.oferta = oferta
        self.cantidad = cantidad
        self.unidad = unidad
        self.ubicacion = ubicacion

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "categoria": self.categoria,
            "subcategoria": self.subcategoria,
            "stock": self.stock,
            "imagenUrl": self.imagen_url,
            "fecha": self.fecha,
            "oferta": self.oferta,
            "cantidad": self.cantidad,
            "unidad": self.unidad,
            "ubicacion": self.ubicacion
        }

