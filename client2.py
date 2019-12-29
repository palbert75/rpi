import socket
import time
import secret

host, port = "192.168.1.117", 9998

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# connection to hostname on the port.
s.connect((host, port))                               

while True:
       
    data = secret.firebase.get('/last/value', '')


    print("Retrieved temperature {} C from firebase".format(str(data['Temp'])))
    

    temp = data['Temp']

    pwm = 0.0
    
    if temp >= 50:
        pwm = 2.0 * (temp -50) 

    s.sendall(str(pwm).encode())
    print("Sent pwm {} to server".format(str(pwm)))
    
    # Read data from the TCP server and close the connection
    received = s.recv(1024)
    print("Got from server: ", received.decode())
    time.sleep(5)

s.close()
