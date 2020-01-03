import socket
import time
import secret
import pwm
import settings

rpi2host, rpi2port = settings.rpi2host, settings.rpi2port                           

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# connection to hostname on the port.
s.connect((rpi2host, rpi2port))                               

while True:
       
    data = secret.firebase.get('/last/value', '')


    print("Retrieved temperature {} C from firebase".format(str(data['Temp'])))

    temp = data['Temp']
    stamp =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    s.sendall(str(temp).encode())
    print("{}: Sent temp {} to server {} (rpi2)".format(stamp, temp, rpi2host))
    
    # Read data from the TCP server and close the connection
    received = s.recv(1024)
    print("Got from server: ", received.decode())
    time.sleep(5)

s.close()
