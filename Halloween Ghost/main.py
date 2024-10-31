#!/usr/bin/env python3

from machine import Pin, UART, PWM
import time
from micropython_dfplayer import DFPlayer  # Import DFPlayer class
from time import sleep
import uasyncio as asyncio  # Import uasyncio for concurrency

# Pin setup
pir_sensor = Pin(28, Pin.IN)                               # PIR sensor connected to GPIO 16
# led = Pin(15, Pin.OUT)                                   # LED connected to GPIO 15
motor1a = Pin(14, Pin.OUT)                                 # Motor IN1 connected to GPIO 14
motor1b = Pin(13, Pin.OUT)                                 # Motor IN2 connected to GPIO 13
motor_pwm = PWM(Pin(12))                                   # PWM pin for speed control on GPIO 12
motor_pwm.freq(1000)                                       # Set PWM frequency for motor
uart_id = 0                                                # UART ID for DFPlayer Mini
uart = UART(uart_id, baudrate=9600, tx=Pin(0), rx=Pin(1))  # TX (Pin 0), RX (Pin 1) for DFPlayer Mini

# Create DFPlayer instance
music = DFPlayer(uart_id, tx_pin_id=0, rx_pin_id=1)

time.sleep(0.2)  # Give DFPlayer time to initialize

# Set volume
music.volume(10)

# Function to play songs
async def play_song(folder, track):
    print(f"Playing track {track} from folder {folder}")
    music.play(folder, track)
    await asyncio.sleep(11)  # Play for 11 seconds

# Motor control functions
async def spin_motor_forward():
    print("Spinning motor")
    for _ in range(5):  # Spin 5 times (10 seconds total)
        print("Spinning motor")
        start_motor()
        await asyncio.sleep(1)        # Spin for 1 second
        stop_motor()                  # Stop the motor
        await asyncio.sleep(1)        # Pause for 1 second

# Spin the motor forwards
def start_motor():
    motor1a.high()                     # Set direction to forward
    motor1b.low()
    motor_pwm.duty_u16(32768)          # Set motor to 50% duty cycle

# Stop the motor
def stop_motor():
    motor1a.low()
    motor1b.low()

# Main function to handle motion detection and tasks
async def main_loop():
    while True:
        if pir_sensor.value(): # Motion detected from PIR sensor
            stop_motor()
            print("Motion detected!")
            
            # Run motor and song concurrently
            await asyncio.gather(spin_motor_forward(), play_song(1, 1))
            stop_motor()
        
            print("Sleeping for 15 seconds...")
            await asyncio.sleep(15)  # Wait before checking for another motion event
            print("Waiting for motion...")

# Run the main loop with uasyncio
try:
    asyncio.run(main_loop())
except KeyboardInterrupt:
    print("Program stopped manually")
