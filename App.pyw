import socket
import random
import subprocess	
from tkinter import *
import tkinter.font as tkFont

#OUI LE CODE EST DEGEU ET PAS COMMENTE PARCE QUE J'AI PAS LE TEMPS GNAGNAGNA

def envoyer():
	global entre, nomUser, filMessages, client_socket

	message = entre.get()
	if len(message) != 0:
		message = nomUser + " : " + message
		filMessages.insert(END, message)
		message = message.encode('utf-8')
		client_socket.send(bytes(message))
		entre.delete(0, 'end')
	else:
		entre.delete(0, 'end')

def reception():
	global filMessages, client_socket
	try:
		messageRecu = client_socket.recv(2048)
		messageRecu = messageRecu.decode("utf-8")
		filMessages.insert(END, messageRecu)	
	except:
		pass
	finally:	
		fen.after(3000, reception)

def placeholder(affichage):
	if affichage == True:
		entre.insert(0, "Saisissez votre message ici")
	else:
		entre.delete(0, "end")

def affichageConversation():
	global cadreParametres, entre, nomUser, filMessages

	logo.pack_forget()
	cadreParametres.pack_forget()

	filMessages = Listbox(fen, width="70", height="20")
	filMessages.pack(pady=15)

	entre = Entry(fen, width="60")
	entre.pack()

	bouttonEnvoyer = Button(fen, text="Envoyer", command=envoyer)
	bouttonEnvoyer.pack(pady=15)

	entre.bind("<Button-1>", placeholder)

	reception()
	placeholder(True)

def connexion():
	global IP, Port, nomUser, entreNom, client_socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((IP, Port))
	client_socket.setblocking(0)
	nomUser = entreNom.get()


def démarrerServeur():
	global entrePort, IP, Port
	Port = int(entrePort.get())
	subprocess.Popen(f"python Serveur.py {IP} {Port}")
	print("Je suis là !")
	connexion()
	affichageConversation()

def hote():
	global entrePort, IP, nomUser, cadreParametres, entreNom

	messageBienvenue.pack_forget()
	cadreBouttons.pack_forget()

	hote = socket.gethostname()
	IP = socket.gethostbyname(hote)

	cadreParametres = Frame(fen, bg="grey")
	cadreParametres.pack()       

	votreIP = Label(cadreParametres, text=f"Votre adresse IP locale : {IP}", font=policeIP, bg="Grey")
	votreIP.pack()

	votrePort = Label(cadreParametres, text="Port", bg="Grey")
	votrePort.pack(anchor=CENTER, pady=7)

	portRecommande = random.randint(49152, 65535)

	entrePort = Entry(cadreParametres)
	entrePort.insert("end", portRecommande)
	entrePort.pack(anchor=CENTER)

	votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
	votreNom.pack(anchor=CENTER, pady=7)

	entreNom = Entry(cadreParametres)
	entreNom.pack(anchor=CENTER)

	bouttonStart = Button(cadreParametres, text="Démarrer", command=démarrerServeur)
	bouttonStart.pack(pady=20)

def seConnecter():
	global entreIP, entrePort, IP, Port
	Port = int(entrePort.get())
	IP = entreIP.get()
	connexion()
	affichageConversation()

def client():
	global entreIP, entrePort, entreNom, cadreParametres
	messageBienvenue.pack_forget()
	cadreBouttons.pack_forget()

	cadreParametres = Frame(fen, bg="grey")
	cadreParametres.pack()       

	IpduServeur = Label(cadreParametres, text="Adresse IP du serveur", bg="Grey")
	IpduServeur.pack(anchor=CENTER, pady=7)

	entreIP = Entry(cadreParametres)
	entreIP.pack(anchor=CENTER)

	PortduServeur = Label(cadreParametres, text="Port du serveur", bg="Grey")
	PortduServeur.pack(anchor=CENTER, pady=7)

	entrePort = Entry(cadreParametres)
	entrePort.pack(anchor=CENTER)

	votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
	votreNom.pack(anchor=CENTER, pady=7)

	entreNom = Entry(cadreParametres)
	entreNom.pack(anchor=CENTER)

	bouttonStart = Button(cadreParametres, text="Se connecter",  command=seConnecter)
	bouttonStart.pack(pady=20)

fen = Tk()
fen.geometry("550x450")
fen.title("Kripto - Un chat chiffré")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
fen.iconbitmap(bitmap="Médias/icone.ico")

policeBienvenue = tkFont.Font(family="Verdanna",size=16,weight="bold")
policeBoutton = tkFont.Font(family="Arial",size=12,weight="bold")
policeIP = tkFont.Font(size=14,weight="bold")

imageLogo = PhotoImage(file="Médias/Logo.png")
 
logo = Label(fen, bg="grey", image=imageLogo)
logo.pack() 

messageBienvenue = Label(fen, text="Bienvenue dans Kripto. Pour démarrez, dites-nous \nsi vous voulez être hôte ou bien client.", bg="grey", font=policeBienvenue)
messageBienvenue.pack()

cadreBouttons = Frame(fen, bg="grey")
cadreBouttons.pack(pady=60)

bouttonHote = Button(cadreBouttons, text="Être hôte", font=policeBoutton, command=hote)
bouttonHote.pack(side=LEFT, padx=7)

bouttonClient = Button(cadreBouttons, text="Être client", font=policeBoutton, command=client)
bouttonClient.pack(side=LEFT, padx=7)

fen.mainloop()