
from banlist import *

def expectsParams(*required):
	def decorator(f):
		def decorated(self, params):
			for p in required:
				if not params.has_key(p):
					self.sendHeader("text/plain")
					self.out.write("Error: missing a required parameter: '%s'\n" % p)
					return
			return f(self, params)
		return decorated
	return decorator

class Communicator(object):
	def __init__(self, ip, output, banlist):
		self.out = output
		self.banlist = banlist
		self.ip = ip
	
	def handleAction(self, action, params):
		self.findActionHandler(action)(params)
		
	def findActionHandler(self, action):
		try:
			return getattr(self, "handle_" + action)
		except:
			return self.handleDefault
			
	def sendHeader(self, ctype):
		self.out.write("Content-type: %s\n\n" % ctype)
	
	def handleDefault(self, params):
		self.sendHeader("text/html")
		self.out.write("Nobody here but us chickens!")
	
	@expectsParams("servers")
	def handle_list(self, params):
		self.sendHeader("text/plain")
		servers = params["servers"].split(";")
		allsrvs = params["servers"] == "all"

		self.out.write(
			"\n".join(
				["%s\n%s\n%s\n%s" % (
					ban.bannedIP, ban.getRemainingBanTime(), ban.reason, ban.hostIP
				) for ban in self.banlist if allsrvs or ban.hostIP in servers]
			)
		)
	
	@expectsParams("hostname", "ip", "duration", "reason")
	def handle_ban(self, params):
		self.sendHeader("text/plain")
		self.banlist.ban(self.ip, params["hostname"], params["ip"], safecast(float, params["duration"], 60 ** 2), params["reason"])
		#self.handle_list({"servers": self.ip})
	
	@expectsParams("ip")
	def handle_unban(self, params):
		self.sendHeader("text/plain")
		self.banlist.unban(self.ip, params["ip"])
