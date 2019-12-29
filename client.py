import socket
import os
import time

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("temp=","")
        temp = temp.replace("'C", "")
        return(temp)

        
host, port = "192.168.1.117", 9999

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# connection to hostname on the port.
s.connect((host, port))                               

while True:
       
    temp = measure_temp()

    s.sendall(temp.encode())

    # Read data from the TCP server and close the connection
    received = s.recv(1024)
    print("Got PWM: ", received.decode())
    time.sleep(1)

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))
