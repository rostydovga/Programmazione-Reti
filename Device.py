import random
import datetime
import time
import socket as sk
from time import strftime

RANGE_RILEVAZIONI = 24

def generateInfo():

    t = random.randrange(0,35,1)
    u = abs(random.random()-(t//100))
    u = round(u,2)

    return t,u

def saveOnFile(ip,hour,temp,umid):
    a,b,c,d = ip.split('.')
    file = open(f'device{d}.txt','a')
    string = f'{hour} - {temp} - {umid}\n'
    file.write(string)
    file.close()


def extractDataFromFile(ip):
    a,b,c,d = ip.split('.')
    f = open(f'device{d}.txt','r+')
    output = f.read()
    #for line in f:
    #    output += ip + ' - ' + line  
    
    f.close()
    return output

def cleanFile(ip):
    a,b,c,d = ip.split('.')
    f = open(f'device{d}.txt','w') 
    f.close()


def sendData(message):        
    # Create il socket UDP
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

    gateway_address = ('localhost', 10000)
    try:

        # inviate il messaggio
        print ('sending "%s"' % message)
        sent = sock.sendto(message.encode(), gateway_address)

    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        sock.close()


class Device:
    #ip del device
    #timer tempo di misurazione per la temperatura
    def __init__(self, ip, timer):
        self.ip = ip
        self.timer = timer

    #funzione principale che runna il device indipendentemete l'uno dall'altro
    def runDevice(self):
        it = 0
        while True:
            #per sicurezza pulisco il file dai vecchi elementi, se presenti
            cleanFile(self.ip)
            #rappresenta le misurazioni nelle 24 ore
            for i in range(RANGE_RILEVAZIONI):
                #parte subito con l'aspettare la fine del timer
                time.sleep(self.timer)
                #genera i dati e prende l'orario corrente
                temp, umid = generateInfo()       
                ora = datetime.datetime.now().strftime('%H:%M:%S')
                #salva nel file il contenuto
                saveOnFile(self.ip,ora,temp,umid)

            print(f'Concluso il compito del device {self.ip}\n\n')
            print('Elementi nel file:\n')
            #estraggo i messaggi dal file 
            message = extractDataFromFile(self.ip)
            #aggiungo all header di message l'ip del device corrente
            #parte il tempo
            t0 = time.time()
            message = self.ip + '#' + str(t0) + '#' +  message
            sendData(message)
            #dopo che è stato inviato il messaggio il file del device viene ripulito per ospitare nuove rilevazioni
            cleanFile(self.ip)
            it+=1
            if it == 3:
                break

        #quado arriva a 24 ore di salvataggi crea una connessione UDP verso gateway ed invia i dati
