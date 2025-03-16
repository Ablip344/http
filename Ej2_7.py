import socket

def descarga(name,port,url):
    # Pablo Gracia Gómez - Práctica 1 Redes - HTTP

    # Obtenemos la IP a partir del nombre
    host = socket.gethostbyname(name)

    # Construimos la petición HTTP 1.0
    send_buf = f'GET {url} HTTP/1.0\r\n'
    send_buf += f'Host: {name}\r\n'
    send_buf += f'User-Agent: Python\r\n'
    send_buf += '\r\n'

    # Creamos un socket TCP (IPv4, SOCK_STREAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 
    s.settimeout(2)  # Tiempo de espera máximo 2 segundos
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
    
    return (a,b)

#print(descarga('www.eupla.es',80,'/redes/practica1.php'))