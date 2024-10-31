#!/usr/bin/env python3

from machine import Pin, UART, PWM
import uasyncio as asyncio  # Import uasyncio for concurrency
from micropython_dfplayer import DFPlayer
import time
import random

# Pin setup
pir_sensor = Pin(28, Pin.IN)                               # PIR sensor connected to GPIO 16
motor1a = Pin(14, Pin.OUT)                                 # Motor IN1 connected to GPIO 14
motor1b = Pin(13, Pin.OUT)                                 # Motor IN2 connected to GPIO 13
motor_pwm = PWM(Pin(12))                                   # PWM pin for speed control on GPIO 12
motor_pwm.freq(1000)                                       # Set PWM frequency for motor
uart_id = 0                                                # UART ID for DFPlayer Mini
uart = UART(uart_id, baudrate=9600, tx=Pin(0), rx=Pin(1))  # TX (Pin 0), RX (Pin 1) for DFPlayer Mini

# Create DFPlayer instance
music = DFPlayer(uart_id, tx_pin_id=0, rx_pin_id=1)
time.sleep(0.2)  # Give DFPlayer time to initialize

# Global variables for sound tracks and motion control
ambient_folder = 1
ambient_tracks = list(range(1, 10))       # Files 001.wav to 009.wav
alert_folder = 2
alert_tracks = [2, 3, 4]                  # Files 002.wav to 004.wav
alert_track_index = 0                     # Track index for cycling alert sounds
ambient_playing = True                    # Flag to manage ambient playback
ambient_task = None                       # Task variable to control ambient playback

# Play ambient sounds in a loop with random wait times
async def play_ambient_loop():
    global ambient_playing
    while True:
        for track in ambient_tracks:
            if not ambient_playing:  # Stop ambient loop if motion is detected
                break
            print(f"Playing ambient track {track} from folder {ambient_folder}")
            music.volume(20)  # Set a different volume for ambient sounds
            music.play(ambient_folder, track)
            
            wait_time = random.randint(2, 5)  # Random wait time between 2 and 10 seconds
            print(f"Waiting for {wait_time} seconds before next track.")
            await asyncio.sleep(wait_time)  # Wait for the random time before the next track
            
        await asyncio.sleep(1)  # Small pause between cycles

# Play alert sequence
async def play_alert_sequence():
    global alert_track_index, ambient_playing
    ambient_playing = False                # Stop ambient playback
    print("Playing alert track 001")
    music.volume(20)  # Set a different volume for alert sounds
    music.play(alert_folder, 1)            # Play immediate alert sound 001.wav
    await asyncio.sleep(3)                 # Wait 2 seconds

    # Play the next alert track in 002.wav to 004.wav sequence
    track = alert_tracks[alert_track_index]  # Get current track number (002, 003, or 004)
    print(f"Playing alert track {track:03}") # Display in 3-digit format
    music.play(alert_folder, track)
    alert_track_index = (alert_track_index + 1) % len(alert_tracks)  # Move to the next track, looping back to 002
    await asyncio.sleep(10)                # Wait while alert plays

    ambient_playing = True                 # Resume ambient playback

# Motor control functions
async def spin_motor_forward():
    await asyncio.sleep(3)
    print("Spinning motor")
    for _ in range(1):                    # Spin 1 time (3 seconds total)
        start_motor()
        await asyncio.sleep(3)            # Spin for 1 second
        stop_motor()                      # Stop the motor
        await asyncio.sleep(1)            # Pause for 1 second

# Spin the motor forwards
def start_motor():
    motor1a.high()                         # Set direction to forward
    motor1b.low()
    motor_pwm.duty_u16(32768)              # Set motor to 50% duty cycle

# Stop the motor
def stop_motor():
    motor1a.low()
    motor1b.low()

# Main function to handle motion detection and tasks
async def main_loop():
    global ambient_task
    ambient_task = asyncio.create_task(play_ambient_loop())  # Start ambient sound loop

    while True:
        if pir_sensor.value():             # Motion detected
            stop_motor()
            print("Motion detected!")
            ambient_playing = False        # Stop ambient playback during alert

            # Run motor and alert sound concurrently
            await asyncio.gather(spin_motor_forward(), play_alert_sequence())
            stop_motor()

            print("Sleeping for 5 seconds...")
            await asyncio.sleep(5)        # Wait before checking for another motion event
            print("Waiting for motion...")
        else:
            # Ensure ambient playback is active if no motion is detected
            ambient_playing = True
            await asyncio.sleep(1)

# Run the main loop with uasyncio
try:
    asyncio.run(main_loop())
except KeyboardInterrupt:
    print("Program stopped manually")
