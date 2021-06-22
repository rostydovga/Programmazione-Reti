import socket as sk
import sys, signal
import time
from threading import Thread

IP_server_cloud = '10.10.10.1'
port = 10000
BUFFSIZE = 2048
#gateway deve conoscere gli ip dei 4 device
ip_address_devices = ['192.168.1.20','192.168.1.21','192.168.1.22','192.168.1.23']
dictionary_data = {}
NUM_DEV = len(ip_address_devices)

def accetta_connessioni_in_entrata():
    
    while True:
        try:
            
            data, address = sock.recvfrom(BUFFSIZE)
    
            print('received %s bytes from %s' % (len(data), address))
            
            #chiamo i thread per la gestione del client
            Thread(target=gestione_client, args=(address,data,)).start()
            
            #gestione_client(address,data)

            #dopo che tutti i client hanno inviato le misurazioni



        except KeyboardInterrupt:
            break

def send_data_to_cloud(message):
    print('Send data to cloud...') 
    gatewaySocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    try:
        #si connette il gateway al cloud
        gatewaySocket.connect(('127.0.0.1', 9000))
    except Exception as data:
        print(f'Errore di tipo {data}')
    #si inviano i valori
    gatewaySocket.send(message.encode())
    response = gatewaySocket.recv(BUFFSIZE)
    print(f'risposta dal cloud: {response.decode()}')
    print('chiusura Socket del gateway...\n\n')
    #si chiude il socket
    gatewaySocket.close()


def gestione_client(client,data):
    #estraggo l'Ip del client e le misurazioni
    ip_client ,t0 ,misurazioni = data.decode('utf8').split('#')
    
    #calcolo il tempo trascorso per inviare il pacchetto da device a gateway
    t_final = round(time.time()-float(t0),5)
    
    #aggiungo gli elementi al dizionario
    dictionary_data[ip_client] = misurazioni
    
    
    print(f'Time taken to transmit the UDP packet from: {ip_client} --> {t_final} seconds')
        #Thread(target=send_data_to_cloud, args=(message,)).start()
        #print(f'Messaggio per il server:\n{message}')
    if set(dictionary_data.keys()) == set(ip_address_devices):
        #creo le stringhe come richieste da progetto
        message = create_Message_To_Server(dictionary_data)
        print('RICEVUTE LE MISURAZIONI DI TUTTI I DEVICE')
        dictionary_data.clear()
        
        send_data_to_cloud(message)

        


def create_Message_To_Server(dictionary):
    string = ''
    for key in dictionary.keys():
        #prelevo le misurazioni inerenti alla key(ip device)
        val = dictionary.get(key)
        #splitto le misurazioni in un array
        array = val.split('\n')
        #concateno tutte le stringhe 
        string = string + add_Ip_to_Rilevation(key,array)

    
    return string


#si occupa di concatenare l'ip del dispositivo alle rilevazioni
def add_Ip_to_Rilevation(ip,ril):
    output = ''
    for i in range(0,len(ril)-1,1):
        output = output + ip + ' - ' + ril[i] + '\n'
    
    return output
        
    


def signal_handler(signal,frame):
    print('Closing the socket...')
    sock.close()
    sys.exit(0)


# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
gateway_address = ('localhost', port)
print ('\nstarting up on %s port %s' % gateway_address)
sock.bind(gateway_address)
signal.signal(signal.SIGINT,signal_handler)

if __name__ == "__main__":
    #sock.listen(5)
    #accetta_connessioni_in_entrata()
    thread_accettazione = Thread(target=accetta_connessioni_in_entrata)
    thread_accettazione.start()
    thread_accettazione.join()

    sock.close()



    
    
