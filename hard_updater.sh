cd /home/pi/Dekstop/robotZero
ps auc | grep python | awk '{print $2}' | sudo xargs kill
sleep 1
sudo python robot/main.py
