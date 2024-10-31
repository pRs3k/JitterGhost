#!/usr/bin/env python3

from machine import Pin, UART, PWM
import uasyncio as asyncio  # Import uasyncio for concurrency
from micropython_dfplayer import DFPlayer
import time
import random

# Pin setup
pir_sensor = Pin(28, Pin.IN)                               # PIR sensor connected to GPIO 16
motor1a = Pin(14, Pin.OUT)                                 # Motor IN1 connected to GPIO 14
motor1b = Pin(15, Pin.OUT)                                 # Motor IN2 connected to GPIO 15
motor_pwm = PWM(Pin(12))                                   # PWM pin for speed control on GPIO 12
motor_pwm.freq(1000)                                       # Set PWM frequency for motor
uart_id = 0                                                # UART ID for DFPlayer Mini
uart = UART(uart_id, baudrate=9600, tx=Pin(0), rx=Pin(1))  # TX (Pin 0), RX (Pin 1) for DFPlayer Mini
red = Pin(22, Pin.OUT)                                     # Red channel connected to GPIO 22
green = Pin(21, Pin.OUT)                                   # Green channel connected to GPIO 21
blue = Pin(20, Pin.OUT)                                    # Blue channel connected to GPIO 20

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
            music.volume(10)  # Set a different volume for ambient sounds
            
            # Play track and wait for completion
            music.play(ambient_folder, track)
            await asyncio.sleep(1)  # Give some time for the track to start before waiting
            
            wait_time = random.randint(2, 5)  # Random wait time between 2 and 5 seconds
            print(f"Waiting for {wait_time} seconds before next track.")
            await asyncio.sleep(wait_time)  # Wait for the random time before the next track

        await asyncio.sleep(1)  # Small pause between cycles

# Play alert sequence
async def play_alert_sequence():
    global alert_track_index, ambient_playing
    print("Playing alert track 001")
    music.volume(10)  # Set a different volume for alert sounds
    music.play(alert_folder, 1)  # Play immediate alert sound 001.wav
    await asyncio.sleep(3)  # Wait 3 seconds for the alert sound to play

    # Play the next alert track in 002.wav to 004.wav sequence
    track = alert_tracks[alert_track_index]  # Get current track number (002, 003, or 004)
    print(f"Playing alert track {track:03}")  # Display in 3-digit format
    music.play(alert_folder, track)
    alert_track_index = (alert_track_index + 1) % len(alert_tracks)  # Move to the next track
    await asyncio.sleep(10)  # Wait while alert plays

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

# Set up the PWM for the green LED
pwm_green = PWM(green)
pwm_green.freq(1000)  # Set the frequency to 1kHz

# Function to fade in
async def fade_in(duration):
    for duty in range(0, 1024):  # PWM duty cycle range (0-1023)
        pwm_green.duty_u16(duty * 65535 // 1023)  # Scale to 16-bit
        await asyncio.sleep(duration / 1024)  # Use await for non-blocking sleep
    pwm_green.duty_u16(0)  # Ensure the LED is off after fading in

# Function to sputter effect
async def sputter(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        if random.random() > 0.5:  # 50% chance to turn on
            pwm_green.duty_u16(65535)  # Full brightness
        else:
            pwm_green.duty_u16(0)  # Turn off
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Non-blocking sleep with faster blinking

async def led_sequence(total_duration):
    fade_duration = total_duration / 2  # First half for fading in
    sputter_duration = total_duration / 2  # Second half for sputtering

    await fade_in(fade_duration)  # Fade in
    await sputter(sputter_duration)  # Sputter effect
    pwm_green.duty_u16(0)  # Ensure the LED is off after the sequence

# LED flash control
async def flash_led():
    flash_duration = 2  # Total duration of flash sequence (in seconds)
    flash_intervals = 10  # Number of flashes
    interval_duration = flash_duration / flash_intervals  # Calculate the duration of each flash

    for _ in range(flash_intervals):                  # Flash LED for the set intervals
        pwm_green.duty_u16(65535)        # Turn on green
        await asyncio.sleep(interval_duration / 2)  # Half the interval duration
        pwm_green.duty_u16(0)             # Turn off green
        await asyncio.sleep(interval_duration / 2)  # Half the interval duration


# Main function to handle motion detection and tasks
async def main_loop():
    global ambient_task
    ambient_task = asyncio.create_task(play_ambient_loop())  # Start ambient sound loop

    while True:
        if pir_sensor.value():  # Motion detected
            print("Motion detected!")
            ambient_task.cancel()  # Stop ambient playback during alert

            # Run motor and alert sound concurrently
            await asyncio.gather(spin_motor_forward(), play_alert_sequence(), flash_led(), led_sequence(3))

            print("Sleeping for 5 seconds...")
            await asyncio.sleep(5)  # Wait before checking for another motion event
            ambient_task = asyncio.create_task(play_ambient_loop())  # Start ambient sound loop
            await asyncio.sleep(1)  # Wait a moment to ensure ambient playback starts correctly
            print("Waiting for motion...")
        else:
            await asyncio.sleep(0.1)  # Short sleep for quicker PIR checks

# Run the main loop with uasyncio
try:
    asyncio.run(main_loop())
except KeyboardInterrupt:
    print("Program stopped manually")