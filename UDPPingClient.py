#############################
# Name: Cooper Rachow       #
# Date: 2/5/24              #
# Assignment: Ping over UDP #
#############################

from socket import *
import sys, time
from datetime import datetime

# A message is displayed if argument count is not correct 
if len(sys.argv) != 4:
        print("Usage: python UDPPingClient.py <server_ip> <server_port> <ping_num>")
        quit()

# the arguments are parsed and assigned to correct variables
server_ip = sys.argv[1]
server_port = int(sys.argv[2])
ping_num = int(sys.argv[3])

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

# initializing key variables. minimum is set to a unreasonably high number so that the
# first rtt will guarentee lower than it and become our initial comparison
ping = 0 # controls order the ping is displayed in response 
total_sent = 0 # keep track of total segments sent 
recieved = 0
lost = 0
total_rtt = 0
minimum = 999999
maximum = 0

print(f"Pinging {server_ip}:")

# runs through however many pings the user desires 
for i in range(ping_num):
    # use datetime to create the required format to send to server 
    date = datetime.now()
    final_date = date.strftime("%a %b %d %I:%M:%S %Y")
    
    # increments "ping" & "total_sent", and begins start time then pings server waiting for response
    try:
        ping += 1
        total_sent += 1
        message = (f"Ping {ping} {final_date}")
        start = time.time()
        client_socket.sendto(message.encode(), (server_ip, server_port))

        # once recieved (it is incremented), the end time is aquired and used to solve the rtt. 
        # total rtt is solved by accumulating each rtt as each ping is received. Min and max rtt
        # is determined by comparing newest to the previous.
        recv_message, server_address = client_socket.recvfrom(2048)
        end = time.time()
        recieved += 1
        rtt = (end - start) * 1000
        total_rtt += rtt
        minimum = min(minimum, rtt)
        maximum = max(maximum, rtt)

        print(f"Reply from {server_ip}: {recv_message.decode()} time={rtt:.1f}ms TTL=1")

    # if the message is not receieved after one second, lost is incremented by 1 and user is notified
    # "ping"" is decremented due to maintaining order of each segement being recieved back
    except OSError as e:
        if "timed out" in str(e):
            ping -= 1
            lost += 1
            print("Request timed out")

lost_percent = lost/total_sent * 100 if total_sent > 0 else 0
average = total_rtt/recieved if recieved > 0 else 0

# statistics are printed after ping count is reached. A checker is placed in case all requests time out
print(f"\nPing statistics for {server_ip}:")
print(f"        Segments: Sent: {total_sent}, Received: {recieved}, Lost: {lost} ({lost_percent:.1f}% Loss)")
print("Approximate round trip times in ms:")
if minimum < 999999:
    print(f"        Minimum = {minimum:.1f}ms, Maximum = {maximum:.1f}ms, Average = {average:.2f}ms\n")
else:
    print(f"        Minimum = 0ms, Maximum = {maximum:.1f}ms, Average = {average:.2f}ms\n")
