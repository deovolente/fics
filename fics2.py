import getpass
import sys
import telnetlib
import time

def login(host, handle, password, verbose=False):

	# Connect to FICS
	try:
    		f = telnetlib.Telnet(host) #connect to host
	except:
    		raise Error("Could not connect to host")
        if verbose:
		print "Connected to " + host
        
	# Await user input prompt
	f.read_until("login: ")
	try:
    		f.write(handle + "\n\r")
	except:
    		raise Error("Could not write username to host")
	if verbose:
		print "Logging in as " + handle + ", please wait..."
	
	if handle == "guest":
#    		print f.read_all()
		f.read_until(":\n\r")
		f.write("\n\r")
		if verbose:
			print "Logged in as guest - no password needed"
	else:
    		f.read_until("password: ")
		try:
    			f.write(password + "\n\r")
		except:
    			raise Error("Could not write password to host")
		if verbose:
			print "Password accepted :)"

	outp = f.read_until ("fics%", timeout=1)
	print ("{" + outp + "}")


	time.sleep(5)

	if (outp == ' '):
		if verbose:
			print "No prompt received"
	else:
		if verbose:
			print "Prompt received"

	return f


host = "freechess.org"
user = "guest"
tn = login(host,user,"",True)
print "Connected!"

tn.write("games" + "\r\n")
print tn.read_all()
	
