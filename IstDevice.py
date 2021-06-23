#importo la classe Device da Device 
from Device import Device
import threading

#Costante che indica ogni quanti secondi eseguire le misurazioni del terreno
TIMER_MISURATION = 1   
#lista degli ip dei device
ip_address_devices = ['192.168.1.20','192.168.1.21','192.168.1.22','192.168.1.23']

#funzione che esegue il metodo principale di Device
def startDevice(ip):
    Device(ip,TIMER_MISURATION).runDevice()

#numero dei device presenti nella lista
number_devices = len(ip_address_devices)

#creo i thread per i devices per eseguirli in parallelo
for i in range(number_devices):
    x = threading.Thread(target=startDevice,args=(ip_address_devices[i],))
    x.start()
    #x.daemon_threads = True  
    print(f'Creato device {ip_address_devices[i]}\n')
