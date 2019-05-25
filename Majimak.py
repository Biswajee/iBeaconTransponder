"""
Created on Tue May 14 01:17:17 2019

@author: Biswajit Roy
"""
import time
import requests
import json
import os
import subprocess
import threading
CONST_DEVICEID = <YOUR_DEVICE_ID>
flag = 0
error_string = {'status': 'unreachable'}
error_string = json.dumps(error_string) 
# Sends health message to server 
def sendHealth(deviceid, status, distance, gps="alpha release"):
    try:
        response = requests.get("https://us-central1-lastleafd.cloudfunctions.net/harvest?id={0}&status={1}".format(deviceid, status))
        response = response.json()
    except:
        response = json.loads(error_string)
    return(response)


def messageSIM():
    subprocess.call([
    "sudo","curl", "--interface", "usb0", "-X", "POST", "-H", 
    "X-Soracom-API-Key: <YOUR_API_KEY>", "-H",
    "X-Soracom-Token: <YOUR_API_TOKEN>",
    "-H", "Content-Type: application/json", "-d", '{ "body": "There is an emergency for device id: <YOUR_DEVICE_ID>" }', "https://g.api.soracom.io/v1/subscribers/<NOT_RANDOM>/send_sms"
    ])
    subprocess.call([
    "sudo","./go_lastleaf"
    ])
    return True
    

# Function that reads distance from the sensor
def read_distance():
    # Initialize the GPIO pins
    import RPi.GPIO as GPIO         # Import the Raspberry Pi GPIO library
    GPIO.setmode(GPIO.BCM)          # Use Broadcom GPIO pin numbering
    TRIG = 2                        # GPIO pin 02
    ECHO = 3                        # GPIO pin 03
    GPIO.setup(TRIG, GPIO.OUT)      # Set TRIG pin as output
    GPIO.setup(ECHO, GPIO.IN)       # Set ECHO pin as input
    GPIO.output(TRIG, GPIO.LOW)     # Initialize TRIG output as LOW

    # Send a HIGH signal to TRIG in order to trigger the sensor
    GPIO.output(TRIG, GPIO.HIGH)    # Send a HIGH pulse to TRIG
    time.sleep(0.00001)             # Wait 10 microseconds to trigger sensor
    GPIO.output(TRIG, GPIO.LOW)     # Set TRIG back to LOW

    # Once the sensor is triggered, it will send an ultrasonic pulse and set
    # the ECHO signal to HIGH. As soon as the receiver detects the original
    # ultrasonic pulse, the sensor will set ECHO back to LOW.

    # We need capture the duration between ECHO HIGH and LOW to measure how
    # long the ultrasonic pulse took on its round-trip.

    pulse_start = time.time()               # Record the pulse start time
    while GPIO.input(ECHO) != GPIO.HIGH:    # Continue updating the start time
        pulse_start = time.time()           # until ECHO HIGH is detected

    pulse_end = pulse_start                 # Record the pulse end time
    while time.time() < pulse_start + 0.1:  # Continue updating the end time
        if GPIO.input(ECHO) == GPIO.LOW:    # until ECHO LOW is detected
            pulse_end = time.time()
            break

    GPIO.cleanup()                  # Done with the GPIO, so let's clean it up

    # The difference (pulse_end - pulse_start) will tell us the duration that
    # the pulse travelled between the transmitter and receiver.
    pulse_duration = pulse_end - pulse_start

    # We know that sound moves through air at 343m/s or 34,300cm/s. We can now
    # use d=vÃ—t to calculate the distance. We need to divide by 2, since we only
    # want the one-way distance to the object, not the round-trip distance that
    # the pulse took.
    distance = 34300 * pulse_duration / 2

    # The sensor is not rated to measure distances over 4m (400cm), so if our
    # calculation results in a distance too large, let's ignore it.
    if distance <= 400:
        return distance
    else:
        return None
 

statusNow = "active"


if __name__ == '__main__':
    print ("Starting distance measurement! Press Ctrl+C to stop this script.")
    time.sleep(1)
    while True:
        
        # Track the current time so we can loop at regular intervals
        loop_start_time = time.time()

        # Read the distance and output the result
        distance = read_distance()
        if distance:
            try:
                if distance < 6:
                    statusNow = "Emergency"
                    if flag == 0:
                        thr = threading.Thread(target=messageSIM, args=(), kwargs={})
                        thr.start() # will run messageSIM()
                        os.environ['MSG_COORD_FLAG'] = '1'
                        flag = 1
                else:
                    statusNow = "active"
                resp =  sendHealth(CONST_DEVICEID, statusNow, distance)
                print (resp)
            except:
                print(thr.is_alive())
                print ("Exception occured !")
            finally:
                print ("Distance: %.1f cm" % (distance))

                # Find out how much time to wait until we should loop again, so that
                # each loop lasts 1 second
                time_to_wait = loop_start_time + 1 - time.time()
                if time_to_wait > 0:
                    time.sleep(time_to_wait)

