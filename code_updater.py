import subprocess
import time
ps = subprocess.Popen('ls | grep ref.willy',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]

if output == 'ref.willy\n':
	time.sleep(20)
	subprocess.call(['git','reset','--hard'])
	subprocess.call(['git','pull','origin','master'])
	subprocess.call(['python','robot/main.py'])
	subprocess.call(['rm','ref.willy'])
else:
	pass

print "finished"