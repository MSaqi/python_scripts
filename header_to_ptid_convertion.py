from scapy.all import *

file1 = open('input/Ether_header_ipv4+ipv6.txt', 'r')
file2 = open('input/renato_header_file.txt', 'r')
hdr_file = open('output/Header_out.txt'  , 'w')
ptid_bin_file = open('output/ptid_bin_out.txt', 'w')
ptid_hex_file = open('output/ptid_hex_out.txt', 'w')
tlayer_ptid_hex_file = open('output/tlptid_hex_out.txt', 'w')
single_flit_ptid_hex_file = open('output/sngle_flt_ptid_hex_out.txt', 'w')
multi_flit_ptid_hex_file = open('output/multi_flt_ptid_hex_out.txt', 'w')
multi_layer_ptid_hex_file = open('output/multi_layer_ptid_hex_out.txt', 'w')
multi_flit_2_layer_file = open('output/multi_flit_2_layer_file.txt', 'w')
total_pkt_length = 0
quic_len = 47
geneve_len = 8
nvgre_len = 8
bth_len = 17
stcp_len = 12
mpls_len = 4
layer_num = 0
length = 0

BTH      = 0
QUIC     = 1
udp      = 2
tcp      = 3
sctp     = 4
icmp     = 5  #this is ICMP4
icmp6    = 6
esp      = 7
ipv6     = 8
ip       = 9
arp      = 10
MPLS     = 11
dot1q    = 12   # VLAN 0 
dot1AD   = 13  # VLAN 1
Eth    = 14
GRE      = 15 
NVGRE    = 16
vxlan    = 17 
GENEVE   = 18
META_HDR = 19

def create_ptid(packet_format):
    ptid = [0]*80  # using this to store the ptid in 80 bit array 
    previous_hdr = 19
    ptid_layer = [[0]*20,[0]*20,[0]*20,[0]*20]
    ptid_20 = [0]*20
    layers = packet_format.split('/')
    layer_num = 0
    len_of_1_pkt = 0 
    layers = packet_format.split('/')
    length =0 
    for layer in layers:
        if layer == 'Ether()':       
            current_hdr = Eth
            len_of_1_pkt = len(Ether())
        elif layer == 'ARP()':
            current_hdr = arp 
            len_of_1_pkt = len(ARP())    
        elif layer == 'RARP()':
            current_hdr = arp   
            len_of_1_pkt = len(ARP())  
        elif layer == 'IP()':
            current_hdr = ip
            len_of_1_pkt = len(IP())
        elif layer == 'UDP()':
            current_hdr = udp
            len_of_1_pkt = len(UDP())
        elif layer == 'TCP()':
            current_hdr = tcp
            len_of_1_pkt = len(TCP())
        elif layer == 'ICMP()':
            current_hdr = icmp
            len_of_1_pkt =  len(ICMP())
        elif layer == 'MPLS()':
            current_hdr = MPLS
            len_of_1_pkt = mpls_len
        elif layer == 'dot1q()':
            current_hdr = dot1q
            len_of_1_pkt = len(Dot1Q())
        elif layer == 'VXLAN()':
            current_hdr = vxlan
            len_of_1_pkt = len(VXLAN())
        elif layer == 'GENEVE()':
            current_hdr = GENEVE
            len_of_1_pkt = geneve_len
        elif layer == 'NVGRE()':
            current_hdr = NVGRE
            len_of_1_pkt = nvgre_len
        elif layer == 'GRE()':
            current_hdr = GRE 
            len_of_1_pkt = nvgre_len
        elif layer == 'QUIC()':
            current_hdr = QUIC
            len_of_1_pkt = quic_len
        elif layer == 'BTH()':
            current_hdr = BTH 
            len_of_1_pkt = bth_len 
        elif layer == 'ESP()':
            current_hdr = esp
            len_of_1_pkt = len(ESP())
        elif layer == 'SCTP()':
            current_hdr = sctp
            len_of_1_pkt = len(SCTP())
        elif layer == 'IPv6()':
            current_hdr = ipv6     
            len_of_1_pkt = len(IPv6())    
        else:
            print("ERROR line should contain some valid header :",layer,"LINE from file ", packet_format )
        length= length + len_of_1_pkt
        if previous_hdr > current_hdr :
            ptid_20[current_hdr] = 1
            previous_hdr = current_hdr
            tunnel_found = 0
        else:
            for x in range(19):
                ptid_layer[layer_num][x] = ptid_20[x]      
            layer_num = layer_num + 1
            previous_hdr = current_hdr
            ptid_20 = [0]*20
            ptid_20[current_hdr] = 1
            tunnel_found = 1 
    for x in range(19):
        ptid_layer[layer_num][x]   =  ptid_20[x] 

    index = layer_num
    for x in range (layer_num+1):
        for y in range(20):
            ptid[y+(20*index)] = ptid_layer[x][y]  # copying the  small ptid to  bigger final ptid
        index = index -1 
    return ptid,length,layer_num
          
def main():
    # need to figure out the icmp case
    while 1:    
        # line = file1.readline() # renato upgraded file with ipv6 and ipv4 and with icmp issues
        line = file2.readline()   # renato header file 

        if not line:
            break       
        line = line.replace("\n","") 
        ptid,length,layer_num = create_ptid(line)

        print("line = ",line,"ptid = ",ptid)
        hdr_file.write(f"{line}")
        hdr_file.write("\n")
        print("reverse")    
        ptid.reverse()    
        for x in ptid:
            print(x, end='')     
            ptid_bin_file.write(str(x))
        ptid_bin_file.write("\n")
        num = 0    
        for bit in range(80):
            num = (num << 1) | ptid[bit]
        ptid_hex_file.write(f"'h{hex(num)[2:]}")
        ptid_hex_file.write("\n")
        print("\n PTID = ",hex(num))
        if layer_num < 2:
            print("Layers = ",layer_num)
            tlayer_ptid_hex_file.write(f"'h{hex(num)[2:]}")
            tlayer_ptid_hex_file.write("                =")
            tlayer_ptid_hex_file.write(f"{layer_num}")
            tlayer_ptid_hex_file.write("\n")
        else :
            print("Layers = ",layer_num)
            multi_layer_ptid_hex_file.write(f"'h{hex(num)[2:]}")
            multi_layer_ptid_hex_file.write("                =")
            multi_layer_ptid_hex_file.write(f"{layer_num}")
            multi_layer_ptid_hex_file.write("\n")
        if length <= 128 :
            print("HEADER_Length = ",length)
            single_flit_ptid_hex_file.write(f"'h{hex(num)[2:]}")
            single_flit_ptid_hex_file.write("                =")
            single_flit_ptid_hex_file.write(f"{length}")
            single_flit_ptid_hex_file.write("\n")
        else :
            print("HEADER_Length = ",length)
            multi_flit_ptid_hex_file.write(f"'h{hex(num)[2:]}")
            multi_flit_ptid_hex_file.write("                =")
            multi_flit_ptid_hex_file.write(f"{length}")
            multi_flit_ptid_hex_file.write("\n")
        if (layer_num < 2) & (length > 128):
            print("HEADER_Length = ",length)
            multi_flit_2_layer_file.write(f"'h{hex(num)[2:]}")
            multi_flit_2_layer_file.write("                =")
            multi_flit_2_layer_file.write(f"{layer_num}")
            multi_flit_2_layer_file.write("                =")
            multi_flit_2_layer_file.write(f"{length}")
            multi_flit_2_layer_file.write("\n")

if __name__ == '__main__':
  main()


