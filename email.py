from socket import *
import ssl
import base64

#get all options from options.txt
optionFile = open("options.txt", "r")
options = optionFile.readlines()

#prepare options/message
server = options[0].split()
port = options[1].split()
fromEmail = options[2].split()
toEmail = options[3].split()
name = options[4].split()
subject = options[5].split()
emailMessage = options[6]
port = int(port[1])
emailMessage = emailMessage[9:]
message = 'From: ' + name[1] + '\r\n' + 'To: ' + toEmail[1] + '\r\n' + 'Subject: ' + subject[1] + '\r\n' + emailMessage + ' \r\n\n'
endmsg = '\r\n.\r\n'

# create socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server[1], port))
recv = clientSocket.recv(1024)
print 'From Server:', recv
if recv[:3] != '220':
	print '220 reply not recieved from server'
print recv

#send HELO command
heloCommand = 'EHLO ALICE\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
if recv1[:3] != '250':
	print 'HELO 250 reply not recieved from server'
print recv1

#send TLS command
tlsCommand = 'STARTTLS\r\n'
clientSocket.send(tlsCommand)
recvTLS = clientSocket.recv(1024)
if recvTLS[:3] != '220':
	print 'STARTTLS 220 reply not recieved from server'
print recvTLS

#wrap client socket with ssl socket
sslSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

#send authentication information
authCommand = 'AUTH LOGIN\r\n'
sslSocket.send(authCommand)
recvAuth = sslSocket.recv(1024)
if recvAuth[:3] != '334':
	print 'Authentication reply not recieved from server'
print recvAuth

#send encoded username and password
sslSocket.send(base64.b64encode('cuppabrownchai')+'\r\n')
print sslSocket.recv(1024)
sslSocket.send(base64.b64encode('zelda1990')+'\r\n')
print sslSocket.recv(1024)

#send mail from command
sslSocket.send("MAIL FROM:" + fromEmail[1] + '\r\n')
recv3 = sslSocket.recv(1024)
if recv3[:3] != '250':
	print 'MAIL FROM 250 reply not recieved from server.'
print recv3

#send rcpt to command
sslSocket.send("RCPT TO:" + toEmail[1] + '\r\n')
recv4 = sslSocket.recv(1024)
if recv4[:3] != '250':
	print 'RCPT 250 reply not recieved from server.'
print recv4

#send data command
dataCommand = "DATA\r\n"
sslSocket.send(dataCommand)
recv5 = sslSocket.recv(1024)
if recv5[:3] != '354':
	print 'DATA 354 reply not recieved from server.'
print recv5

#send my test message
sslSocket.send(message)
sslSocket.send(endmsg)

#send quit command
termCommand = 'QUIT\r\n'
sslSocket.send(termCommand)
recv6 = sslSocket.recv(1024)
if recv6[:3] != '250':
	print 'QUIT 250 reply not recieved from server.'
print recv6
