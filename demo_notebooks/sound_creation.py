import numpy as np
from scipy.io.wavfile import write

# ===== Parameters =====
sample_rate = 44100
duration = 4.5
fade_time = 0.12

base_freqs = [220, 275, 293.3, 330, 366.7, 440, 495]   # airy, non-threatening range
pulse_rate = 2.6               # average pulses per second
jitter = 0.65                  # timing randomness
noise_level = 0.008

# ===== Time axis =====
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = np.zeros_like(t)

# ===== Generate pulses =====
current_time = 0.0
while current_time < duration:
    freq = np.random.choice(base_freqs)
    pulse_length = np.random.uniform(0.08, 0.16)
    start = int(current_time * sample_rate)
    end = int((current_time + pulse_length) * sample_rate)

    if end >= len(signal):
        break

    pulse_t = t[start:end] - t[start]
    envelope = np.sin(np.pi * pulse_t / pulse_length)  # smooth bell
    tone = np.sin(2 * np.pi * freq * pulse_t)

    signal[start:end] += tone * envelope * 0.6

    # irregular spacing between pulses
    current_time += (1 / pulse_rate) * np.random.uniform(1 - jitter, 1 + jitter)

# ===== Subtle air =====
noise = np.random.randn(len(t))
noise = np.convolve(noise, np.ones(300)/300, mode='same')
signal += noise * noise_level

# ===== Fade in / out =====
fade_samples = int(sample_rate * fade_time)
signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)

# ===== Normalize =====
signal /= np.max(np.abs(signal)) * 1.15

write("ai_thinking_v2.wav", sample_rate, signal.astype(np.float32))
print("Generated ai_thinking_v2.wav")
