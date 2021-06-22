import sys, signal, time
import socket as sk

CLOUD_ADDRESS = '10.10.10.2'
CLOUD_PORT = 9000
BUF_SIZE = 4096

#libera i socket ed esce dal programma
def signal_handler(signal, frame):
    print('Exiting Cloud Server (Ctrl+C pressed)')
    #si chiudono i socket il programma
    gatewaySocket.close()
    cloudSocket.close()
    sys.exit(0)


if __name__ == '__main__':
    #si crea l'oggetto socket TCP
    cloudSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    #si associa il socket alla porta e all'indirizzo
    cloudSocket.bind(('localhost', CLOUD_PORT))
    #si abilita la connessione
    cloudSocket.listen(1)
    #se viene premuto Ctrl+C l'esecuzione si interrompe
    signal.signal(signal.SIGINT, signal_handler)
    print('Cloud Server ready...')
    
    while True:
        #il socket si prepara ad accettare la connessione con il gateway
        gatewaySocket, gatewayAddress = cloudSocket.accept()
        
        try:
            #parte il timer per calcolare il tempo impiegato
            start = time.time()
            #riceve il messaggio dal gateway
            message = gatewaySocket.recv(BUF_SIZE)
            print('received %s bytes' % (len(message)))
            #si calcola il tempo impiegato per ricevere il messaggio
            end = time.time() - start
            #si visualizzano i valori su console
            print(message.decode('utf-8'))
            #print('Time taken to transmit the TCP packet:', end, 'seconds\n\n')
            print(f'Time taken to transmit the TCP packet: {end} seconds\n\n')
            #si invia una risposta affermativa
            gatewaySocket.send("Data Received!".encode())
            #si rilascia il canale TCP
            gatewaySocket.close()
        except IOError:
            gatewaySocket.send("Error During Trasmition!".encode())
            gatewaySocket.close()