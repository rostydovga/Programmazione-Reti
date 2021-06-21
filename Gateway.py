import socket as sk
import socketserver
import time
from threading import Thread

port = 10000
BUFFSIZE = 4096
#gateway deve conoscere gli ip dei 4 device
ip_address_devices = ['192.168.1.20','192.168.1.21','192.168.1.22','192.168.1.23']
ip_address_recv = []
dictionary_data = {}
NUM_DEV = len(ip_address_devices)

def accetta_connessioni_in_entrata():
    while True:
        print('\n\r waiting to receive message...')
        data, address = sock.recvfrom(BUFFSIZE)

        print('received %s bytes from %s' % (len(data), address))
        #print (data.decode('utf8'))
        #chiamo i thread per la gestione del client
        Thread(target=gestione_client, args=(address,data,)).start()


def gestione_client(client,data):
    #ip_client, port_client = client
    #print(f'client --> {ip_client}   {port_client}')
    #print(f'data --> {data}\n')
    #ip_address_recv.recv(BUFFSIZE).append(ip_client)
    #estraggo l'Ip del client e le misurazioni
    ip_client ,misurazioni = data.decode('utf8').split('#')
    #aggiungo gli elementi al dizionario
    dictionary_data[ip_client] = misurazioni
    #print(f'ip client: {ip_client}\nmisurazioni ---> {misurazioni}\n\n')
    if len(dictionary_data.keys()) == NUM_DEV:
        #creo le stringhe come richieste da progetto
        message = createMessageToServer(dictionary_data)
        #print('Messaggio modificato...{message}')


    print(dictionary_data)


def createMessageToServer(dictionary):
    string = ''
    for key in dictionary.keys():
        val = dictionary.get(key)
        print('stampo un valore alla volta')
        
        #print(f'key = {key}, valori = {val}\n')
        

    return string




# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', port)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)

if __name__ == "__main__":
    #sock.listen(5)
    thread_accettazione = Thread(target=accetta_connessioni_in_entrata)
    thread_accettazione.start()
    thread_accettazione.join()
    
    sock.close
    


    
    
