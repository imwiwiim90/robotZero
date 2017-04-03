import subprocess
ps = subprocess.Popen("python tester.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
