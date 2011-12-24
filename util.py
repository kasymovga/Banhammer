
import datetime

def first(seq):
	try:
		return seq[0]
	except IndexError:
		pass
		
def last(seq):
	try:
		return seq[-1]
	except IndexError:
		pass

def dictform(form):
	d = {}
	
	for k in form.keys():
		d[k] = form[k].value
	
	return d

def safecast(t, val, default):
	try:
		return t(val)
	except:
		return default
		

def timeformat(t):
	return str(datetime.timedelta(0, t))
