import subprocess  
import os  
import shutil  
  
def copiar_archivo(origen, destino):  
    # Si origen y destino son el mismo archivo, no copiar  
    if os.path.abspath(origen) == os.path.abspath(destino):  
        return  
    os.makedirs(os.path.dirname(destino), exist_ok=True)  
    shutil.copy(origen, destino)  
  
def ejecutar_git(repo, comando):  
    resultado = subprocess.run(  
        ["git", "-C", repo] + comando,  
        capture_output=True,  
        text=True  
    )  
  
    if resultado.returncode != 0:  
        print(f"Error ejecutando git {' '.join(comando)}")  
        print(resultado.stderr)  
        return False  
  
    return True  
  
def subir_archivo_a_github(ruta_local, repo_destino, mensaje_commit):  
    nombre_archivo = os.path.basename(ruta_local)  
    destino = os.path.join(repo_destino, nombre_archivo)  
  
    # Copiar solo si origen y destino no son el mismo archivo  
    copiar_archivo(ruta_local, destino)  
  
    # Añadir archivo al commit  
    if not ejecutar_git(repo_destino, ["add", nombre_archivo]):  
        return False  
  
    # Crear commit  
    if not ejecutar_git(repo_destino, ["commit", "-m", mensaje_commit]):  
        return False  
  
    # Subir cambios  
    if not ejecutar_git(repo_destino, ["push"]):  
        return False  
  
    print(f"Archivo {nombre_archivo} subido correctamente a GitHub")  
    return True  
  
def subir_imagenes_a_github(repo_destino, rutas_imagenes, mensaje_commit):  
    """  
    Sube múltiples imágenes a GitHub en un solo commit.  
    """  
    if not rutas_imagenes:  
        print("No hay imágenes para subir")  
        return True  
  
    archivos_añadidos = []  
  
    # Copiar todas las imágenes al destino  
    for ruta_local in rutas_imagenes:  
        nombre_archivo = os.path.basename(ruta_local)  
        destino = os.path.join(repo_destino, nombre_archivo)  
        copiar_archivo(ruta_local, destino)  
        archivos_añadidos.append(nombre_archivo)  
  
    # Añadir todos los archivos al commit  
    if not ejecutar_git(repo_destino, ["add"] + archivos_añadidos):  
        return False  
  
    # Crear un solo commit  
    if not ejecutar_git(repo_destino, ["commit", "-m", mensaje_commit]):  
        return False  
  
    # Subir cambios con --force  
    if not ejecutar_git(repo_destino, ["push", "--force"]):  
        return False  
  
    print(f"{len(archivos_añadidos)} imágenes subidas correctamente a GitHub en un solo commit")  
    return True