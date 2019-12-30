import socket
import os
import time
import select
import settings

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("temp=","")
        temp = temp.replace("'C", "")
        return(temp)

def processPWM(pwm):
    print("Switch fan rotation to {} %".format(pwm))


ws1host, ws1port = settings.ws1host, settings.ws1port
rpihost, rpiPWMport = settings.rpi1host, settings.rpi1port

# create a socket object
ws_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# connection to hostname on the port.
ws_s.connect((ws1host, ws1port))                               
   



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((rpihost, rpiPWMport))
server_socket.listen(5)
print ("Listening on port {}".format(rpiPWMport))

read_list = [server_socket]
server_socket.setblocking(0)

lastTime = 0
while True:

    
    if (time.time() - lastTime ) >= 15:
        
        lastTime = time.time()

        temp = measure_temp()

        # Send temperature to workstation server
        ws_s.sendall(temp.encode())
        print("Sent temperature {} C to server {}".format(float(temp), ws1host))

        # Read response data from the workstation1 server
        received = ws_s.recv(1024)
        print("Got from server: ", received.decode())
        
    # Check if there is incomming PWM response from rpi2
    readable, writable, errored = select.select(read_list, [], [], 1)
    for s in readable:
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print ("PWM Connection from {}".format(address))
        else:
            data = s.recv(1024)
            if data:
                processPWM(float(data.decode()))
            else:
                s.close()
                read_list.remove(s)

    time.sleep(1)

ws_s.close()
