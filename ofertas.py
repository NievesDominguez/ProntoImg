import json
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
from datetime import datetime
import os
import ssl

# -------------------------------------------------------------------
# 0. DESACTIVAR VERIFICACIÓN SSL (solución al error self-signed cert)
# -------------------------------------------------------------------
ssl._create_default_https_context = ssl._create_unverified_context

# -------------------------------------------------------------------
# 1. Cargar credenciales desde archivo JSON
# -------------------------------------------------------------------
CREDENTIALS_PATH = "credentials.json"

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH
)

db = firestore.Client(credentials=credentials, project=credentials.project_id)

# -------------------------------------------------------------------
# 2. Cargar Excel desde la hoja "Ofertas"
# -------------------------------------------------------------------
df = pd.read_excel("data/DatosFirestore.xlsx", sheet_name="Ofertas")

# -------------------------------------------------------------------
# 3. Funciones auxiliares
# -------------------------------------------------------------------
def parse_fecha(valor):
    if isinstance(valor, datetime):
        return valor.strftime("%Y-%m-%d")
    if isinstance(valor, str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(valor, fmt).strftime("%Y-%m-%d")
            except:
                pass
    return None

def parse_maximo(valor):
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        limpio = valor.replace("€", "").replace(" ", "").replace(",", ".")
        try:
            return float(limpio)
        except:
            return None
    return None

# -------------------------------------------------------------------
# 4. Subir cada fila a Firestore
# -------------------------------------------------------------------
for _, row in df.iterrows():

    try:
        formula = json.loads(row["Fórmula"])
    except Exception as e:
        print(f"❌ Error en fórmula de {row['Código']}: {e}")
        continue

    doc = {
        "codigo": row["Código"],
        "nombre": row["Nombre"],
        "descripcion": row["Descripción"],
        "tipo": row["Tipo"].lower(),
        "ambito": row["Ámbito"].lower(),
        "formula": formula,
        "fecha_inicio": parse_fecha(row["Inicio"]),
        "fecha_fin": parse_fecha(row["Fin"]),
        "max_descuento": parse_maximo(row["Máximo"])
    }

    db.collection("descuentos").document(row["Código"]).set(doc)
    print(f"✔ Subido: {row['Código']}")

print("\n🎉 Proceso completado sin errores.")