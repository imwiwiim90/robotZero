import subprocess
import time
ps = subprocess.Popen("ps | grep python | wc -l",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
n = int(ps.communicate(0)[0].strip())
ps = subprocess.Popen("ps | grep python | sort -k 1 -r| awk '{print $1}' | tail -n" + str(n-3) + "| xargs kill ",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
subprocess.Popen("git reset --hard",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
ps = subprocess.Popen("git pull origin master",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
subprocess.Popen("sudo python robot/main.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

print ps.communicate(0)

#time.sleep(10)
#ps = subprocess.Popen("",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
