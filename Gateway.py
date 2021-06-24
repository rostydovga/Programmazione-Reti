import socket as sk
import sys, signal
import time
from threading import Thread

#costanti  
IP_interface_to_server = '10.10.10.10'
IP_gateway = '192.168.1.10'
GATEWAY_PORT = 10000
CLOUD_PORT = 9000
BUFFSIZE = 2048

#gateway deve conoscere gli ip dei 4 device
ip_address_devices = set(['192.168.1.20','192.168.1.21','192.168.1.22','192.168.1.23'])
#dizionario di tipo: ip --> rilevazioni
dictionary_data = {}

#gestisce le connessioni in entrata
def accept_connections():
    while True:
        try:
            data, address = sock.recvfrom(BUFFSIZE)    
            print('Received %s bytes from %s' % (len(data), address))            
            #chiamo i thread per la gestione del client
            Thread(target=data_management, args=(address,data,)).start()
        except KeyboardInterrupt:
            break

#metodo che apre una connessione verso il cloud ed invia i dati
def send_data_to_cloud(message):
    print('Send data to cloud...') 
    gatewaySocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    try:
        #si connette il gateway al cloud
        gatewaySocket.connect(('localhost',CLOUD_PORT))
    
        #si inviano i dati
        gatewaySocket.send(message.encode())
        response = gatewaySocket.recv(BUFFSIZE)
        print(f'Response from cloud: {response.decode()}')
        
    except Exception as data:
        print(f'Error type: {data}')
    finally:
        #si chiude il socket
        print('Closing gateway socket...\n\n')
        gatewaySocket.close()

#elabora i dati e li invia al cloud
def data_management(client,data):
    #estraggo l'Ip del client e le misurazioni
    ip_client ,t0 ,misurazioni = data.decode('utf8').split('#')
    
    #calcolo il tempo trascorso per inviare il pacchetto da device a gateway
    t_final = round(time.time()-float(t0),5)
    
    #aggiungo gli elementi al dizionario
    dictionary_data[ip_client] = misurazioni
    
    print(f'Time taken to transmit the UDP packet from: {ip_client} --> {t_final} seconds')
    
    #controllo di aver ricevuto le misurazioni da tutti i client
    if set(dictionary_data.keys()) == ip_address_devices:
        #creo le stringhe come richieste da progetto
        message = create_message_to_server(dictionary_data)
        print('Received all devices misurements')
        #pulisco il dizionario per le misurazioni future
        dictionary_data.clear()
        #invio i dati al cloud
        send_data_to_cloud(message)

#si occupa di creare il messaggio come da richiesta progetto
def create_message_to_server(dictionary):
    string = ''
    for key in dictionary.keys():
        #prelevo le misurazioni inerenti alla key(ip device)
        val = dictionary.get(key)
        #splitto le misurazioni in un array
        array = val.split('\n')
        #concateno tutte le stringhe 
        string = string + add_ip_to_rilevation(key,array)
    return string

#si occupa di concatenare l'ip del dispositivo alle rilevazioni
def add_ip_to_rilevation(ip,ril):
    output = ''
    for i in range(0,len(ril)-1,1):
        output = output + ip + ' - ' + ril[i] + '\n'
    return output
        
#libera il socket ed esce dal programma
def signal_handler(signal,frame):
    print('Closing the socket...')
    sock.close()
    sys.exit(0)


# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
gateway_address = ('', GATEWAY_PORT)
print ('\nstarting up gateway on %s port %s' % gateway_address)
sock.bind(gateway_address)
signal.signal(signal.SIGINT,signal_handler)

if __name__ == "__main__":
    accept_connections()
    #thread_connections = Thread(target=accept_connections)
    #thread_connections.start()
    #thread_connections.join()

    sock.close()
