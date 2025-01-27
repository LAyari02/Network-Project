from scapy.all import ARP, Ether, srp

def scan_local_network(ip_range):
    print(f"Scanning the network: {ip_range}...\n")
    
    # Construire une trame Ethernet + ARP
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=ip_range)
    packet = ether / arp

    # Envoyer et recevoir des réponses
    result = srp(packet, timeout=2, verbose=0)[0]

    # Stocker les résultats
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def display_results(devices):
    print("Devices connected to the network:")
    print("IP Address\t\tMAC Address")
    print("-" * 40)
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}")

if __name__ == "__main__":
    # Définir la plage IP à scanner (exemple : réseau 192.168.1.0/24)
    ip_range = "10.13.0.0/24"
    
    # Scanner le réseau
    devices = scan_local_network(ip_range)
    
    # Afficher les résultats
    display_results(devices)
