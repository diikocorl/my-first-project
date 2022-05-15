import socket

def CreateServer(host,port):
	Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Server.bind((host,port)) #tao server
	Server.listen(5)
	return Server
	
def ReadRequest(Client):
	re = ''
	Client.settimeout(1)
	try:
		re = Client.recv(1024).decode()
		while (re):
			re = re + Client.recv(1024).decode()
	except socket.timeout: #fail after 1 second of no activity
		if not re:
			print("Didn't receive data! [Timeout]")
	finally:
		return re 




#2. Client connect Server + Read HTTP Request
def ReadHTTPRequest(Server):
	re = ''
	while (re==''):
		Client, address = Server.accept()
		print("Client: ",address," da ket noi toi server")
		re = ReadRequest(Client)
	return Client, re 
			
def SendFileLogin(Client):
	f = open("login.html","rb")
	L = f.read()
	header = """HTTP/1.1 200 OK
Content-Length: %d

"""%len(L)
	print("---------------HTTP Response login.html---------------")
	print(header)
	header += L.decode()
	Client.send(bytes(header,'utf-8'))
	
	
def MovePageLogin(Client):
	header="""HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8081/login.html

"""
	print("---------------HTTP Response move login.html---------------")
	print(header)
	Client.send(bytes(header,'utf-8'))
			
def MoveHomePage(Server,Client,Request):
	if "GET /login.html HTTP/1.1" in Request:
		SendFileLogin(Client)
		Server.close()
		return True
	if "GET / HTTP/1.1" in Request:
		#Move login.html
		MovePageLogin(Client) 
		Server.close()
		#Tra ve file login.html cho client
		Server = CreateServer("localhost",8081)
		Client, Request = ReadHTTPRequest(Server)
		print("---------------HTTP Request---------------")
		print(Request)
		MoveHomePage(Server,Client,Request)
		return True
	

def SendFileInfor(Client): 
	f = open ("infor.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
	print("-----------------HTTP respone  Infor.html--------------- ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def SendImg(Client, NameImg):
	with open(NameImg, 'rb') as f:
		L = f.read()
		header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
		print("-----------------HTTP respone images--------------- ")
		print(header)
		header =  bytes(header,'utf-8') + L
		Client.send(header)	


def SendInfor(Server, Client, Request):
	if "Username=admin&Password=123456" in Request:
		SendFileInfor(Client)
	#images
	
	Client, Request = ReadHTTPRequest(Server)
	print("---------------HTTP Request infor.html/images--------------- ")
	print(Request)
	if "GET /noll.jpg HTTP/1.1" in Request:
		SendImg(Client, "noll.jpg")
	if "GET /diiko.jpg HTTP/1.1" in Request:
		SendImg(Client, "diiko.jpg")
	if "GET /lian.jpg HTTP/1.1" in Request:
		SendImg(Client, "lian.jpg")

	Client, Request = ReadHTTPRequest(Server)
	print("---------------HTTP Request infor.html/images--------------- ")
	print(Request)
	if "GET /noll.jpg HTTP/1.1" in Request:
		SendImg(Client, "noll.jpg")
	if "GET /diiko.jpg HTTP/1.1" in Request:
		SendImg(Client, "diiko.jpg")
	if "GET /lian.jpg HTTP/1.1" in Request:
		SendImg(Client, "lian.jpg")

	Client, Request = ReadHTTPRequest(Server)
	print("---------------HTTP Request infor.html/images---------------")
	print(Request)
	if "GET /noll.jpg HTTP/1.1" in Request:
		SendImg(Client, "noll.jpg")
	if "GET /diiko.jpg HTTP/1.1" in Request:
		SendImg(Client, "diiko.jpg")
	if "GET /lian.jpg HTTP/1.1" in Request:
		SendImg(Client, "lian.jpg")

	Server.close()


if __name__ == "__main__":
	print("########## GIAO THUC HTTP ##########")	
	#1. Create server  
	Server = CreateServer("localhost",8080)
	#2. Client connect Server + Read HTTP Request
	Client, Request = ReadHTTPRequest(Server)
	print("---------------HTTP request Login Form---------------")
	print(Request)
	#3. Send login.html + Close Server
	MoveHomePage(Server,Client,Request)

	#1. Create server  
	Server = CreateServer("localhost",10000)
	#2. Client connect Server + Read HTTP Request
	Client, Request = ReadHTTPRequest(Server)
	print("---------------HTTP request WhoWhatWear---------------")
	print(Request)
	#3. Send infor.html + Close Server
	SendInfor(Server, Client, Request)
	
	
	
	
	
	
	
		
	
	