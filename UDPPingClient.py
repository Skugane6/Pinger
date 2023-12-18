import socket
import time

port = 12000
server_address = ('localhost', port)
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

timeout_duration = 1.0
total_pings_to_send = 10
total_rtt_sum = 0
lost_packets_count = 0
current_sequence_number = 1

while current_sequence_number <= total_pings_to_send:
    ping_message = f'Ping {current_sequence_number} {time.time()}'
    udp_client_socket.sendto(ping_message.encode(), server_address)
    udp_client_socket.settimeout(timeout_duration)
    try:
        response, server_address = udp_client_socket.recvfrom(1024)
        rtt = time.time() - float(ping_message.split()[-1])
        print(f'Received response: {response.decode()}, RTT: {rtt:.6f} seconds')
        total_rtt_sum += rtt
    except socket.timeout:
        print(f'Request timed out')
        lost_packets_count += 1
    current_sequence_number += 1

packet_loss_rate_percentage = (lost_packets_count / total_pings_to_send) * 100
average_rtt_time = total_rtt_sum / (total_pings_to_send - lost_packets_count)

print(f'Ping statistics: {total_pings_to_send} packets transmitted, {lost_packets_count} packets lost, '
      f'{packet_loss_rate_percentage:.2f}% packet loss')

print(f'Round trip time (RTT) - Min/Avg/Max: {average_rtt_time:.6f}/{average_rtt_time:.6f}/{average_rtt_time:.6f} seconds')


udp_client_socket.close()
