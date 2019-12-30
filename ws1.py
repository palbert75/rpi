import socket
import time
import secret
import pwm
import settings

print ("Prepare socket listener")
TCP_IP = settings.ws1host   #accept connection on all ip address of the machine
TCP_PORT = settings.ws1port #accept connection only on port 1978
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

                    stamp =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    PWM = pwm.calcPwm(float(temp))

                        
                    print("{} : Got {} C from {} -> PWM: {}))".format(stamp, float(temp), addr, PWM))         

                    conn.sendall("ACK".encode())
                    
                    data = { 
                                'Device' : 'MyPI',
                                'Temp' : float(temp),
                                'PWM' : PWM,
                                'Stamp' : stamp
                        }

                    result = secret.firebase.put('/last', 'value', data) 
                    result = secret.firebase.post('/values/', data) 
                    print("{} : Record stored in firebase db {}".format(stamp, result))
