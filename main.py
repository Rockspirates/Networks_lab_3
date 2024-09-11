import sounddevice as sd
import numpy as np
from decoder import decode_audio_file, get_frequency
from generator import generate_cts
from helper import waittime
from sender import send_cts
from computer import computer
from message import message
import threading
import queue
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize a queue to store audio data
audio_queue = queue.Queue()
# Initialize a message queue, this stores all the messages I have to send
message_queue = queue.Queue()
# Initialize a start_time variable
start_time = time.time()
running_status = threading.Event()
# Set the event to indicate that the thread should run
running_status.set()  

#Initialize your computer with an instance of computer class
server = computer(1)
#Initialize an instance of message class
message_heard = message()

# Parameters for recording
sample_rate = 44100  # Sample rate for audio
block_size = 1024    # Block size for processing

# Frequency thresholds (can be adjusted)
start_frequency = 1000  # Frequency to start recording
stop_frequency = 1100   # Frequency to stop recording
tolerance = 50  # Frequency tolerance to account for noise

recording = False  # Flag to indicate whether recording is active
audio_data = []    # List to store the recorded audio data


def process(audio_file):
    """This function will be called after the audio stops recording."""
    global start_time

    print("Processing audio data...")
    # Example: saving the audio data to a file (optional)
    audio_file = np.concatenate(audio_file)  # Concatenate chunks into one array
    print(f"Audio data length: {len(audio_file)} samples")
    
    message_heard = decode_audio_file(audio_file) 

    print(message_heard)


def callback(indata, frames, time, status):
    """Callback function to process audio blocks and check frequency."""
    global recording, audio_data

    if status:
        print(status, file=sys.stderr)

    # Analyze the frequency content of the audio block
    frequency = get_frequency(indata[:, 0], sample_rate)

    if not recording and abs(frequency - start_frequency) <= tolerance:
        print(f"Detected start frequency {frequency:.1f} Hz. Starting recording.")
        recording = True
        audio_data = []  # Clear previous audio data before starting new recording

    if recording:
        # Append the current audio block to the audio_data list
        audio_data.append(indata.copy())

        # If stop frequency is detected, stop recording and call process
        if abs(frequency - stop_frequency) <= tolerance:
            print(f"Detected stop frequency {frequency:.1f} Hz. Stopping recording.")
            process(audio_data)
            recording = False


def listen():
    global running_status

    print("Listening for specific frequencies...")

    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, blocksize=block_size):
        while running_status.is_set():  
            if recording:
                print("Don't do anything")

            else:
                if message_heard.message_type == None:
                    pass
                else:
                    if message_heard.message_type == "RTS":
                        
                        # time.sleep(os.getenv("RTS_CTS"))
                        # if 

            # if server.state == "BASE":
            #     if len(message_queue) == 0:
            #         continue
            #     else:
            #         if time.time() - start_time >= server.get_time():
            #             pass



            # if start_time != -1:
            #     if time.time() - start_time >= server.get_time():
            #         start_time = server.timeout()
            # # Main loop: the callback handles everything in the background
            sd.sleep(100)  # Short sleep to prevent excessive CPU usage


def get_input():
    global running_status, start_time

    while running_status.is_set():
        user_input = input("Enter command (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            running_status.clear()
            print("Exiting...")
            break
        else:
            print(f"You entered: {user_input}")
            message_queue.put(user_input)
            start_time = time.time()


# Start the listening thread
listen_thread = threading.Thread(target=listen)  # Adjust the time as needed
listen_thread.start()

# Start the input thread
input_thread = threading.Thread(target=get_input)
input_thread.start()

# Wait for threads to complete
listen_thread.join()
input_thread.join()
