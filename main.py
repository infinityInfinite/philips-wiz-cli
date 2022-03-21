import socket
import sys
import click
import time
import json
import pyfiglet
from contextlib import closing
from scenes import get_scenes
from termcolor import colored,cprint

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
        red = click.prompt(colored("Please enter value of red","red"),type=int,default=0,show_default=True)
        green = click.prompt(colored("Please enter value of green","green"),type=int,default=0,show_default=True)
        blue = click.prompt(colored("Please enter value of blue","blue"),type=int,default=255,show_default=True)
        if red <= 255 and green <= 255 and blue <= 255:
            new_color = {"r":red,"g":green,"b":blue}
        else:
            print("[-] value must be lower than 255")
            print("[-] setting to default color (blue)")
            new_color = {"r":0,"g":0,"b":255}
            
        return new_color


    def set_scene(self):
        scenes = get_scenes()
        for i,v in scenes.items():
            print(colored(f"{i} : {v}","magenta"))
        user_prompt = click.prompt(colored("choose an scene:","yellow"),type=int,default=1,show_default=True)
        message = '{"id":1,"method":"setPilot","params":{"sceneId":0}}'
        json_message = json.loads(message)
        json_message['params']['sceneId'] = user_prompt
        udp_client(self.ip,self.port,json.dumps(json_message))
        
    
def udp_client(ip,port,message,return_response=False):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
    print(colored("Do Ctrl+C to exit the program !!","blue"))

    while True:
        try:
            s.sendto(message.encode('utf-8'),(ip,port))
            print(colored(f"\n [-] Data sent to client : {message},\n","green"))
            s.settimeout(5)
            data,address = s.recvfrom(4096)
            
            if return_response:
                s.close()
                return data
            else:
                print(colored(f"\n [-] Data recieved from Client : {data.decode('utf-8')},\n","green"))
                s.close()
        except socket.timeout:
            s.close()
            print(colored("[-] Looks like given ip is not wiz-light , try looking ip address in your wiz mobile app !","red"))
            exit() 
        break



def error_check(port,ipaddr):
    port_open = False
    valid_ip = False
    overflow_error = False
    wiz_light = False
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
        print(colored("[-] port must be below 65535","red"))
    if valid_ip == False:
        print(colored('[-] ip address is not valid / checking port is available didnt take place ..',"red"))
    if valid_ip == True and port == False:
        print(colored('[-] given port is not open',"red"))        
        
    if overflow_error == False and valid_ip == True and port_open == True:
        return True
    else:
        return False;


def gettui():
    print(colored("Coming soon...","blue"))

def welcome():
    header = pyfiglet.figlet_format("wiz-cli")
    print(colored(header,"red",attrs=["bold"]))
    
@click.command()
@click.option("-p","--port",default=38899,type=int)
@click.option("-ip","--ipaddr",required=True,type=str,prompt="please enter the ip of your wiz light (you can get it from your wiz mobile app)")
@click.option("-m","--message",default="hello world (default message)",type=str)
@click.option('--tui',is_flag=True)
@click.option('-cc','--changecolor',is_flag=True)
@click.option('-off','--turnoff',is_flag=True)
@click.option('-on','--turnon',is_flag=True)
@click.option('-dim','--dimming',type=int)
@click.option('-ss','--setscene',is_flag=True)
def main(port,ipaddr,message,tui,changecolor,turnoff,turnon,dimming,setscene):
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
       if setscene:
           wiz_light.set_scene()
       if tui:
           print("tui comming soon")
    else:
       print(colored("some error","red"))
    
main()
