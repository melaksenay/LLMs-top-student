import sounddevice as sd
import numpy as np
import io
import wave
import openai
import soundfile as sf
import os

openai.api_key = api key here
samplerate = 16000  # use 16kHz audio for best performance
batch_duration = 120  # 10 second recording time
transcription_file = 'transcription.txt'

# Function to record a batch of audio
def record_audio(duration, samplerate, device=None):
    try:
        if device is not None:
            print(f"Using device index: {device}")
        else:
            print("Using default input device.")
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate,
                            channels=1, dtype='float32', device=device)
        sd.wait()  # Wait until the recording is finished
        print("Recording finished.")
        return np.squeeze(audio_data)
    except Exception as e:
        print(f"An error occurred during recording: {e}")
        return None

# Function to save audio to a WAV format for API use
def save_audio_to_wav(audio_data, samplerate):
    if audio_data is None:
        raise ValueError("No audio data to save.")
    if not isinstance(audio_data, np.ndarray):
        raise TypeError("audio_data must be a NumPy array.")
    if audio_data.dtype != np.float32 and audio_data.dtype != np.float64:
        raise TypeError("audio_data must be of type float32 or float64.")
    
    # Normalize and convert to int16
    wav_data = (audio_data * 32767).astype(np.int16)
    
    # Create a BytesIO object and write the WAV data into it
    buffer = io.BytesIO()
    sf.write(buffer, wav_data, samplerate, format='WAV', subtype='PCM_16')
    buffer.seek(0)  # Reset buffer pointer to the beginning
    
    # Assign a name attribute to the BytesIO object
    buffer.name = 'audio.wav'
    
    return buffer

# Whisper API
def transcribe_audio(audio_file, response_format="text"):
    try:
        print("Transcribing audio...")
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format=response_format  #response format is text by default.
        )
        print("Transcription completed.")
        
        if response_format == "text":
            return transcription  # Directly return the string
        elif response_format in ["json", "verbose_json"]:
            return transcription.get('text', '')  #access the 'text' key
        else:
            print(f"Unsupported response format: {response_format}")
            return ""
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""

# Main function to record and transcribe audio
def main():
    # List available devices lol
    print("Listing available audio devices...")
    devices = sd.query_devices()
    valid_input_devices = []
    for idx, device in enumerate(devices):
        input_channels = device['max_input_channels']
        if input_channels > 0:
            print(f"{idx}: {device['name']} - {input_channels} input channels")
            valid_input_devices.append(idx)
    if not valid_input_devices:
        print("No input devices found. Please connect a microphone.")
        return

    # Prompt user to select input device
    device_index = input("Enter the device index to use for recording (or press Enter to use default): ")
    if device_index.strip() == "":
        input_device = None  # Use default
    else:
        try:
            input_device = int(device_index)
            if input_device not in valid_input_devices:
                print("Invalid device index selected.")
                return
        except ValueError:
            print("Invalid input. Exiting.")
            return

    #Record the audio!
    audio_batch = record_audio(batch_duration, samplerate, device=input_device)

    if audio_batch is None:
        print("Skipping transcription due to recording error.")
        return  # Exit the program

    # Save audio as WAV file in-memory :)
    try:
        audio_wav = save_audio_to_wav(audio_batch, samplerate)
    except ValueError as ve:
        print(f"Error saving audio: {ve}")
        return  # Exit the program
    except TypeError as te:
        print(f"Error saving audio: {te}")
        return  # Exit the program

    #Transcribe audio batch
    transcription_text = transcribe_audio(audio_wav, response_format="text")

    with open(transcription_file, 'a') as file:
        # Write the transcription to a file
        file.write(transcription_text)
    # resultss
    print(f"Transcription: {transcription_text}")

if __name__ == "__main__":
    main()