import subprocess
import time

subprocess.call(['git','reset','--hard'])
subprocess.call(['git','pull','origin','master'])
subprocess.call(['mkdir','tetadas'])
time.sleep(10)
print "finished"