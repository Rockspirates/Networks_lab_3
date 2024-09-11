import numpy as np

def decode_audio_file():
    pass

def get_frequency(data, sample_rate):
    """Get the dominant frequency of a block of audio data."""
    # Apply FFT to get frequency content
    fft_result = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1 / sample_rate)
    
    # Get the index of the peak in the FFT result (dominant frequency)
    peak_index = np.argmax(np.abs(fft_result))
    peak_frequency = freqs[peak_index]
    
    return peak_frequency