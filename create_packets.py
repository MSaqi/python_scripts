from scapy.all import *

file = open('Ether_header.txt', 'r')
total_pkt_length = 0
quic_len = 47
geneve_len = 8
nvgre_len = 8
bth_len = 17
stcp_len = 12
mpls_len = 4
 


def calculate_pkt_len(packet_format):
    len_of_1_pkt = 0 
    layers = packet_format.split('/')
    length =0 
    for layer in layers:
        if layer == 'Ether()':            
            len_of_1_pkt = len(Ether())
        elif layer == 'ARP()':
            len_of_1_pkt = len(ARP())
        elif layer == 'RARP()':
            len_of_1_pkt = len(ARP())
        elif layer == 'IP()':
            len_of_1_pkt = len(IP())
        elif layer == 'UDP()':
            len_of_1_pkt = len(UDP())
        elif layer == 'TCP()':
            len_of_1_pkt = len(TCP())
        elif layer == 'ICMP()':
            len_of_1_pkt =  len(ICMP())
        elif layer == 'MPLS()':
            len_of_1_pkt = mpls_len
        elif layer == 'dot1q()':
            len_of_1_pkt = len(Dot1Q())
        elif layer == 'VXLAN()':
            len_of_1_pkt = len(VXLAN())
        elif layer == 'GENEVE()':
            len_of_1_pkt = geneve_len
        elif layer == 'NVGRE()':
            len_of_1_pkt = nvgre_len
        elif layer == 'GRE()':
            len_of_1_pkt = nvgre_len 
        elif layer == 'QUIC()':
            len_of_1_pkt = quic_len
        elif layer == 'BTH()':
            len_of_1_pkt = bth_len 
        elif layer == 'BTH()':
            len_of_1_pkt = bth_len 
        elif layer == 'ESP()':
            len_of_1_pkt = len(ESP())
        elif layer == 'SCTP()':
            len_of_1_pkt = len(SCTP())      
        else:
            print(f"Invalid layer: {layer}")
        length= length + len_of_1_pkt
    return length

def main():

    while 1:
        line = file.readline()
        if not line:
            break       
        line = line.replace("\n","") 
        total_pkt_length = calculate_pkt_len(line)
        print("HEADER = ",line," size=",total_pkt_length,"bytes")

if __name__ == '__main__':
  main()


