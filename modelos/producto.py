from datetime import datetime    
  
class Producto:    
    def __init__(self, nombre, descripcion, precio, categoria, subcategoria, stock,    
                 imagen_url, oferta, cantidad, unidad, ubicacion,    
                 alergenos_contiene=None, alergenos_trazas=None, iva=None, al_peso=None):    
  
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
        self.alergenos_contiene = alergenos_contiene or []    
        self.alergenos_trazas = alergenos_trazas or []    
        self.iva = iva    
        self.al_peso = al_peso    
  
    def to_dict(self):    
        data = {    
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
            "ubicacion": self.ubicacion,    
            "alergenos_contiene": self.alergenos_contiene,    
            "alergenos_trazas": self.alergenos_trazas,  
            "iva": self.iva  
        }    
            
        # Solo incluir al_peso si es True para evitar almacenar None o False, que no se usan
        if self.al_peso is True:    
            data["al_peso"] = self.al_peso    
                
        return data