import socket

# Pablo Gracia Gómez - Práctica 1 Redes - HTTP


name = "www.eupla.es"
url = "/redes/practica1.php"
port = 80
  


host = socket.gethostbyname(name)


send_buf = f'GET {url} HTTP/1.0\r\n'
send_buf += f'Host: {name}\r\n'           
send_buf += f'User-Agent: Python\r\n'      
# send_buf += 'Cookie: redes=925541; expires=Sun, 09-Mar-2025 08:04:49 GMT; Max-Age=43200\r\n' # COOKIE
#send_buf += '\r\n'  
send_buf += '\r\n'                         




# Creación del socket usando TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
s.connect((host, port)) # Conectamos el socket

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

# Decodificamos la respuesta recibida
data = data.decode('utf-8')
data=data.split('\r\n')
b=''
a=''
w=0
for i in data:
    if w==1:
        b+=i

    if w==0:
        if i=='</head>':
            w=1
        a+=i
print(data)


print("ENVIADO" + "-"*16)
print(send_buf)
print("\nCABECERAS RECIBIDAS" + "-"*16)
print(a)
print("\nCUERPO RECIBIDO" + "-"*16)
print(b)
