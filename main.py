import socket
import sys
import click
from contextlib import closing
import time
import json
import pyfiglet

class Wiz:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.color = {}
        self.dimming = 100
    def turn_on(self):
        message = '{"id":1,"method":"setState","params":{"state":true}}'
        udp_client(self.ip,self.port,message)

    def turn_off(self):
        message = '{"id":1,"method":"setState","params":{"state":false}}'
        udp_client(self.ip,self.port,message)

    def change_color(self):
        self.color = self.ask_color()
        message = '{"id":1,"method":"setPilot","params":{"r":0,"g":0,"b":0,"dimming":100}}'
        json_message = json.loads(message)
        json_message["params"]["r"] = self.color["r"]
        json_message["params"]["g"] = self.color["g"]
        json_message["params"]["b"] = self.color["b"]
        json_message["params"]["dimming"] = self.dimming
        udp_client(self.ip,self.port,json.dumps(json_message))

    def change_dimming(self,value):
        self.dimming = value;
        message = '{"id":1,"method":"setPilot","params":{"dimming":100}}'
        json_message = json.loads(message)
        json_message['params']['dimming'] = self.dimming;
        udp_client(self.ip,self.port,json.dumps(json_message))
        return True
    
    def ask_color(self):
        red = click.prompt("Please enter value of red",type=int,default=0,show_default=True)
        green = click.prompt("Please enter value of green",type=int,default=0,show_default=True)
        blue = click.prompt("Please enter value of blue",type=int,default=255,show_default=True)
        if red <= 255 and green <= 255 and blue <= 255:
            new_color = {"r":red,"g":green,"b":blue}
        else:
            print("[-] value must be lower than 255")
            print("[-] setting to default color (blue)")
            new_color = {"r":0,"g":0,"b":255}
            
        return new_color
        
def udp_client(ip,port,message):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    print("Do Ctrl+C to exit the program !!")

    while True:
        s.sendto(message.encode('utf-8'),(ip,port))
        print(f"\n [-] Data sent to client : {message},\n")
        data,address = s.recvfrom(4096)
        print(f"\n [-] Data recieved from Client : {data.decode('utf-8')},\n")
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


def gettui():
    print('welcome to pyauto cli..')



def welcome():
    header = pyfiglet.figlet_format("wiz-cli")
    print(header)
    
@click.command()
@click.option("-p","--port",default=38899,type=int)
@click.option("-ip","--ipaddr",required=True,type=str,prompt="please enter the ip of your wiz light (you can get it from your wiz mobile app)")
@click.option("-m","--message",default="hello world (default message)",type=str)
@click.option('--tui',is_flag=True)
@click.option('-cc','--changecolor',is_flag=True)
@click.option('-off','--turnoff',is_flag=True)
@click.option('-on','--turnon',is_flag=True)
@click.option('-dim','--dimming',type=int)
def main(port,ipaddr,message,tui,changecolor,turnoff,turnon,dimming):
    welcome()
    if(error_check(port,ipaddr)):
       wiz_light = Wiz(ipaddr,port)
       if turnon:
           wiz_light.turn_on()
       if changecolor:
           wiz_light.change_color()
       if turnoff:
           wiz_light.turn_off()
       if dimming != None:
           wiz_light.change_dimming(dimming)
       if tui:
           print("tui comming soon")
    else:
       print("some error")
    
main()
