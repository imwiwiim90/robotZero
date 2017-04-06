cd /home/pi/Desktop/robotZero
ps auc | grep python | awk '{print $2}' | sudo xargs kill
git reset --hard
git pull origin master
sudo python robot/main.py
