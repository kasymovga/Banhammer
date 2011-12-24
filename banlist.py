
import time
from util import *

class NexuizBan(object):
	def __init__(self, hostIP, hostName, bannedIP, bannedAt, unbanAt, reason):
		self.hostIP = hostIP
		self.hostName = hostName
		self.bannedIP = bannedIP
		self.bannedAt = bannedAt
		self.unbanAt = unbanAt
		self.reason = reason
		
	def isExpired(self):
		return time.time() >= self.unbanAt
	
	def getRemainingBanTime(self):
		return self.unbanAt - time.time()

class NexuizBanList(object):
	def __init__(self):
		self.bans = []
		self.load()
	
	def ban(self, hostIP, hostName, bannedIP, duration, reason):
		if self.findBan(hostIP, bannedIP) is not None:
			return
			
		self.bans.append(NexuizBan(hostIP, hostName, bannedIP, time.time(), time.time() + duration, reason))
		self.save()
	
	def unban(self, hostIP, bannedIP):
		self.bans.remove(self.findBan(hostIP, bannedIP))
		self.save()
		
	def findBan(self, hostIP, bannedIP):
		return first([ban for ban in self.bans if ban.hostIP == hostIP and ban.bannedIP == bannedIP])
	
	def removeExpired(self):
		map(self.bans.remove, [b for b in self.bans if b.isExpired()])
	
	def bansOf(self, *servers):
		return [ban for ban in self.bans if ban.hostIP in servers]
	
	def __iter__(self):
		return self.bans.__iter__()
	
	# Beauty ends here
	
	def _load(self):
		i = 0
		
		with open("bans.dat") as f:
			for line in [l[:-1] for l in f.readlines()]:
				if i == 0:
					hostIP 	 = line
					#print "ip", hostIP
				elif i == 1:
					hostName = line
					#print "name", hostName
				elif i == 2:
					bannedIP = line
					#print "banned", hostIP
				elif i == 3:
					bannedAt = line
					#print "at", bannedAt
				elif i == 4:
					unbanAt  = line
					#print "unban", unbanAt
				elif i == 5:
					reason 	 = line
					#print "reason", reason
				
				i += 1
				
				if i == 6:
					i = 0
					self.bans.append(NexuizBan(hostIP, hostName, bannedIP, safecast(float, bannedAt, 0), safecast(float, unbanAt, 60 ** 2), reason))
					#print "ban added"
		
		#print self.bans
		
	def load(self):
		try:
			return self._load()
		except:
			pass
	
	def save(self):
		with open("bans.dat", "w") as f:
			for ban in self:
				f.write("%s\n%s\n%s\n%d\n%d\n%s\n" % (
					ban.hostIP,
					ban.hostName,
					ban.bannedIP,
					ban.bannedAt,
					ban.unbanAt,
					ban.reason
				))
			
