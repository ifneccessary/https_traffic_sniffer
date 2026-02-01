import socket,struct



sk=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(socket.ETHERTYPE_IP))
# might need to be modifed
sk.bind(("wlan0",0))

while True:
    frame=sk.recv(2064)
    proto=struct.unpack('!1B',frame[23:24])[0]
    # can be changed to filter for specific protocol
    if proto==6:
        dst_mac=":".join(f"{c:02X}" for c in struct.unpack('!6B',frame[0:6]))
        src_mac=":".join(f"{c:02X}" for c in struct.unpack('!6B',frame[6:12]))
        src_ip=socket.inet_ntoa(frame[26:30])
        src_host=None
        dst_ip=socket.inet_ntoa(frame[30:34])
        dst_host=None
        try: 
         src_host=socket.gethostbyaddr(src_ip)
        except socket.herror:
           None
        try:   
         dst_host=socket.gethostbyaddr(dst_ip) 
        except socket.herror:
         None
        src_port=struct.unpack('!H',frame[34:36])[0]
        dst_port=struct.unpack('!H',frame[36:38])[0]
        # might need to  be  modified to  flter specific PORT Traffic
        if src_port==443 or dst_port==443:
         print(f"{src_host[0] if src_host else src_ip}{f"({src_ip})" if src_host else ''}:{src_port} ----> {dst_host[0] if dst_host else dst_ip}{f"({dst_ip})" if dst_host else ''}:{dst_port}")
    
    
