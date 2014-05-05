
from banlist import *
from time import strftime
from util import dp2html
import os

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
		
	def tableformat(self, n):
		c = "odd" if n % 2 else "even"
		
		return """
					<tr>
						<td class='%(c)s'>%%s</td>
						<td class='%(c)s'>%%s</td>
						<td class='%(c)s'>%%s</td>
						<td class='%(c)s'><b>%%s</b></td>
						<td class='%(c)s'>%%s</td>
						<td class='%(c)s'>%%s</td>
					</tr>""" % {"c" : c}
	
	def handle_view(self, params):
		self.sendHeader("text/html")
		
		self.out.write("""
<html>
	<head>
		<title>The Hall of Shame</title>
		<style type="text/css">
			%(css)s
		</style>
	</head>
	
	<body>
		<h1>The Hall of Shame</h1>
		<br/>
		
		<table>
			<tr>
				<th>Banned IP</th>
				<th>Server IP</th>
				<th>Server name</th>
				<th>Reason</th>
				<th>Time of ban</th>
				<th>Remaining time</th>
			</tr>
			
			%(entries)s
		</table>
		
		<br/>
		Powered by <a href="https://github.com/nexAkari/Banhammer">Banhammer</a>
		%(sig)s
	</body>
</html>


		""" % {
			"sig": os.environ["SERVER_SIGNATURE"],
			"entries": "\n".join(
				[
					self.tableformat(n) % (
						b.bannedIP,
						b.hostIP,
						b.hostName,
						dp2html(b.reason),
						strftime("%c", time.localtime(b.bannedAt)),
						timeformat(b.getRemainingBanTime())
					) for n, b in enumerate(self.banlist.bans[::-1])
				]
			),
			"css": """
			body {
				font-family: sans-serif;
				font-size: 75%;
				background: #EEEEEE;
				color: #000;
				margin: 10px;
			}

			h1 {
				margin: 0px;
				color: #800;
				text-align: center;
				margin-top: 1em;
			}
		
			a {
				color: #29579A;
				text-decoration: none;   
			}
			
			a:hover {
				color: #56729A;
				text-decoration: underline;
			}      
		
			table { 
				border-spacing: 0;
				width: 100%;
				border: 1px solid #333333;
				border-collapse: collapse;
			}
			
			th, td {
				text-align: center;
				padding-top: 0.2em;
				border: 1px solid #666666;
				padding-bottom: 0.2em;
			}
			
			.even {
				background-color: #AAAAAA;
			}
			
			.odd {
				background-color: #CCCCCC;
			}
			
			th {
				border-bottom: 2px solid #000000;
				color: #800;
				background-color: #CCCCCC;
			}
			"""
		})
