#!/usr/bin/env python3

from machine import Pin, UART, PWM
import time
from micropython_dfplayer import DFPlayer
from time import sleep

# Pin setup
# pir_sensor = Pin(16, Pin.IN)         # PIR sensor connected to GPIO 16
# led = Pin(15, Pin.OUT)               # LED connected to GPIO 15
motor1a = Pin(14, Pin.OUT)             # Motor IN1 connected to GPIO 14
motor1b = Pin(13, Pin.OUT)             # Motor IN2 connected to GPIO 13
motor_pwm = PWM(Pin(12))               # PWM pin for speed control on GPIO 12
motor_pwm.freq(1000)                   # Set PWM frequency for motor
uart_id = 0                            # UART ID
uart = UART(uart_id, baudrate=9600, tx=Pin(0), rx=Pin(1))  # TX (Pin 0), RX (Pin 1)

# Create DFPlayer instance, using the UART ID, and pin IDs
music = DFPlayer(uart_id, tx_pin_id=0, rx_pin_id=1)

# Give dfplayer time to initialize
time.sleep(0.2) 

# Set volume
music.volume(10)

# Play a song
def play_song(folder, track):
    print(f"Playing track {track} from folder {folder}")
    music.play(folder, track)
    sleep(11)  # Play for 11 seconds


# Motor control functions
def spin_motor_forward():
    print("Spinning motor")
    for _ in range(5):  # Spin 5 times
        print("Spinning motor")
        start_motor()
        time.sleep(1)                    # Spin for 1 second
        stop_motor()                     # Stop the motor
        time.sleep(1)                    # Pause for 1 second

# Spin the motor forwards
def start_motor():
    motor1a.high()                       # Set direction to forward
    motor1b.low()
    motor_pwm.duty_u16(32768)            # Set motor to 50% duty cycle

# Stop the motor
def stop_motor():
    motor1a.low()
    motor1b.low()

# LED flash control
def flash_led():
    for _ in range(10):                  # Flash for 10 seconds (1 second interval)
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

# Main loop
while True:
#    if pir_sensor.value():              # Check if motion is detected
    if 2 > 1:                            # Currently set to execute continuously for testing
        stop_motor()
        print("Motion detected!")
#        flash_led()                     # Flash LED when motion is detected
        spin_motor_forward()             # Spin motor forward
        play_song(1,1)                   # Play track 1 from folder 1
        stop_motor()
        
    print("Sleeping for 15 seconds...")
    time.sleep(15)                      # Pause before checking for event again