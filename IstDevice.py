from Device import Device
import threading

TIMER_MISURAZIONE = 1
ip_address_devices = ['192.168.1.20','192.168.1.21','192.168.1.22','192.168.1.23']

def istanziaDevice(ip):
    Device(ip,TIMER_MISURAZIONE).runDevice()



number_devices = len(ip_address_devices)

for i in range(number_devices):
    print(f'Iterazione {i}')
    x = threading.Thread(target=istanziaDevice,args=(ip_address_devices[i],))
    x.start()
    x.daemon_threads = True  
    print(f'Creato device {ip_address_devices[i]}\n')






