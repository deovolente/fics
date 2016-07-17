import getpass
import sys
import telnetlib
import time


def right(s, amount):
    return s[-amount:]


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
		f.read_until(":\n\r")
		f.write("\n\r")
		if verbose:
			print "Logging in as guest - no password needed"
	else:
    		f.read_until("password: ")
		try:
    			f.write(password + "\n\r")
		except:
    			raise Error("Could not write password to host")
		if verbose:
			print "Password accepted :)"

	outp = f.read_until ("fics%", timeout=1)
#	print ("{" + right(outp, 5) + "}")


	if (right(outp, 5) <> 'fics%'):
		if verbose:
			print "No prompt received"
	else:
		if verbose:
			print "Prompt received"

	return f


def fics_cmd (session, command, completion_OK_text):
	try:
		session.read_very_eager()
		session.write(command + "\n\r")
		
		outp = session.read_until (completion_OK_text, timeout=1)
		if right(outp, len(completion_OK_text)) == completion_OK_text:
			return outp
		else:
			return ""

	except:
		raise Error("Unsuccessful command execution")




host = "freechess.org"
user = "guest"
tn = login(host,user,"",True)
print "Connected!"


if fics_cmd(tn, "set seek 0", "You will not see seek ads."):
	print "No more seek ads!"
else:
	print "Turning seek ads off unsuccessful"


# print fics_cmd(tn, "games", "games displayed.")

print fics_cmd(tn, "finger drakem", "fics%")





#tn.write("set seek 0" + "\n\r")
#outp = tn.read_until ("fics%", timeout=1)
#print ("{" + outp + "}")
#print tn.read_all()

#tn.write("games" + "\n\r")
#outp = tn.read_until ("fics%", timeout=1)
#print ("{" + outp + "}")
#print tn.read_all()
