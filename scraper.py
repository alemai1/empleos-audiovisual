import json
import datetime
import time
import random
import requests
from bs4 import BeautifulSoup

# Simula ser un navegador normal
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

def buscar_computrabajo():
    print("Buscando en Computrabajo...")
    url = "https://py.computrabajo.com/trabajo-de-audiovisual"
    trabajos = []
    
    try:
        respuesta = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        ofertas = soup.find_all("article", class_="box_offer")
        
        for oferta in ofertas[:8]: # Traemos las 8 más recientes
            titulo_tag = oferta.find("h2")
            empresa_tag = oferta.find("p", class_="fs16")
            
            if titulo_tag and titulo_tag.find("a"):
                enlace_tag = titulo_tag.find("a")
                titulo = enlace_tag.text.strip()
                enlace = "https://py.computrabajo.com" + enlace_tag["href"]
                empresa = empresa_tag.text.strip() if empresa_tag else "Empresa Confidencial"
                
                trabajos.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "ubicacion": "Paraguay",
                    "descripcion": "Oferta encontrada en Computrabajo.",
                    "enlace": enlace,
                    "etiqueta": "Computrabajo"
                })
    except Exception as e:
        print("Error al leer Computrabajo:", e)
        
    return trabajos

def buscar_buscojobs():
    print("Buscando en Buscojobs...")
    # URL de búsqueda de Buscojobs en Paraguay
    url = "https://www.buscojobs.com.py/ofertas/trabajo-de-audiovisual"
    trabajos = []
    
    try:
        respuesta = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        
        # Buscojobs suele usar clases diferentes (esto es un estándar común, si la web cambia, se ajusta aquí)
        ofertas = soup.find_all("div", class_="offer-title") 
        
        for oferta in ofertas[:8]:
            enlace_tag = oferta.find("a")
            if enlace_tag:
                titulo = enlace_tag.text.strip()
                enlace = enlace_tag["href"]
                # Asegurarnos de que el link esté completo
                if not enlace.startswith("http"):
                    enlace = "https://www.buscojobs.com.py" + enlace
                
                trabajos.append({
                    "titulo": titulo,
                    "empresa": "Ver detalles en la web",
                    "ubicacion": "Paraguay",
                    "descripcion": "Oferta encontrada en Buscojobs.",
                    "enlace": enlace,
                    "etiqueta": "Buscojobs"
                })
    except Exception as e:
        print("Error al leer Buscojobs:", e)
        
    return trabajos

def iniciar_piloto_automatico():
    print("🤖 ¡Robot iniciado! Buscando en múltiples portales...")
    
    while True:
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n[{hora_actual}] Iniciando nueva ronda de búsqueda...")
        
        # 1. Buscar en Computrabajo
        trabajos_ct = buscar_computrabajo()
        
        # Pausa aleatoria (entre 5 y 10 segundos) para no parecer un robot y evitar bloqueos
        time.sleep(random.randint(5, 10))
        
        # 2. Buscar en Buscojobs
        trabajos_bj = buscar_buscojobs()
        
        # 3. Juntar todos los trabajos
        todos_los_trabajos = trabajos_ct + trabajos_bj
        
        # Si no encontró nada (por errores de conexión o cambios en la web), usamos datos de respaldo
        if len(todos_los_trabajos) == 0:
            print("⚠️ No se pudieron extraer datos en vivo. Usando datos de respaldo.")
            todos_los_trabajos = [{
                "titulo": "Editor Audiovisual / Creador de Contenido 🎥 (Respaldo)",
                "empresa": "Agencia Local",
                "ubicacion": "Asunción, Paraguay",
                "descripcion": "No pudimos conectar con los portales, pero puedes buscar manualmente mientras tanto.",
                "enlace": "https://py.computrabajo.com/trabajo-de-audiovisual",
                "etiqueta": "Respaldo"
            }]
        
        # Guardar en el JSON
        with open("jobs.json", "w", encoding="utf-8") as archivo:
            json.dump(todos_los_trabajos, archivo, ensure_ascii=False, indent=4)
            
        print(f"✅ ¡Éxito! Base de datos actualizada con {len(todos_los_trabajos)} ofertas.")
        print("💤 El robot se va a dormir. Despertará en 4 horas...\n")
        
        # Dormir 4 horas (14400 segundos)
        time.sleep(14400)

if __name__ == "__main__":
    iniciar_piloto_automatico()