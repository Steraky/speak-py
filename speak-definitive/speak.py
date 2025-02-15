from ui import Menu
import requests, re, json
import os, sys, time, terminaltables
from terminaltables import SingleTable
from colorama import Fore, init
from time import sleep
import random
import getpass
import base64
import socket
import threading

class state():
    need_ip_port = True

version = 'DEFINITIVE'

stop_thread = False

warn = ("  [" + Fore.LIGHTRED_EX + "!" + Fore.RESET + "] ")
info = ("  [" + Fore.BLUE + "*" + Fore.RESET + "] ")

user = getpass.getuser()

def times():
	times = time.strftime("%H:%M:%S")
	times = str(times)
	return(times)

def clear():
	if os.name == 'nt':
		return os.system('cls')
	else:
		return os.system('clear')

clear()

if os.name == 'nt':
    init(convert=True)
else:
    init(convert=False)

print(Menu.design_ui)

def Messages():
    TABLE_DATA = []
    private_messages = (Fore.LIGHTYELLOW_EX + "Speak Main" + Fore.RESET, "Nom D'utilisateur : " + user)
    TABLE_DATA.append(private_messages)
    private_messages = (Fore.LIGHTYELLOW_EX + "News :" + Fore.RESET, Fore.LIGHTBLACK_EX + "Grosse Update :" + Fore.RESET)
    TABLE_DATA.append(private_messages) 
    private_messages = (" ", Fore.LIGHTBLACK_EX + "Pseudo En Couleur" + Fore.RESET)
    TABLE_DATA.append(private_messages)
    private_messages = (" ", Fore.LIGHTBLACK_EX + "Code Optimised" + Fore.RESET)
    TABLE_DATA.append(private_messages)
    table = SingleTable(TABLE_DATA)
    print("\n"+table.table)
Messages()

def client_speak(nickname, ip, port, color):
    try:
        # Connecting To Server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection = client.connect((str(ip),int(port)))
        ver = client.send(version.encode('utf-8'))
        # Listening to Server and Sending Nickname
        def receive():
            while True:
                global stop_thread
                if stop_thread:
                    break
                try:
                    # Receive Message From Server
                    # If 'NICK' Send Nickname
                    message = client.recv(1024).decode('utf-8')
                    if message == 'NICK':
                        encodenick = nickname.encode('utf-8')
                        cryptnick = base64.b85encode(encodenick)
                        client.send(cryptnick)
                        next_message = client.recv(1024).decode('utf-8')
                        if next_message == 'BAN':
                            print(Fore.LIGHTRED_EX + " Vous avez été Banni de speak par un Administrateur")
                            client.close()
                            stop_thread = True
                    else:
                        print(" ")
                        messagedecrypt = base64.b85decode(message)
                        messagedecode = messagedecrypt.decode('utf-8')
                        print(messagedecode)
                        print(" ")
                except:
                    # Close Connection When Error
                    print(warn + "Une erreure s'est produite!")
                    client.close()
                    break

        # Sending Messages To Server
        def write():
            while True:
                if stop_thread:
                    break
                writer = getpass.getpass(Fore.LIGHTBLACK_EX +" Vous ↓ :"+ Fore.RESET)
                message = ' - {}: {}'.format(color + nickname + Fore.RESET, writer)
                encoded_message = message.encode('utf-8')
                msgcrypt = base64.b85encode(encoded_message)
                client.send(msgcrypt)

        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()
    except:
        print(" ")
        print(warn + "Une erreure s'est produite!")
        sleep(1.5)
        clear()
        print(" ")
        sys.exit(info + "Disconnected")

def Ip_Select(nick, color_choice):
    if state.need_ip_port == True:
        print(" ")
        ip = input(" Ip du serveur speak : ")
        print(" ")
        port = input(" Port du serveur speak : ")
        clear()
        print(Menu.design_ui)
        print(" ")
        client_speak(nickname=nick, ip=ip, port=port, color=color_choice)
    else:
        clear()
        print(Menu.design_ui)
        print(" ")
        ip = 'vps-1f21facc.vps.ovh.net'
        port = 6677
        client_speak(nickname=nick, ip=ip, port=port, color=color_choice)

def Choice_Color(nickname):
    clear()
    print(Menu.design_ui)
    print(" ")
    print(f"""
    Couleur du pseudo :

        [{Fore.LIGHTBLUE_EX + str("1") + Fore.RESET}] : Bleu Clair (Default)
        [{Fore.LIGHTBLUE_EX + str("2") + Fore.RESET}] : Rose
        [{Fore.LIGHTBLUE_EX + str("3") + Fore.RESET}] : Jaune
        [{Fore.LIGHTBLUE_EX + str("4") + Fore.RESET}] : Violet
        [{Fore.LIGHTBLUE_EX + str("5") + Fore.RESET}] : Vert
        [{Fore.LIGHTBLUE_EX + str("6") + Fore.RESET}] : Rouge
        [{Fore.LIGHTBLUE_EX + str("7") + Fore.RESET}] : Cyan
        [{Fore.LIGHTBLUE_EX + str("8") + Fore.RESET}] : Bleu

    """)
    color_choice = input(" Votre choix : ")

    if color_choice == '1':
        color = Fore.LIGHTBLUE_EX
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '':
        color = Fore.LIGHTBLUE_EX
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '2':
        color = Fore.LIGHTMAGENTA_EX
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '3':
        color = Fore.YELLOW
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '4':
        color = Fore.MAGENTA
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '5':
        color = Fore.LIGHTGREEN_EX
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '6':
        color = Fore.LIGHTRED_EX
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '7':
        color = Fore.LIGHTCYAN_EX
        Ip_Select(nick=nickname, color_choice=color)
    elif color_choice == '8':
        color = Fore.BLUE
        Ip_Select(nick=nickname, color_choice=color)
    else:
        print(" ")
        print("  " + warn + "Erreur x-x")
        sleep(1.5)
        clear()
        print(Menu.design_ui)
        Messages()
        Choix()
        pass

def Nick_Choice():
    # Choosing Nickname
    print(f"""
    Nom d'utilisateur :

    [{Fore.LIGHTBLUE_EX + str("1") + Fore.RESET}] : Au hazard
    [{Fore.LIGHTBLUE_EX + str("2") + Fore.RESET}] : Nom au choix
    [{Fore.LIGHTBLUE_EX + str("3") + Fore.RESET}] : Nom de l'user du pc

    """)
    nick_choice = input(" Votre choix : ")

    if nick_choice == '1':
        url = "http://names.drycodes.com/10?nameOptions=all"
        data = requests.get(url).content.decode('utf-8')
        values = json.loads(data)
        randomchoice = random.choice(values)
        nickname = str(randomchoice)
        print(" ")
        print(" Votre nom d'utilisateur : %s" % (nickname))
        sleep(1.5)
        clear()
        print(Menu.design_ui)
        Choice_Color(nickname=nickname)

    elif nick_choice == '2':
        print(" ")
        name = input(" Nouveau nom d'utilisateur : ")
        nickname = str(name)
        if nickname == '':
            print(" ")
            print("  " + warn + "Erreur x-x")
            sleep(1.5)
            clear()
            print(Menu.design_ui)
            Messages()
            Choix()
            pass
        else:
            sleep(1.5)
            clear()
            print(Menu.design_ui)
            Choice_Color(nickname=nickname)

    elif nick_choice == '3':
        nickname = str(user)
        print(" ")
        print(" Votre nom d'utilisateur : %s" % (nickname))
        sleep(1.5)
        clear()
        print(Menu.design_ui)
        Choice_Color(nickname=nickname)
    else:
        print(" ")
        print("  " + warn + "Erreur x-x")
        sleep(1.5)
        clear()
        print(Menu.design_ui)
        Messages()
        Choix()
        pass

def Choix():
    print(f"""

    [{Fore.LIGHTBLUE_EX + str("1") + Fore.RESET}] Serveur speak Officiel
    
    [{Fore.LIGHTBLUE_EX + str("2") + Fore.RESET}] Connection a un Serveur Speak non-officiel

    """
    )
    choice = input(" Salon choisi : ")

    #Général
    if choice == '1':
        clear()
        print(Menu.design_ui)
        state.need_ip_port = False
        Nick_Choice()

    elif choice == '2':
        clear()
        print(Menu.design_ui)
        state.need_ip_port = True
        Nick_Choice()

    elif choice == 'credits':
        clear()
        print(f"""
        
        /$$$$$$                            /$$ /$$   /$$             
       /$$__  $$                          | $$|__/  | $$             
      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$$ /$$ /$$$$$$   /$$$$$$$
      | $$       /$$__  $$ /$$__  $$ /$$__  $$| $$|_  $$_/  /$$_____/
      | $$      | $$  \__/| $$$$$$$$| $$  | $$| $$  | $$   |  $$$$$$ 
      | $$    $$| $$      | $$_____/| $$  | $$| $$  | $$ /$$\____  $$
      |  $$$$$$/| $$      |  $$$$$$$|  $$$$$$$| $$  |  $$$$//$$$$$$$/
       \______/ |__/       \_______/ \_______/|__/   \___/ |_______/ 
                                                               
                                                               
      Credits :

      {str("Director : ") + Fore.LIGHTRED_EX + str("ezby") + Fore.RESET}
      {str("Developper : ") + Fore.LIGHTBLUE_EX + str("Steraky / Hide") + Fore.RESET}
      {str("Beta tester : ") + Fore.MAGENTA + str("Orizon's, Rocher Coco, Neko, tamashi, punchnox, ThePillow, Courgette, Vendetta, Yamass") + Fore.RESET}

""")
        sleep(20000)

    else:
        print(" ")
        print("  " + warn + "Erreur x-x")
        sleep(1.5)
        clear()
        print(Menu.design_ui)
        Messages()
        Choix()
        pass

Choix()
