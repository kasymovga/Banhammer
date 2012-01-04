
import datetime, re

MAX_TIME = 999999999 * 3600 * 24

QFONT_TABLE = [
    "\0", '#',  '#',  '#',  '#',  '.',  '#',  '#',
    '#',  '\t', '\n', '#',  ' ',  '\r', '.',  '.',
    '[',  ']',  '0',  '1',  '2',  '3',  '4',  '5',
    '6',  '7',  '8',  '9',  '.',  '<',  '=',  '>',
    ' ',  '!',  '"',  '#',  '$',  '%',  '&',  '\'',
    '(',  ')',  '*',  '+',  ',',  '-',  '.',  '/',
    '0',  '1',  '2',  '3',  '4',  '5',  '6',  '7',
    '8',  '9',  ':',  ';',  '<',  '=',  '>',  '?',
    '@',  'A',  'B',  'C',  'D',  'E',  'F',  'G',
    'H',  'I',  'J',  'K',  'L',  'M',  'N',  'O',
    'P',  'Q',  'R',  'S',  'T',  'U',  'V',  'W',
    'X',  'Y',  'Z',  '[',  '\\', ']',  '^',  '_',
    '`',  'a',  'b',  'c',  'd',  'e',  'f',  'g',
    'h',  'i',  'j',  'k',  'l',  'm',  'n',  'o',
    'p',  'q',  'r',  's',  't',  'u',  'v',  'w',
    'x',  'y',  'z',  '{',  '|',  '}',  '~',  '<',
    '<',  '=',  '>',  '#',  '#',  '.',  '#',  '#',
    '#',  '#',  ' ',  '#',  ' ',  '>',  '.',  '.',
    '[',  ']',  '0',  '1',  '2',  '3',  '4',  '5',
    '6',  '7',  '8',  '9',  '.',  '<',  '=',  '>',
    ' ',  '!',  '"',  '#',  '$',  '%',  '&',  '\'',
    '(',  ')',  '*',  '+',  ',',  '-',  '.',  '/',
    '0',  '1',  '2',  '3',  '4',  '5',  '6',  '7',
    '8',  '9',  ':',  ';',  '<',  '=',  '>',  '?',
    '@',  'A',  'B',  'C',  'D',  'E',  'F',  'G',
    'H',  'I',  'J',  'K',  'L',  'M',  'N',  'O',
    'P',  'Q',  'R',  'S',  'T',  'U',  'V',  'W',
    'X',  'Y',  'Z',  '[',  '\\', ']',  '^',  '_',
    '`',  'a',  'b',  'c',  'd',  'e',  'f',  'g',
    'h',  'i',  'j',  'k',  'l',  'm',  'n',  'o',
    'p',  'q',  'r',  's',  't',  'u',  'v',  'w',
    'x',  'y',  'z',  '{',  '|',  '}',  '~',  '<'
]

DPCOLOR_REGEXP = re.compile(r"(?:(\^\^)|\^x([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])|\^([0-9])|(.))(?=([0-9,]?))", re.S)

DPCOLOR_SIMPLE = {
	0:		"000",
	1:		"F00",
	2:		"0F0",
	3:		"FF0",
	4:		"00F",
	5:		"F0F",
	6:		"F0F",
	7:		"000", #"FFF",
	8:		"888",
	9:		"888"
}

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
	return str(datetime.timedelta(0, min(MAX_TIME, t)))

def qfont2ascii(s):
	s2 = str()
	
	for i in s:
		try:
			s2 += QFONT_TABLE[ord(i)]
		except:
			s2 += "<?>"
		
	return s2

def dp2html(s):
	s2 = str()
	colorstr = str()
	oldcolor = ""
    
	for i in DPCOLOR_REGEXP.findall(qfont2ascii(s)):
		escaped, red, green, blue, color, char, wtf = i
		
		if escaped:
			s2 += "^"
			continue
		
		elif color:
			colorstr = DPCOLOR_SIMPLE[int(color)]
		
		elif red:
			colorstr = ("%s%s%s" % (red, green, blue)).upper()
        
		if colorstr != oldcolor:
			if oldcolor != "":
				s2 += "</font>"
			s2 += "<font color=\"#%s\">" % colorstr
			
			oldcolor = colorstr
			
		s2 += char
		
	return s2 + ("</font>" if oldcolor != "" else "")
