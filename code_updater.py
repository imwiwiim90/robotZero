import subprocess

subprocess.call(['git','reset','--hard'])
subprocess.call(['git','pull','origin','master'])
print "finished"