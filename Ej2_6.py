import socket

# Pablo Gracia Gómez - Práctica 1 Redes - HTTP



# Recurso: separamos dominio y objeto
name = "www.eupla.es"
url = "/redes/logoredes.jpg"
port = 80
  

# Obtenemos la IP a partir del nombre
host = socket.gethostbyname(name)

# Construimos la petición HTTP 1.0
send_buf = f'GET {url} HTTP/1.0\r\n'
send_buf += f'Host: {name}\r\n'           
send_buf += f'User-Agent: Python\r\n'
send_buf += f'If-Modified-Since: Thu, 13 Feb 2025 10:51:34 GMT\r\n'       
send_buf += '\r\n'                         

# Creamos un socket TCP (IPv4, SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
s.connect((host, port)) # Conexión con la ip y puerto establecidos

# Enviamos la petición HTTP
s.send(send_buf.encode())

# Recogemos los datos en un bucle
data = b""
while True:
    part = s.recv(256)
    if part == b'':
        break
    data += part

s.close()

print(data)