'''
    Progetto Reti 2021 - Traccia 1 IoT
    Nicola Costa - Rostyslav Dovganyuk
'''

import random
import datetime
import time
import socket as sk
from time import strftime

#costante usata per simulare le 24 ore
RANGE_RILEVATION = 24
GATEWAY_PORT = 10000

#metodo per la generazione di temperatura ed umidità
def generateInfo():
    t = random.randrange(0,35,1)
    u = abs(random.random()-(t//100))
    u = round(u,2)
    return t,u

#metodo per il salvataggio dei dati nel file
def saveOnFile(ip,hour,temp,umid):
    #split dell'ip per nominare il file in modo esplicativo "device20.txt"
    a,b,c,d = ip.split('.')
    file = open(f'device{d}.txt','a')
    string = f'{hour} - {temp} - {umid}\n'
    file.write(string)
    file.close()

#metodo per estrarre il contenuto del file
def extractDataFromFile(ip):
    a,b,c,d = ip.split('.')
    file = open(f'device{d}.txt','r+')
    #viene salvato tutto il contenuto del file in output
    output = file.read()
    file.close()
    return output

#metodo per pulire il contenuto del file, aprendolo in modalità 'write' e chiudendolo
def cleanFile(ip):
    a,b,c,d = ip.split('.')
    file = open(f'device{d}.txt','w') 
    file.close()

#metodo per connettere il device al gateway e inviare i dati
def sendData(message):        
    #viene creato il socket UDP
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    gateway_address = ('localhost',GATEWAY_PORT)
    try:
        #viene inviato il messaggio contenente le rilevazioni
        print('sending "%s"' % message)
        sock.sendto(message.encode(), gateway_address)
    except Exception as info:
        print(info)
    finally:
        print('closing socket')
        sock.close()


'''
    Classe Device
'''
class Device:
    #ip: indirizzo ip del device
    #timer: ogni quanto tempo vengono rilevati i dati dal terreno
    def __init__(self, ip, timer):
        self.ip = ip
        self.timer = timer

    #metodo principale per l'esecuzione del device
    def runDevice(self):
        while True:
            #per sicurezza pulisco il file dai vecchi elementi, se presenti
            cleanFile(self.ip)
            
            #simula le misurazioni nelle 24 ore
            for i in range(RANGE_RILEVATION):
                #parte subito con l'aspettare la fine del timer
                time.sleep(self.timer)
                #genera i dati e prende l'orario corrente
                temp, umid = generateInfo()       
                hour = datetime.datetime.now().strftime('%H:%M:%S')
                
                #salva nel file i dati 
                saveOnFile(self.ip,hour,temp,umid)

            print(f'Device {self.ip} has completed the measurements\n')
            #estraggo i messaggi dal file 
            message = extractDataFromFile(self.ip)
            #concateno a message l'ip del device corrente e il tempo 0, necessario alla misurazione tempistiche trasmissive del pacchetto UDP
            t0 = time.time()
            message = self.ip + '#' + str(t0) + '#' +  message
            
            sendData(message)
            #dopo che è stato inviato il messaggio il file del device viene ripulito per ospitare nuove rilevazioni
            cleanFile(self.ip)         
