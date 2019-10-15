
def objToFile(obj,filename):
	def write(string):
		for char in string:
			f.write(chr(ord(char)+1))
	f = open(filename,'w')
	for i in dir(obj):
		eval_obj_i = eval('obj.%s'%(i))
		t = type(eval_obj_i).__name__
		if t in ['int','float','tuple','list','bool']:
			write('obj.%s = %s'%(i,eval_obj_i))
		elif t == 'str':
			write('obj.%s = "%s"'%(i,eval_obj_i))
		else:
			continue
		write('\n')
	f.close()

def fileToObj(obj,filename):
	f = open(filename,'r')
	fcont = ''
	while True:
		data = f.read(1)
		if data=='':break
		fcont += chr(ord(data)-1)
	f.close()
	varuables = {'obj':obj}
	exec(fcont,varuables)
	return varuables['obj']

def getchange(x,y,x2,y2):
	x=x2-x
	y=y2-y
	avg=(abs(x)+abs(y))
	if avg==0:
		return 0,0
	return x/avg,y/avg