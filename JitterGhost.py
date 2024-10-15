#!/usr/bin/env python3

from machine import Pin, UART, PWM
import time

# Pin setup
pir_sensor = Pin(16, Pin.IN)           # PIR sensor connected to GPIO 16
led = Pin(15, Pin.OUT)                 # LED connected to GPIO 15
motor_pwm = PWM(Pin(14))               # Motor connected to GPIO 14 (PWM)
motor_pwm.freq(1000)                   # Set PWM frequency for motor

# Setup UART for DFPlayer Mini
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # TX (Pin 0), RX (Pin 1)

# DFPlayer Mini commands
def play_song():
    uart.write(b'\x7E\xFF\x06\x03\x00\x00\x01\xFE\xF7\xEF')  # Play first song
    time.sleep(10)  # Play for 10 seconds
    uart.write(b'\x7E\xFF\x06\x16\x00\x00\x00\xFE\xE9\xEF')  # Stop playing

# Motor control
def spin_motor():
    motor_pwm.duty_u16(32768)  # Set motor to 50% duty cycle (adjust if needed)
    time.sleep(10)             # Spin for 10 seconds
    motor_pwm.duty_u16(0)      # Stop motor

# LED flash control
def flash_led():
    for _ in range(10):        # Flash for 10 seconds (1 second interval)
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

# Main loop
while True:
    if pir_sensor.value() == 1:    # Detect motion
        print("Motion detected!")
        play_song()                # Play song for 10 seconds
        spin_motor()               # Spin motor for 10 seconds
        flash_led()                # Flash LED for 10 seconds
        print("Pausing for 5 seconds...")
        time.sleep(15)              # Pause for 15 seconds before checking again
    time.sleep(0.1)                # Short delay before checking again