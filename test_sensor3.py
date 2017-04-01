import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
TRIG = 5
ECHO = 6
GPIO.setup(TRIG,GPIO.OUT)
# GPIO 23 set up as input. It is pulled up to stop false signals  
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.output(TRIG,0)
print "Make sure you have a button connected so that when pressed"  
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"  
raw_input("Press Enter when ready\n>")  
  
print "Waiting for falling edge on port 23"  
# now the program will do nothing until the signal on port 23   
# starts to fall towards zero. This is why we used the pullup  
# to keep the signal high and prevent a false interrupt  
GPIO.output(TRIG,1)
time.sleep(0.00001)
GPIO.output(TRIG,False)

try:  
    GPIO.wait_for_edge(ECHO, GPIO.FALLING)  
    print "\nFalling edge detected. Now your program can continue with"  
    print "whatever was waiting for a button press."  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
