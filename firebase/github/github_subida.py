import os
import shutil
import subprocess

def subir_imagenes_a_github(carpeta_origen, repo_destino, mensaje_commit="Subida automática de imágenes"):
    # 1. Copiar imágenes al repositorio
    for archivo in os.listdir(carpeta_origen):
        ruta_archivo = os.path.join(carpeta_origen, archivo)
        if os.path.isfile(ruta_archivo):
            shutil.copy(ruta_archivo, repo_destino)

    # 2. Ejecutar comandos git
    comandos = [
        ["git", "-C", repo_destino, "add", "."],
        ["git", "-C", repo_destino, "commit", "-m", mensaje_commit],
        ["git", "-C", repo_destino, "push"]
    ]

    for cmd in comandos:
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode != 0:
            print(f"Error ejecutando {' '.join(cmd)}:")
            print(resultado.stderr)
            return False

    print("Imágenes subidas correctamente a GitHub")
    return True
