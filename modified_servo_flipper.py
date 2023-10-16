
from modified_servo import Servo
import time
from machine import Pin, PWM

motor = Servo(pin=14)
takki = Pin(36, Pin.IN, Pin.PULL_UP)

flipper_up_position = 0  # Angle for flipper up position
flipper_down_position = 40  # Angle for flipper down position

button_prev_state = takki.value()
while True:
    button_current_state = takki.value()
    
    # Button is pressed and was not pressed in previous loop
    if not button_current_state and button_current_state != button_prev_state:
        motor.move(flipper_up_position)
        
    # Button is released and was pressed in previous loop
    elif button_current_state and button_current_state != button_prev_state:
        motor.move(flipper_down_position)
        
    button_prev_state = button_current_state
    time.sleep(0.05)  # Small delay for debouncing
