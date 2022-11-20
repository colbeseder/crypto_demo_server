#!python3
import http.server, urllib.parse, socketserver, os, string, random, sys, re, base64


from Cryptodome.Cipher import ARC4
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA
from Cryptodome import Random

""" Usage <PORT=8000> <SCHROOT=pwd>"""

default_port = 8000
DATA_FILE = "data.html"
KEY = b"YELLOW_SUBMARINE"

arg_count = len(sys.argv)

if arg_count < 2:
	PORT = default_port
else:
	try:
		PORT = int(sys.argv[1], 10)
	except ValueError:
		PORT = default_port

if arg_count > 2 and sys.argv[2]:
	SCHROOT = sys.argv[2] + "/"
else:
	SCHROOT = ""

def add_data(x):
	with open(DATA_FILE, "a") as myfile:
		myfile.write(x)
try:
    os.remove(DATA_FILE)
except:
    pass
add_data("Secret: 0J3/koz8ZH+sOoulenw0iA==<br>")

def rc4_encrypt(d):
	cipher = ARC4.new(KEY)
	return base64.b64encode(cipher.encrypt(d.encode())).decode("utf-8") 

class Berver(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		print("===============================================")
		path = self.path[1:]
		query = ""
		if "?" in path:
			path, query = path.split("?", 1)
		path = urllib.parse.unquote(path)
		self.path = path
		if path == "": #TODO: enter here for all directories
			path = "index.html"
		try:
			'''File: Return content'''
			path = SCHROOT + path
			print("Path: %s"%path)
			f = open(path, 'rb')
			content = f.read()
			self.send_response(200)
			if path[-5:] == ".html":
				self.send_header('Content-Type', 'text/html')
		except:
			try:
				'''Directory: Return listing'''
				listing = self.get_listing_page()
				content = bytes(listing, "utf-8")
				self.send_response(200)
				self.send_header('Content-Type', 'text/html')
			except:
				'''404 Not found'''
				content = self.get_404()
				self.send_response(404)
				self.send_header('Content-Type', 'text/html')
		#self.send_header('content-encoding', 'gzip')
		#print(self.headers)
		self.end_headers()
		self.wfile.write(content)

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		if self.path[1:] == "rc4_endpoint.html":
			string_data = post_data.decode("utf-8") 
			pat = r"alias=([^&]*)&secret=([^&]*)"
			m = re.search(pat, string_data)
			if m:
				new_data = "%s: %s<br>\n"%(m.group(1), rc4_encrypt(m.group(2)))
				print("new data: " + new_data)
				add_data(new_data)
			else :
				self.respond_now(500, "Bad request")
				return
		elif self.path[1:] == "AES_CBC_message":
			try:
				d = CBC_decrypt(base64.b64decode(post_data), KEY)
				print(d)
				self.respond_now(200, "thanks")
			except Exception as e:
				print(str(e))
				self.respond_now(500, str(e))
			return
				
			
		r = self.do_GET()
		sys.stdout.write("Request body:\t")
		print(post_data)
		return r

	def get_listing_page(self):
		result = '''<html>\n\t<head><meta charset="UTF-8"></head>\n\t<body>\n\t\t<div style="float:right">%s</div>\n\t\t<h1>%s</h1>\n'''%(rnd_string(), self.path)
		result += "\t\t<ul>\n"
		names = os.listdir(os.getcwd() + "/" + SCHROOT + self.path)
		localPath = self.path + "/"
		if localPath == "//":
			localPath = "/"
		if localPath[0] != "/":
			localPath = "/" + localPath
		for name in names:
			result += "\t\t\t<li><a href='%s'>%s</a></li>\n"%(localPath + name, name)
		result += '''\t\t</ul>\n\t</body>\n</html>'''
		return result

	def get_404(self):
		try:
			'''if 404.html exists, return it'''
			f = open("404.html", 'rb')
			content = f.read()
		except:
			'''Default 404 page'''
			content = bytes("File not found :-(", "utf-8")
		return content

	def respond_now(self, code, msg):
		self.send_response(code)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes(msg, "utf-8"))

	def serve_forever(port=8000):
		socketserver.TCPServer(('', port), Berver).serve_forever(PORT)

def rnd_string(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def CBC_decrypt(st, key, iv=b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'):
	prev = iv
	result = b""
	for i in range(0, len(st), 16):
		cipherBlock = st[i:i + 16]
		chainedBlock = ECB_decrypt(cipherBlock, key)
		plainBlock = XOR(chainedBlock, prev)
		prev = cipherBlock
		result += plainBlock
	return stripPKCS7(result)

def ECB_decrypt(st, key):
	iv = b'\0\0\0\0\0\0\0\0'
	cipher = AES.new(key, AES.MODE_ECB)
	msg = cipher.decrypt(st)
	#return stripPKCS7(msg)
	return msg


def stripPKCS7(st):
	padLength = st[-1]
	#print(padLength)
	#valdate padding
	for c in st[-padLength:]:
		if c != padLength:
			raise EnvironmentError("invalid padding")
			print("Invalid padding!")
			break
	return st[0:-padLength]

def XOR(str1, str2):
	result = b""
	for i in range(len(str1)):
		if i >= len(str2):
			break
		result += bytes([str1[i] ^ str2[i]])
	return result


print("Serving %s at http://localhost:%s"%(os.getcwd(), PORT))
Berver.serve_forever(PORT)