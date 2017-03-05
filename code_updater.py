import subprocess
import time

subprocess.call(['git','reset','--hard'])
subprocess.call(['git','pull','origin','master'])
time.sleep(20)
print "finished"