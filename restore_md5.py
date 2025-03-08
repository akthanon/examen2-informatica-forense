import hashlib
import sys

def calcular_md5(archivo):
    hasher = hashlib.md5()
    with open(archivo, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def recuperar_archivo(original_hash, archivo_modificado):
    with open(archivo_modificado, "rb") as f:
        data = bytearray(f.read())  # Convertimos a bytearray para modificarlo
    
    total_bytes = len(data)
    
    for i in range(total_bytes):
        byte_original = data[i]  # Guardamos el valor original
        for nuevo_byte in range(256):  # Probamos todos los valores posibles (0-255)
            if nuevo_byte == byte_original:
                continue  # Saltamos el mismo valor
            
            data[i] = nuevo_byte  # Modificamos el byte
            nuevo_hash = hashlib.md5(data).hexdigest()
            
            if nuevo_hash == original_hash:
                print(f"Archivo restaurado modificando el byte en la posición {i}")
                with open("ftp_access_rec.exe", "wb") as f:
                    f.write(data)  # Guardamos el archivo recuperado
                return True
        
        data[i] = byte_original  # Restauramos el byte original antes de probar la siguiente posición
        
        # Mostrar el progreso cada vez que se modifica un byte
        progreso = (i + 1) / total_bytes * 100
        print(f"Progreso: {progreso:.2f}%",nuevo_hash)
    
    print("No se pudo recuperar el archivo")
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python restore_md5.py <hash_original> <archivo_modificado>")
        sys.exit(1)
    
    hash_original = sys.argv[1]
    archivo_modificado = sys.argv[2]
    
    recuperar_archivo(hash_original, archivo_modificado)
