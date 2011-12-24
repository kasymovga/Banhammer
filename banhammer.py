
import sys, os, cgi, cgitb
from banlist 		import *
from communicator 	import *
from util			import *

cgitb.enable()

form = dictform(cgi.FieldStorage())

try:
	action = form["action"]
except:
	action = "view"

banlist = NexuizBanList()
banlist.removeExpired()
com 	= Communicator(os.environ["REMOTE_ADDR"], sys.stdout, banlist)
com.handleAction(action, form)
