import machine
import network
import socket





def StartServer():   
    # Importing relevant libraries

    # Initialize an object of network class
    ap = network.WLAN (network.AP_IF)
    ap.active (True)
    # Setting the name of the WI-Fi address
    ap.config (essid = 'TEAMNINE')
    # Setting the password
    ap.config (authmode = 3, password = '99999999')

 

    html = """<!DOCTYPE html>
    <html>
        <head> <title>WebServer</title> </head>
        <body> <h1>ESP32 Pins</h1>
            <table border="3"> <tr><th>Device</th><th>Pin</th><th>Value</th></tr> %s </table>
        </body>
    </html>
    """ 

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        
        while True:
            line = cl_file.readline()
            print(line)
            if not line or line == b'\r\n':
                break
        rows = ""
        response = html % '\n'.join(rows)
        cl.send(response)

        cl.close()
StartServer()