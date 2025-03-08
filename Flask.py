import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Configurar proxy de Tor
TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Verificar si Tor está corriendo
def is_tor_running():
    try:
        response = requests.get("https://check.torproject.org/api/ip", proxies=TOR_PROXY, timeout=10)
        return response.json().get("IsTor", False)
    except Exception:
        return False

@app.route("/")
def index():
    client_ip = request.remote_addr
    tor_status = is_tor_running()
    tor_ip = "No disponible"
    
    if tor_status:
        try:
            response = requests.get("https://check.torproject.org/api/ip", proxies=TOR_PROXY)
            tor_ip = response.json().get("IP", "Error al obtener IP")
        except Exception as e:
            tor_ip = f"Error: {str(e)}"

    # Solo imprimir la información en la terminal
    print("\n--- Verificación de Conexión Tor ---")
    print(f"Tu IP pública (sin Tor): {client_ip}")
    print(f"¿Conectado a Tor?: {'Sí' if tor_status else 'No'}")
    print(f"IP Salida Tor: {tor_ip}\n")

    return "Información mostrada en la terminal."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
