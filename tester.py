import subprocess
import time
subprocess.call("cd /home/pi/Desktop/robotZero/",shell=True)
ps = subprocess.Popen("ps auc| grep python | wc -l ",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
n = int(ps.communicate(0)[0].strip())
if n > 1:
	ps = subprocess.Popen("ps auc| grep python | awk '{print $2}'| sort  | head -n" + str(n-1) + "| sudo xargs kill ",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print ps.communicate(0)
ps = subprocess.Popen("git reset --hard",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print ps.communicate(0)
ps = subprocess.Popen("git pull origin master",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print ps.communicate(0)[0]
f = open("error.txt","w")
subprocess.Popen("sudo python robot/main.py",shell=True,stderr=f)


#time.sleep(10)
#ps = subprocess.Popen("",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
