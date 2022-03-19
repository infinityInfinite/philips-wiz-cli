import socket
import sys
import click
from contextlib import closing
import time


class Wiz:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def turn_on(self):
        message = '{"id":1,"method":"setState","params":{"state":true}}'
        udp_client(self.ip,self.port,message)

    def turn_off(self):
        message = '{"id":1,"method":"setState","params":{"state":false}}'
        udp_client(self.ip,self.port,message)

    def change_color(self):
        message = '{"id":1,"method":"setPilot","params":{"r":0,"g":0,"b":255,"dimming":100}}'
        udp_client(self.ip,self.port,message)


def udp_client(ip,port,message):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    print("Do Ctrl+C to exit the program !!")

    while True:
        s.sendto(message.encode('utf-8'),(ip,port))
        print(f"\n [-] Data sent to client : {message},\n")
        data,address = s.recvfrom(4096)
        print(f"\n [-] Data recieved from Client : {data.decode('utf-8')},\n")
        time.sleep(3)
        s.close()
        break



def error_check(port,ipaddr):
    port_open = False
    valid_ip = False
    overflow_error = False

    try:
        socket.inet_aton(ipaddr)
        valid_ip = True
    except socket.error:
        valid_ip = False



    with closing(socket.socket(socket.AF_INET,socket.SOCK_DGRAM)) as sock:
        if port < 65535 and valid_ip:
            if sock.connect_ex((ipaddr,port)) == 0:                                   
                port_open = True
        if port > 65535:
            overflow_error = True

        
    if overflow_error == True:
        print("[-] port must be below 65535")
    if valid_ip == False:
        print('[-] ip address is not valid / checking port is available didnt take place ..')
    if valid_ip == True and port == False:
        print('[-] given port is not open')

    if overflow_error == False and valid_ip == True and port_open == True:
        return True
    else:
        return False;

            
@click.command()
@click.option("-p","--port",default=38899,type=int)
@click.option("-ip","--ipaddr",required=True,type=str)
@click.option("-m","--message",default="hello world (default message)",type=str)
def main(port,ipaddr,message):
    if error_check(port,ipaddr):
        wiz_light = Wiz(ipaddr,port)
        wiz_light.turn_off()
        time.sleep(5)
        wiz_light.turn_on()
        time.sleep(5)
        wiz_light.change_color()
    else:
        print('false..')
   
main()
