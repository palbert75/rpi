import socket
import time
import pwm
import settings

rpi1host, rpi1port = settings.rpi1host, settings.rpi1port

# create a socket object
rp1_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# connection to hostname on the port.
rp1_s.connect((rpi1host, rpi1port))    


print ("Prepare socket listener")
TCP_IP = settings.rpi2host   #accept connection on all ip address of the machine
TCP_PORT = settings.rpi2port #accept connection only on port
BUFFER_SIZE = 1024 # we can receive at max 1024 bytes at time

# we choosen to use TCP stream socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# we inform the SO to bypass TIME_WAIT 
# this mean that we can restart this program without waiting fordispla
# TIME_WAIT elapsing. 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and to the port. 
# This listener will receive from kernel only packet with this 
# unique id in the header!

s.bind((TCP_IP, TCP_PORT))

lastpwm=0.0

while True:
    print ("Wait for client on port {}".format(TCP_PORT))
    # Start the listener (wait for only 1 connection at time)
    s.listen(1)

    conn, addr = s.accept() #Wait for client 

    # please note that the accept is sync function. the program will wait
    # for kernel interrupt before go to the next instruction

    # When a client arrive
    print ('Accecpted client from address:', addr)  

    # Start reading data
    while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                    print ("No other data. Socket closed")
                    break
            else:
                    temp = data.decode()
                    PWM = pwm.calcPwm(float(temp))

                    stamp =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    conn.sendall("ACK".encode())
                    
                    if lastpwm != PWM: 
                        print("{} : Got temp {} calculated PWM: {} to {}".format(stamp, temp, PWM, rpi1host))
                        rp1_s.sendall(str(PWM).encode())
                        lastpwm = PWM
