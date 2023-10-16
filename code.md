```py
from machine import I2C, Pin, PWM
from I2C_LCD import I2cLcd
from stepper import mystepmotor
from Servo_modified import Servo

import _thread as th
import time
import random


flipper_up_position = 0  # Angle for flipper up position
flipper_down_position = 40  # Angle for flipper down position

# Variables


button = Pin(14, Pin.IN, Pin.PULL_UP) # The button value is 1
big_score = Pin(40, Pin.IN, Pin.PULL_UP)
light_stuck = Pin(13, Pin.IN, Pin.PULL_UP)
light_end = Pin(12, Pin.IN, Pin.PULL_UP)

myStepMotor = mystepmotor(38, 37, 36, 35)

servo_left_button = Pin(15, Pin.IN, Pin.PULL_UP)
servo_left = Servo(pin=16)

servo_right_button = Pin(17, Pin.IN, Pin.PULL_UP)
servo_right = Servo(pin=18)

stepper_running = True


# Buzzer
passiveBuzzer = PWM(Pin(21))

passiveBuzzer.deinit()
passiveBuzzer.init()
passiveBuzzer.duty(0)

# Threads
def servo_flipper_left():
    while servo_flipper_left:
        global servo_left_button
        global servo_left_state_before


def servo_flipper_right():
    while servo_flipper_right:
        global servo_right_button
        global servo_right_state_before
        servo_right_state = servo_right_button.value()
        if servo_right_state_before == 1 and servo_right_state == 0:
            print("works")
            servo_left.move(45)
        servo_right.move(0)
        servo_right_state_before = servo_right_state

def stepper():
    while stepper_running:
        myStepMotor.moveAround(0,1,2000)

# Functions
def gameover(first_message, second_message):
    stepper_running = score_detect_running = servo_flipper_left = servo_flipper_right = scored_running = False
    lcd.move_to(0, 0)
    lcd.putstr(first_message)

    lcd.move_to(0, 1)
    lcd.putstr(second_message)
    for i in range(800, 100, -30):
        time.sleep_ms(100)
        passiveBuzzer.duty(100)
        passiveBuzzer.freq(i)
    passiveBuzzer.duty(0)
    time.sleep_ms(250)
    Switch = False


# Start Up
passiveBuzzer.duty(100)
passiveBuzzer.freq(900)
time.sleep_ms(100)
passiveBuzzer.duty(0)

score = 0
ball = 0

Switch = True
light_stuck_once = False
memory_activated = False

servo_left_state_before = 1
servo_right_state_before = 1

light_stuck_state_before = 1
light_end_state_before = 1

big_score_before = 1
button_state_before = 1


th.start_new_thread(stepper,())


i2c = I2C(scl=Pin(40), sda=Pin(41), freq=400000)
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    for device in devices:
        print("I2C addr: "+ hex(device))
        lcd = I2cLcd(i2c, device, 2, 16)


lcd.move_to(0, 0)
lcd.putstr("Pin the Alien")

lcd.move_to(0, 1)
lcd.putstr("Score:%d" %(score))



while True:
    while Switch == True:
    # Light reader
        light_stuck_state = light_stuck.value()
        if light_stuck_state_before == 1 and light_stuck_state == 0 and light_stuck_once == False:
            stepper_running = False
            print("Stepper Stopped")
            if memory_activated == True:
                gameover("Lost to wheel","of Doom")
                break
            else:
                if ball >= 1:
                    gameover("Lost to wheel","of Doom")
                    break
            memory_activated = True
            light_stuck_once = True
            light_stuck_before = light_stuck_state


        light_end_state = light_end.value()
        if light_end_state_before == 1 and light_end_state == 0:
            ball += 1
            if ball >= 2 and light_stuck_once == False:
                gameover("Gameover", "Get Better")
                break
            elif ball == 1 and light_stuck_once == True:
                stepper_running = True
                print('Stepper Motor Activated again')
                light_stuck_once = False
            else:
                if ball == 1 and light_stuck_once == False:
                    lcd.move_to(0, 1)
                    lcd.putstr("Insert 2nd ball")
            light_end_before = light_end_state



        servo_left_state = servo_left_button.value()
        if not servo_left_state and servo_left_state != servo_left_state_before:
            print("Servo Left Clicked")
            servo_left.move(0)
        elif servo_left_state and servo_left_state != servo_left_state_before:
            servo_left.move(100)
        servo_left_state_before = servo_left_state
        
        
        servo_right_state = servo_right_button.value()
        if not servo_right_state and servo_right_state != servo_right_state_before:
            print("Servo Right Clicked")
            servo_right.move(0)
        elif servo_right_state and servo_right_state != servo_right_state_before:
            servo_right.move(100)
        servo_right_state_before = servo_right_state
        
    # Score
        big_score_state = big_score.value()
        if big_score_before == 1 and big_score_state == 0:
            score += 5000
            lcd.move_to(0, 1)
            lcd.putstr("Score:%d" %(score))
            print(f"Big Score {score}")
        big_score_state_before = big_score_state

# NEEDS MOTAR BUTTON TO WORK NOW


        button_state = button.value()
        if button_state_before == 1 and button_state == 0:
            passiveBuzzer.duty(100)
            passiveBuzzer.freq(1300)
            score += 150
            lcd.move_to(0, 1)
            lcd.putstr("Score:%d" %(score))
            print(f"Score {score}")
            time.sleep_ms(10)
            passiveBuzzer.duty(0)

        button_state_before = button_state # uppfærum stöðuna fyrir næstu umferð


    while Switch == False:
        # Restart using
        servo_left_state = servo_left_button.value()
        servo_right_state = servo_right_button.value()
        if servo_left_state_before == 1 and servo_left_state == 0 and servo_right_state_before == 1 and servo_right_state == 0:
            stepper_running = True
            
            servo_left.move(0)
            score = 0
            ball = 0
            light_stuck_once = False
            
            lcd.move_to(0, 0)
            lcd.putstr("Pin the Alien")

            lcd.move_to(0, 1)
            lcd.putstr("Score:%d" %(score))
            
            passiveBuzzer.duty(100)
            passiveBuzzer.freq(900)
            time.sleep_ms(200)
            passiveBuzzer.duty(0)
            Switch = True
        servo_left_state_before = servo_left_state
        servo_right_state_before = servo_right_state
```
