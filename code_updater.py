import subprocess
import time
time.sleep(20)
subprocess.call(['git','reset','--hard'])
subprocess.call(['git','pull','origin','master'])
subprocess.call(['mkdir','tetadas'])
print "finished"