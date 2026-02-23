import subprocess
import os
import shutil

def copiar_archivo(origen, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy(origen, destino)

def ejecutar_git(repo, comando):
    resultado = subprocess.run(
        ["git", "-C", repo] + comando,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        print(f"❌ Error ejecutando git {' '.join(comando)}")
        print(resultado.stderr)
        return False

    return True

def subir_archivo_a_github(ruta_local, repo_destino, mensaje_commit):
    nombre_archivo = os.path.basename(ruta_local)
    destino = os.path.join(repo_destino, nombre_archivo)

    copiar_archivo(ruta_local, destino)

    if not ejecutar_git(repo_destino, ["add", nombre_archivo]):
        return False

    if not ejecutar_git(repo_destino, ["commit", "-m", mensaje_commit]):
        return False

    if not ejecutar_git(repo_destino, ["push"]):
        return False

    print(f"✔ Archivo {nombre_archivo} subido correctamente a GitHub")
    return True
