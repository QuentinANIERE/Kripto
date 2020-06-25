# coding: utf8
import sys, platform
import time
import socket
import tkinter
import winsound
import threading
from tkinter import *
import tkinter.simpledialog
import tkinter.font as tkFont
from tkinter import messagebox
from random import randint, choices
from Modules import ChiffrementRSA, Fonctions, LecteurSauvegarde, Paramètres, Sauvegarde, Serveur


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                          Index

I. Définition de AfficherMenu()........................................................84

    La fonction qui affiche le menu principal de l'application. Elle est appellée au 
    démarrage de l'application et quand l'utilisateur retourne au menu.

II. Hôte et clients...................................................................105

    Les fonctions qui servent à afficher le menus de connexion pour le client et celles 
    qui servent à démarrer le serveur.

    A. Travail spécifique à l'hôte....................................................105

        1. Définition de DevenirHôte()................................................105

            Cette fonction affiche le menu qui permet à l'hôte de configurer le mode de 
            connexion au serveur (Ip, Port et nom d'utilisateur)

        2. Définition de DémarrerServeur()............................................176

            Cette fonction lance le thread du serveur, en récupérant les informations
            données sur l'interface de connexion.

    B. Fonctions spécifiques au client

        1. Définition de DevenirClient()..................................................220

            Cette fonction affiche l'interface qui permet choisir à quel serveur se connecter 

        2. Définition de SeConnecter()..................................................220

            Fonction qui récupere les informations saisies par l'utilisateur dans la fonction
            DevenirClient() et qui initie une connexion avec le serveur.
    

III. Connexion et envoi de messages...................................................271

    Les fonctions dédiées à l'envoi et à la réception de messages au serveur

    A. Connexion.......................................................271

        1. Définition de Connexion()..................................................271

            Cette fonction sert à se connecter au serveur et à Envoyer le nom 
            d'utilisateur, la clé publique, le module de chiffrement au serveur, et on 
            recoit les informations de chiffrement du serveur, la clé publique et le 
            module de chiffrement. Si le serveur demande un mot de passe,  c'est cette 
            fonction qui le récupére auprès de l'utilisateur, le chiffre et l'envoi au 
            serveur.

    B. Définition de AffichageConversations().......................................381

        Cette fonction sert à générer l'interface de la conversation
   
    C.Envoyer et recevoir.............................................................450

        1. Définition de Envoyer().....................................................450

            Fonctions qui fonctionne avec deux mode :

                - Le mode "automatique": La fonction récupere la valeur du champ de saisie
                et l'envoi au serveur
                
                - Le mode "manuel": La fonction est appellée et envoie le message au serveur

        2.définition de recevoir()....................................................593

IV.Barre d'application................................................................676
    A.définition de retournerMenu()...................................................676
    B.définition de infosServeur()....................................................732
    C.définition de aide()............................................................777
    D.Activer et désactiver le son....................................................817
        1.définition de activerSon()..................................................817
        2.définition de couperSon()...................................................826
    E.définition de Contact().........................................................836

V.définition de fermeture()...........................................................891

VI.Lancement du programme.............................................................902

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



def AfficherMenu():

    #FINIE

    """ Fonction qui affiche le menu principal de l'application """

    global MessageBienvenue, CadreBouttons, Logo

    Logo = Label(fen, bg="grey", image=ImageLogo)
    Logo.pack()

    MessageBienvenue = Label(fen, text="Bienvenue dans Kripto. Pour démarrez, dites-nous \nsi vous voulez être hôte ou bien client.", bg="grey", font=PoliceTitre)
    MessageBienvenue.pack()

    CadreBouttons = Frame(fen, bg="grey")
    CadreBouttons.pack(pady=60)

    BouttonHôte = Button(CadreBouttons, text="Être hôte", font=PoliceBoutton, command=DevenirHôte)
    BouttonHôte.pack(side=LEFT, padx=7)

    BouttonClient = Button(CadreBouttons, text="Être client", font=PoliceBoutton, command=DevenirClient)
    BouttonClient.pack(side=LEFT, padx=7)


def DevenirHôte():

    #FINIE

    """ Fonction qui affiche l'interface qui permet de définir l'Ip et le port qui seront
    utilisées par le serveur. """

    global InputIp, IP, InputPort, InputNom, CadreParamètres, SousMenuCliqué

    SousMenuCliqué = True
    #Si l"utilisateur veut retourner au menu, on sait qu'il est dans un sous-menu

    MessageBienvenue.pack_forget()
    CadreBouttons.pack_forget()

    Machine = socket.gethostname()
    IP = socket.gethostbyname(Machine)

    CadreParamètres = Frame(fen, bg="grey")
    CadreParamètres.pack()

    # Label de l'adresse Ip
    Label(CadreParamètres, text="Votre Adresse IP", bg="Grey").pack(anchor=CENTER, pady=7)
    # Pas besoin de stocker les labels dans une variable, on n'aura pas besoin de les 
    # récupérer plus tard

    InputIp = Entry(CadreParamètres)
    InputIp.insert("end", IP) #On insére l'Ip qu'on à récupéré auparavant
    InputIp.pack(anchor=CENTER)

    #Label du port
    Label(CadreParamètres, text="Port", bg="Grey").pack(anchor=CENTER, pady=7)

    InputPort = Entry(CadreParamètres)
    InputPort.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["PortPréféré"] != "Inconnu":
    # Si l'utilisateur a définit un port par défaut
        Fonctions.placeholder(InputPort, Paramètres.DicoParamètres["PortPréféré"], True)
        #La fonction placeholder reproduit à peu prés le même comportement que l'attribut HTML du
        # même nom : Elle sert à afficher une suggestion qui s'efface de la zone de saisie au clic
        # sur cette dernière.

    else:
        
        PortRecommandé = randint(49152, 65535)
        #On recommande un port dans la plage de ceux les moins utilisés
        Fonctions.placeholder(InputPort, PortRecommandé, True)

    #Label du nom d'utilisateur
    Label(CadreParamètres, text="Votre nom d'utilisateur", bg="Grey").pack(anchor=CENTER, pady=7)

    InputNom = Entry(CadreParamètres)
    InputNom.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["NomUserDéfaut"] != "Inconnu":
    # Si l'utilisateur a définit un nom d'utilisateur par défaut
        Fonctions.placeholder(InputNom, Paramètres.DicoParamètres["NomUserDéfaut"], True)

    else:

        SuggestionNom = choices(ListeNoms)
        Fonctions.placeholder(InputNom, SuggestionNom[0], True)

    InputNom.bind("<Button-1>", lambda z: Fonctions.placeholder(InputNom, "", False))
    #On utilise une fonction anonyme lambda pour pouvoir exécuter une fonction avec des arguments
    #On associe le clic gauche sur la zone de saisie du nom à la fonction placeholder, qui effacera le contenu
    # de la zone si c'est la suggestion originale

    InputPort.bind("<Button-1>", lambda z: Fonctions.placeholder(InputPort, "", False))

    BouttonDémarrer = Button(CadreParamètres, text="Démarrer", command=DémarrerServeur)
    BouttonDémarrer.pack(pady=20)

def DémarrerServeur():

    """ Cette fonction récupére les coordonées du serveur saisis dans le menu d'hôte, et lance
    le thread du serveur """

    global InputIp, IP, InputPort, Port, Rôle, InputNom, FichierSauvegarde, MotDePasse, NomUser

    if len(InputNom.get()) > 16:

        tkinter.messagebox.showerror(title="Nom d'utilisateur trop long", message="Votre nom d'utilisateur doit faire moins de 16 caractères")
        return False
        #On stoppe l'exécution de la fonction

    Rôle = "Hôte"
    IP = InputIp.get()

    try: Port = int(InputPort.get())
    except ValueError:

        tkinter.messagebox.showerror(title="Problème de port", message="Le port doit être un nombre entier entre 1 et 65535")
        return False

    Serveur.Démarrer(IP, Port, Paramètres.DicoParamètres["NombreUsersMax"], Paramètres.DicoParamètres["MotDePasse"])

    time.sleep(0.2)
    #On attend que le serveur démarre

    if Connexion() == True:
    #Si la connexion est une réussite, on affiche les conversations

        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":

            MotDePasse = tkinter.simpledialog.askstring("Mot de passe", "Veuillez saisir le mot de passe de la sauvegarde", show="•")
            ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Veuillez confirmer le mot de passe", show="•")

            while ConfirmationMotDePasse != MotDePasse:

                ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation erroné", "Les deux mots de passe ne correspondent pas. Veuillez confirmer le mot de passe", show="•")

            FichierSauvegarde = Sauvegarde.InitialisationSauvegarde(MotDePasse)

        AffichageConversations()


def DevenirClient():

    # FINIE

    """ Cette fonction affiche l'interface qui permet choisir à quel serveur se connecter"""

    global InputIp, InputPort, InputNom, CadreParamètres, SousMenuCliqué

    SousMenuCliqué = True
    #Si l"utilisateur veut retourner au menu, on sait qu'il est dans un sous-menu

    MessageBienvenue.pack_forget()
    CadreBouttons.pack_forget()

    CadreParamètres = Frame(fen, bg="grey")
    CadreParamètres.pack()

    #Label Adresse ip du serveur
    Label(CadreParamètres, text="Adresse IP du serveur", bg="Grey").pack(anchor=CENTER, pady=7)

    InputIp = Entry(CadreParamètres)
    InputIp.insert("end", "192.168.1.")
    InputIp.pack(anchor=CENTER)

    PortduServeur = Label(CadreParamètres, text="Port du serveur", bg="Grey")
    PortduServeur.pack(anchor=CENTER, pady=7)

    InputPort = Entry(CadreParamètres)
    InputPort.pack(anchor=CENTER)

    #Label de nom
    Label(CadreParamètres, text="Votre nom d'utilisateur", bg="Grey").pack(anchor=CENTER, pady=7)

    InputNom = Entry(CadreParamètres)
    InputNom.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["NomUserDéfaut"] != "Inconnu":
    # Si l'utilisateur a définit un nom d'utilisateur par défaut
        Fonctions.placeholder(InputNom, Paramètres.DicoParamètres["NomUserDéfaut"], True)

    else:
        SuggestionDeNom = choices(ListeNoms)
        Fonctions.placeholder(InputNom, SuggestionDeNom[0], True)

    InputNom.bind("<Button-1>", lambda b: Fonctions.placeholder(InputNom, "", False))
    #On utilise une fonction anonyme lambda pour pouvoir executer une fonction avec des arguments

    Button(CadreParamètres, text="Se connecter",  command=SeConnecter).pack(pady=20)


def Connexion():

    # FINIE

    """ Cette fonction sert à se connecter au serveur et à Envoyer le nom d'utilisateur, la clé publique, le module de chiffrement au serveur,
    et on recoit les informations de chiffrement du serveur, la clé publique et le module de chiffrement. Si le serveur demande un mot de passe,
    c'est cette fonction qui le récupére auprès de l'utilisateur, le chiffre l'envoi au serveur."
    """

    global IP, Port, NomUser, InputNom, ConnexionSocket, InputIp, Rôle, CléPublique, CléPubliqueServeur, ModuleServeur

    IP = InputIp.get()
    NomUser = InputNom.get()

    ConnexionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On défini notre connexion socket
    # - AF_INET => Protocole IPV4
    # - SOCK_STREAM => Stream veut dire cours d'eau, comme un flot continu de donnés qui est envoyé

    ConnexionSocket.settimeout(5)
    #Si au bout de 5secondes, il n'y pas de réponse (Délai plus que nécéssaire pour des simples paquets TCP) une exception est générée

    try: ConnexionSocket.connect((IP, Port))

    except (ConnectionRefusedError, socket.timeout):
    #Si on arrive pas à se connecter au serveur

        if Rôle != "Hôte":
        #Si c'est l'hôte, il a déja recu l'erreur de la part du serveur donc affiche rien

            MessageErreur = "IL semblerait que les coordonées du serveur ne soit pas valides. Réferez vous à l'aide pour régler ce problème."
            tkinter.messagebox.showerror(title="Aïe...", message=MessageErreur)
    
        return False
    
    else:

        InfosChiffrement = f"{NomUser}|{CléPublique}|{Module}"
        InfosChiffrement = InfosChiffrement.encode('utf-8')

        ConnexionSocket.send(bytes(InfosChiffrement))
        #On formate, puis on envoi les informations de chiffrement au serveur

        AutorisationEtDonnées = ConnexionSocket.recv(4096)
        AutorisationEtDonnées = AutorisationEtDonnées.decode("utf-8")
        #On recoit de la part du serveur l'autorisation de se connecter, et les informations de chiffrement du serveur

        if AutorisationEtDonnées != "False":
        #Si le serveur autorise la connexion

            AutorisationEtDonnées = AutorisationEtDonnées.split("|")
            #On récupere les données sous forme de le liste

            CléPubliqueServeur = int(AutorisationEtDonnées[0])
            ModuleServeur = int(AutorisationEtDonnées[1])
            PrésenceMotDePasse = AutorisationEtDonnées[2]

            if PrésenceMotDePasse == "True" and Rôle != "Hôte":
            # l'hôte n'a pas besoin de se connecter

                ConnexionEnAttente  = True

                while ConnexionEnAttente:

                    MotDePasseServeur= tkinter.simpledialog.askstring("Mot de passe du serveur", "Ce serveur demande un mot de passe pour se connecter", show="•")

                    if MotDePasseServeur == None or MotDePasseServeur == "":
                    #Si l'utilisateur annule la connexion, il faut se déconnecter du serveur

                        ConnexionSocket.close()
                        return False

                    else:

                        MotDePasseServeurChiffré = ChiffrementRSA.chiffrement(MotDePasseServeur, CléPubliqueServeur, ModuleServeur)

                        ConnexionSocket.send(bytes(MotDePasseServeurChiffré, "utf-8"))

                        Autorisation = ConnexionSocket.recv(4096)
                        Autorisation =  Autorisation.decode("utf-8")

                        if Autorisation == "OK":
                            ConnexionEnAttente = False

                        else:
                            tkinter.messagebox.showwarning(title="Mot de passe incorrect", message="Le mot de passe est incorrect")


            ConnexionSocket.setblocking(0)
            #On définit le mode de connexion sur non bloquant (Voir explications dans la fonction réception)

            return True
            #On retoune que la connexion a été validé

        else:
        #Si le serveur ne donne pas son autorisation

            motif = ConnexionSocket.recv(4096)
            #On recoit du serveur le motif du refus de

            tkinter.messagebox.showerror(title="Connexion refusée par le serveur", message=motif.decode("utf-8"))
            return False


def SeConnecter():

    #FINIE

    """ Fonction qui affiche l'interface de discusion si la connexion au serveur est une réussite"""

    global InputIp, IP, InputPort, Port, Rôle, FichierSauvegarde, MotDePasse

    Rôle = "Client"
    Port = int(InputPort.get())
    IP = InputIp.get()

    if Connexion() == True:

        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":

            MotDePasse = tkinter.simpledialog.askstring("Mot de passe", "Veuillez saisir le mot de passe de la sauvegarde", show='*')
            ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Veuillez confirmer le mot de passe", show='*')

            while ConfirmationMotDePasse != MotDePasse:

                ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Confirmation erronée. Veuillez confirmer le mot de passe", show='*')

            FichierSauvegarde = Sauvegarde.InitialisationSauvegarde(MotDePasse)

        AffichageConversations()

    
def AffichageConversations():

    #FINIE

    """ Cette fonction sert à générer l'interface de la conversation"""

    global CadreParamètres, SaisieMessage, NomUser, FilsMessages, BouttonEnvoyer, Connexion, ThreadRéception

    Logo.pack_forget()
    CadreParamètres.pack_forget()

    BarreMenu.delete(1)
    BarreMenu.insert_command(1, label="Menu", command= lambda : retournerMenu(DemandeConfirmation = True, ConversationEnCours = True))
    #On remplace la commande "Menu" pour car la commande associée doit avoir l'argument "ConversationEnCours" à jour

    BarreMenu.insert_command(2, label="Couper Son", command=couperSon)
    BarreMenu.insert_command(4, label="Infos du serveur", command=infosServeur)

    FilsMessages = Listbox(fen, width="70", height="20")
    FilsMessages.pack(pady=15)

    SaisieMessage = Entry(fen, width="60")
    SaisieMessage.pack()

    BouttonEnvoyer = Button(fen, text="Envoyer", command=Envoyer)
    BouttonEnvoyer.pack(pady=15)

    SaisieMessage.bind("<Button-1>", lambda a: Fonctions.placeholder(SaisieMessage, "", False))
    #On utilise une lambda pour appeler une fonction avec des arguments

    fen.bind_all('<Return>', lambda c: Envoyer())
    #On associe l'appui a a fonction Envoyer avec une fonction lambda afin de pouvoir Envoyer aucun argument

    Connexion = True #Tant que cette variable est égale à True, le thread tournera

    ThreadRéception = threading.Thread(target=recevoir)
    ThreadRéception.daemon = True #Cet attribut signifie que quand il ne reste que ce thread, le programme s'arrête.
    ThreadRéception.start()

    Fonctions.placeholder(SaisieMessage, "Saisissez votre message ici", True)


def Envoyer(ModeManuel = False, MessageManuel = None):

    #FINIE

    #Le mode manuel est un mode qui ne récupére pas l'entrée, mais le message passé en argument

    """Fonction qui chiffre et envoi les message au serveur. Les messages sont chiffrés en fonction du serveur"""

    global SaisieMessage, NomUser, FilsMessages, ConnexionSocket, NombreErreurs, CléPubliqueServeur, ModuleServeur, SonActivé, EnvoiPossible

    if ModeManuel == True: message = MessageManuel
    else: message = SaisieMessage.get()

    if len(message) > 1000: tkinter.messagebox.showerror(title="Attention au spam !", message="Afin d'éviter de surcharger le serveur, les messages de plus de 1000 caractères sont interdits")

    elif message == "": pass
    elif message[0] == "/":

        RéponseUser = None
        stop = False

        if message == "/stop" and ModeManuel == False and Role == "Hote":

            RéponseUser = tkinter.messagebox.askokcancel("Kripto","Voulez vraiment arrêter le serveur ?")
            stop = True

        elif message == "/stop" and ModeManuel == False and Role == "Client":

            tkinter.messagebox.showerror(title = "Erreur de permission", message = "Vous ne pouvez pas arrêter le serveur, vous n'êtes pas l'hôte de la disscusion")


        if RéponseUser == True and Role == "Hote" or ModeManuel == True or message != "/stop":

            message = Fonctions.formaterPaquet("Commande", message)
            message = ChiffrementRSA.chiffrement(message, CléPubliqueServeur, ModuleServeur)

            messageFinal = f"{len(message)}-{message}"
            messageFinal = messageFinal.encode('utf-8')

            try: ConnexionSocket.send(bytes(messageFinal))
            except (ConnectionResetError, ConnectionAbortedError):
            #Si le serveur ne répond pas

                if NombreErreurs < 3:
                    tkinter.messagebox.showerror(title="Aïe...", message="Impossible de joindre le serveur. Veuillez réessayer.")
                    NombreErreurs += 1
                else:
                #Si il y'a plus de trois erreurs, on stoppe le programme, en invitant l'utilisateur à se reconnecter

                    messsageErreur = "Le serveur est injoignable pour le moment. Veuillez vous reconnecter ou bien référez vous à l'aide"
                    tkinter.messagebox.showerror(title="Aïe...", message=messsageErreur)
                    retournerMenu(DemandeConfirmation = False, ConversationEnCours = True)

            if stop == True: retournerMenu(DemandeConfirmation = None, ConversationEnCours = True, DemandeArrêt = False)

    elif len(message) != 0 and EnvoiPossible:

        EnvoiPossible = False

        messageInterface = f"[{time.strftime('%H:%M:%S')}] {NomUser} → {message}"
        #On garde de coté un message avec un formaté spécialement pour l'interface, mais on ne l'utilise que si l'envoi est réussi.

        message = Fonctions.formaterPaquet("Message", message)

        message = ChiffrementRSA.chiffrement(message, CléPubliqueServeur, ModuleServeur)
        messageFinal = f"{len(message)}-{message}"
        #On rajoute un en tête avec la longueur totale du message
        messageFinal = messageFinal.encode('utf-8')

        try: ConnexionSocket.send(bytes(messageFinal))
        except (ConnectionResetError, ConnectionAbortedError):
        #Si le serveur ne répond pas

            if NombreErreurs < 3:
                tkinter.messagebox.showerror(title="Aïe...", message="Impossible de joindre le serveur. Veuillez réessayer.")
                NombreErreurs += 1

            else:
            #Si il y'a plus de trois erreurs, on stoppe le programme, en invitant l'utilisateur à se reconnecter

                messsageErreur = "Le serveur est injoignable pour le moment. Veuillez vous reconnecter ou bien référez vous à l'aide"
                #On stocke le message dans un variable pour diminuer la taille de la ligne d'en dessous
                tkinter.messagebox.showerror(title="Aïe...", message=messsageErreur)
                retournerMenu(DemandeConfirmation = False, ConversationEnCours = True)

        else:
        #Si il n'a pas eu d'execeptions

            if len(messageInterface) > 70:
            #Si le message à afficher fait plus de 70 caratères

                LignesMessages = Fonctions.couperPhrases(messageInterface)
                #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                for ligne in LignesMessages:
                    FilsMessages.insert(END, ligne)

                    if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                        Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, ligne)
            else:
                FilsMessages.insert(END, messageInterface)

                if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                    Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, messageInterface)

            FilsMessages.yview(END)
            #On défile tout en bas cette dernière, vers le message le plus récent

            if SonActivé == True:

                if Paramètres.DicoParamètres["SonEnvoi"] != "Inconnu":
                    winsound.PlaySound("Sons/" + Paramètres.DicoParamètres["SonEnvoi"], winsound.SND_ASYNC)

                else:
                    winsound.PlaySound("Sons/Pop.wav", winsound.SND_ASYNC)

            SaisieMessage.delete(0, 'end')
            #On vide la zone de saisie du message

            def RéactivationEnvoi():

                global EnvoiPossible

                EnvoiPossible = True

            fen.after(500, RéactivationEnvoi)
            #Au bout de 500ms en asynchrone, on appelle la fonction qui rendra possible l'envoi de messages

def recevoir():

    """ Fonction qui s'appelle elle même toutes les 10ms qui permet de vérifier
    la présence de nouveaux messages"""

    global FilsMessages, ConnexionSocket, CléPrivée, Module, SonActivé, Connexion
    #On récupere les variables nécéssaires au fonctionemment de la fonction

    while Connexion == True:
        try:
        #Cette partie du code est dans un bloc "try, except" car "ConnexionSocket.setblocking(0)" a été défini sur False
        #Au lieu d'attendre un message, si rien n'est envoyé cela va générer une exception, ce qui permet un fonctionnement asynchrone.

            messageRecu = ConnexionSocket.recv(32768)
            #32768 est la limite d'octets recevables
            messageRecu = messageRecu.decode("utf-8")

            if messageRecu != "":

                messageRecu = messageRecu.split("-")
                #Le message comporte un petit entête
                #Exemple = 564-6646464/65656/4564564654, 564 est içi la longueur totale du message. Cela peut arriver que les très long messages (Fichiers)
                #fassent plus de 2048 la taille taille du buffer

                LongeurMessage = int(messageRecu[0])

                while len(messageRecu[1]) < LongeurMessage:
                #Tant que le message recu est plus petit que la longueur totale du message

                    suite = ConnexionSocket.recv(32768)
                    suite = suite.decode("utf-8")

                    messageRecu[1] += suite
                    #On ajoute la suite du message recu

                messageRecu = ChiffrementRSA.déchiffrement(messageRecu[1], CléPrivée, Module)
                #On ne déchiffre que l'index 1 du message, qui est le messge en lui même
                #0 étant la longueur de ce message

                if len(messageRecu) > 70:
                #Si le message à afficher fait plus de 70 caratères

                    LignesMessages = couperPhrases(messageRecu)
                    #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                    for ligne in LignesMessages:
                    #On insere chaque ligne
                        FilsMessages.insert(END, ligne)

                        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                            NouvelleLigne(FichierSauvegarde, MotDePasse, ligne)
                            #On sauvegarde la ligne

                else:
                    FilsMessages.insert(END, messageRecu)

                    if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                        Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, messageRecu)
                        #On sauvegarde le nouveau message

                FilsMessages.yview(END)
                #On insére le message dans la listbox des messages, puis on force le défilement tout en bas de cette dernière

                if SonActivé == True:
                    if Paramètres.DicoParamètres["SonRéception"] != "Inconnu":
                        winsound.PlaySound("Sons/" + Paramètres.DicoParamètres["SonRéception"], winsound.SND_ASYNC)
                    else:
                        winsound.PlaySound("Sons/Dong.wav", winsound.SND_ASYNC)
            else:
                print("message vide")

        except BlockingIOError:
        #Si aucun message n'a été envoyé, on ne fait rien et on attend pour préserver les ressources la machine
            time.sleep(0.1)

        except (ConnectionAbortedError, ConnectionResetError):
        #Le serveur a crashé

            tkinter.messagebox.showerror(title="Aïe...", message="Le serveur a crashé...")
            exit()



def retournerMenu(DemandeConfirmation = None, ConversationEnCours = None, DepuisMenu = None, DemandeArrêt = True):

    global FilsMessages, SaisieMessage, BouttonEnvoyer, SousMenuCliqué, Connexion

    Confirmation = None

    if DemandeConfirmation == True:
        Confirmation = messagebox.askquestion (f"Vous partez déja {NomUser} ?","Vous voulez vraiment retourner au menu ?",icon = 'warning')

    if Confirmation == "yes" or DemandeConfirmation == None:

        if ConversationEnCours:

        #Si l'utilisateur était dans la fenêtre de conversation

            SousMenuCliqué = False

            if Role == "Hote" and  DemandeArrêt == True:

                Envoyer(True, "/stop") #L'envoi du /stop permet d'éviter au serveur de crasher / tourner dans le vide
                time.sleep(0.3)

            BarreMenu.delete(1)
            BarreMenu.insert_command(1, label="Menu", command= lambda : retournerMenu(DepuisMenu = True))
            #On remplace la commande "Menu" pour car la commande associée doit avoir l'argument "ConversationEnCours" à jour

            FilsMessages.pack_forget()
            SaisieMessage.pack_forget()
            BouttonEnvoyer.pack_forget()

            fen.unbind_all(ALL)

            BarreMenu.delete(2)
            BarreMenu.delete(3)
            #On efface les commandes "Couper Son" et "Infos Serveur" du menu

            Connexion = False
            ConnexionSocket.close()

        if DepuisMenu:
        #Si l'utilisateur était dans la fenêtre de menu

            if SousMenuCliqué:
            #Si l'utilisateur était dans le sous menu (Démarrage du serveur ou connexion)

                logo.pack_forget()
                CadreParamètres.pack_forget()

        if SousMenuCliqué or ConversationEnCours:
        #Si l"utilisateur n'est pas dans le menu principal

            if SousMenuCliqué:
                SousMenuCliqué = False

            AfficherMenu()


def infosServeur():
    """ Cette fonction affiches les informations du serveur dans une fenêtre en top level"""

    global IP, Port
    #On récupere les variables d'adresse du serveur

    def QuitterInfos():
        """Fonction qui détruit la fenêtre des infos du serveur"""
        fenInfos.destroy()

    fenInfos = Toplevel()
    fenInfos.geometry("300x280")
    fenInfos.configure(bg="grey")
    fenInfos.resizable(width=False, height=False)
    fenInfos.iconbitmap(bitmap="Médias/information.ico")
    fenInfos.title("Infos du serveur")
    #Définition de l'apparence de la fenêtre

    TitreAdresseServeur = Label(fenInfos, text="Adresse du serveur", bg="Grey", font=PoliceTitre)
    TitreAdresseServeur.pack(pady=10)

    AdresseServeur = Label(fenInfos, text=IP, bg="Grey", font=PoliceSousTitre)
    AdresseServeur.pack()

    TitrePortServeur = Label(fenInfos, text="Port du serveur", bg="Grey", font=PoliceTitre)
    TitrePortServeur.pack(pady=10)

    PortServeur = Label(fenInfos, text=Port, bg="Grey", font=PoliceSousTitre)
    PortServeur.pack()

    TitreUtilisateursCo = Label(fenInfos, text="Utiliseurs connectées", bg="Grey", font=PoliceTitre)
    TitreUtilisateursCo.pack(pady=10)

    UtilisateurCo = Label(fenInfos, text="N/C", bg="Grey", font=PoliceSousTitre)
    UtilisateurCo.pack()

    BouttonFermer = Button(fenInfos, text="Fermer", command=QuitterInfos)
    BouttonFermer.pack(pady=20, side=BOTTOM)

    fenInfos.focus_force()
    #On affiche la fenêtre au premier plan

    fenInfos.mainloop()


def aide():
    """ Cette fonction affiche l'aide dans une fenêtre en top level"""

    def QuitterAide():
        """Fonction qui détruit la fenêtre d'aide"""
        fenAide.destroy()

    fenAide = Toplevel()
    fenAide.geometry("300x280")
    fenAide.configure(bg="grey")
    fenAide.resizable(width=False, height=False)
    fenAide.iconbitmap(bitmap="Médias/information.ico")
    fenAide.title("Aide")
    #Définition de l'apparence de la fenêtre

    TitreAideIP = Label(fenAide, text="Si votre IP n'est pas valide", bg="Grey", font=PoliceTitre)
    TitreAideIP.pack(pady=10)

    AideIP0 = Label(fenAide, text="Entrez vous même l'adresse IPv4.\nPour la trouver :", bg="Grey", font=PoliceSousTitre)
    AideIP0.pack()

    AideIP1 = Label(fenAide, text="le-routeur-wifi.com/adresse-ip-mac/", bg="Grey", font=PoliceSousTitre, fg="blue")
    AideIP1.pack()
    AideIP1.bind("<Button-1>", lambda e: Fonctions.callback("https://le-routeur-wifi.com/adresse-ip-mac/"))

    TitreAidePort0 = Label(fenAide, text="Si votre port n'est pas valide", bg="Grey", font=PoliceTitre)
    TitreAidePort0.pack(pady=10)

    AidePort0 = Label(fenAide, text="Veillez à choisir un nombre entier\nentre 0 et 65535", bg="Grey", font=PoliceSousTitre)
    AidePort0.pack()

    BouttonFermer = Button(fenAide, text="Fermer", command=QuitterAide)
    BouttonFermer.pack(pady=20, side=BOTTOM)

    fenAide.focus_force()
    #On affiche la fenêtre au premier plan

    fenAide.mainloop()


def activerSon():
    global SonActivé

    SonActivé = True

    BarreMenu.delete(2)
    BarreMenu.insert_command(2, label="Couper Son", command=couperSon)
    #On supprime la commande à l'index 2 du menu pour y ajouter la commande couperSon à la même position

def couperSon():
    global SonActivé

    SonActivé = False

    BarreMenu.delete(2)
    BarreMenu.insert_command(2, label="Activer Son", command=activerSon)
    #On supprime la commande à l'index 2 du menu pour y ajouter la commande activerSon à la même position


def Contact():
    """ Cette fonction affiches les informations du serveur dans une fenêtre en top level"""

    def EnvoiAPI():

        TitreIssue = InputObjet.get()
        Message = InputMessage.get() + "\n" + platform.system() + " " + platform.release() + " " + platform.version()

        print(TitreIssue)
        print(Message)

    fenContact = Toplevel()
    fenContact.geometry("300x280")
    fenContact.configure(bg="grey")
    fenContact.resizable(width=False, height=False)
    fenContact.iconbitmap(bitmap="Médias/information.ico")
    fenContact.title("Contact")

    #Label d'objet
    Label(fenContact, text="Objet : ", bg="Grey", font=PoliceTitre).pack(pady=10)

    InputObjet = Entry(fenContact, width = 50, bg="White", font=PoliceSousTitre)
    InputObjet.pack(padx=20)

    #Label de message
    Label(fenContact, text="Message : ", bg="Grey", font=PoliceTitre).pack(pady=10)

    InputMessage = Entry(fenContact, width = 50, bg="White", font=PoliceSousTitre)
    InputMessage.pack(padx=20)

    Button(fenContact, text="Envoyer votre message", command=EnvoiAPI).pack(pady=20, side=BOTTOM)

    fenContact.focus_force()
    #On affiche la fenêtre au premier plan

    fenContact.mainloop()


def fermeture():

    """ Fonction appellée quand l'utilisateur veut fermer la fenêtre """

    RéponseUser  = tkinter.messagebox.askokcancel("Kripto","Vous partez déja ?")

    if RéponseUser == True:

        sys.exit()
        #On utilise sys.exit() plutôt que exit() car cela éviter au threads de tourner en arrière plan

#Code exécuté au démarage de l'application

Paramètres.LectureParamètres()

ListeNoms = ["Autruche", "Bob", "AmiralBenson", "TomNook", "Karamazov", "OdileDeray", "PatéEnCroute", "Risitas", "Clown"]
#La liste des noms qui seront suggérés à l'utilisateur.

FichierSauvegarde = None
MotDePasse = None
#Initilisation du mot de passe de la sauvegarde et le fichier de sauvegarde

Module, CléPublique, CléPrivée = ChiffrementRSA.génération(16)
#On génére une clé publique et une clé publique et on garde en mémoire le module de chiffrement

NombreErreurs = 0

EnvoiPossible = True
SonActivé = True
SousMenuCliqué = False

fen = Tk()
fen.geometry("550x460")
fen.title("Kripto - Un chat chiffré")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
fen.iconbitmap(bitmap="Médias/icone.ico")
fen.protocol("WM_DELETE_WINDOW", fermeture)

BarreMenu = Menu(fen)
BarreMenu.add_command(label="Menu", command= lambda : retournerMenu(DepuisMenu = True))
BarreMenu.add_command(label="Aide", command=aide)
BarreMenu.add_command(label="Sauvegardes", command=LecteurSauvegarde.LecteurSauvegarde)
BarreMenu.add_command(label="Paramètres", command=Paramètres.InterfaceParamètres)
BarreMenu.add_command(label="Contact", command=Contact)
fen.configure(menu=BarreMenu)

PoliceTitreBienvenue = tkFont.Font(family="Verdanna",size=16,weight="bold")
PoliceBoutton = tkFont.Font(family="Arial",size=12,weight="bold")
PoliceTitre = tkFont.Font(size=14,weight="bold")
PoliceSousTitre = tkFont.Font(size=12)

ImageLogo = PhotoImage(file="Médias/Logo.png")

AfficherMenu()
fen.mainloop()
