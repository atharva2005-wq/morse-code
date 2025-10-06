import importlib
import subprocess
import sys

# --- Auto-install required modules ---
def install_if_missing(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"⚙️ Installing missing module: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["numpy", "matplotlib"]:
    install_if_missing(pkg)

# --- Imports after ensuring installation ---
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Morse Code Dictionary ---
MORSE_CODE = {
    'A': ".-", 'B': "-...", 'C': "-.-.", 'D': "-..", 'E': ".",
    'F': "..-.", 'G': "--.", 'H': "....", 'I': "..", 'J': ".---",
    'K': "-.-", 'L': ".-..", 'M': "--", 'N': "-.", 'O': "---",
    'P': ".--.", 'Q': "--.-", 'R': ".-.", 'S': "...", 'T': "-",
    'U': "..-", 'V': "...-", 'W': ".--", 'X': "-..-", 'Y': "-.--", 'Z': "--..",
    '1': ".----", '2': "..---", '3': "...--", '4': "....-", '5': ".....",
    '6': "-....", '7': "--...", '8': "---..", '9': "----.", '0': "-----"
}

# --- Signal Parameters ---
DOT_DURATION = 0.3
DASH_DURATION = 0.9
GAP_DURATION = 0.3
CARRIER_FREQ = 10
SAMPLE_RATE = 2000

# --- Conversion Functions ---
def text_to_morse(text):
    return ' '.join(MORSE_CODE.get(c.upper(), '') for c in text)

def morse_to_signal(morse):
    """Convert Morse code into binary ON/OFF signal"""
    signal = []
    for char in morse:
        if char == '.':
            signal += [1] * int(DOT_DURATION * SAMPLE_RATE)
            signal += [0] * int(GAP_DURATION * SAMPLE_RATE)
        elif char == '-':
            signal += [1] * int(DASH_DURATION * SAMPLE_RATE)
            signal += [0] * int(GAP_DURATION * SAMPLE_RATE)
        elif char == ' ':
            signal += [0] * int(GAP_DURATION * SAMPLE_RATE * 3)
    return np.array(signal)

def generate_ask(signal):
    """Generate ASK-modulated waveform"""
    t = np.linspace(0, len(signal) / SAMPLE_RATE, len(signal))
    carrier = np.sin(2 * np.pi * CARRIER_FREQ * t)
    ask_wave = carrier * signal
    return t, ask_wave

# --- GUI Setup ---
def create_gui():
    root = Tk()
    root.title("🔦 Morse Code ASK Simulator")
    root.geometry("900x650")
    root.configure(bg="#1e1b2e")

    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)

    # --- Title ---
    title = Label(root, text="Morse Code ASK Simulator", font=("Segoe UI", 22, "bold"),
                  fg="#60a5fa", bg="#1e1b2e")
    title.pack(pady=15)

    # --- Input Area ---
    frame = Frame(root, bg="#1e1b2e")
    frame.pack(pady=10)

    Label(frame, text="Enter Text:", font=("Segoe UI", 13), bg="#1e1b2e", fg="white").grid(row=0, column=0, padx=5)
    text_entry = Entry(frame, font=("Segoe UI", 13), width=25)
    text_entry.grid(row=0, column=1, padx=5)

    # --- Morse Output ---
    morse_label = Label(root, text="", font=("Consolas", 14, "bold"),
                        fg="#a5b4fc", bg="#1e1b2e")
    morse_label.pack(pady=10)

    # --- Canvas for Graph ---
    fig, ax = plt.subplots(figsize=(9, 3))
    fig.patch.set_facecolor("#1e1b2e")
    ax.set_facecolor("#0f172a")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=15)

    # --- ASK Plot Function ---
    def plot_ask():
        text = text_entry.get().strip()
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to transmit.")
            return

        morse = text_to_morse(text)
        morse_label.config(text=f"Morse Code: {morse}")

        signal = morse_to_signal(morse)
        t, ask_wave = generate_ask(signal)

        ax.clear()
        ax.plot(t, ask_wave, color='#00FFFF', linewidth=1.8, label='ASK Signal')
        ax.fill_between(t, ask_wave, color='#00ffff33')
        ax.set_title(f"ASK Waveform for '{text.upper()}'", color="#FFD700", fontsize=14, pad=10)
        ax.set_xlabel("Time (s)", color="#94A3B8")
        ax.set_ylabel("Amplitude", color="#94A3B8")
        ax.grid(True, color='#334155', linestyle='--', alpha=0.7)
        ax.tick_params(colors='white')
        ax.legend(facecolor='#1E293B', edgecolor='#38BDF8')

        canvas.draw()

    # --- Buttons ---
    btn_frame = Frame(root, bg="#1e1b2e")
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Generate Waveform", command=plot_ask).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Exit", command=root.destroy).grid(row=0, column=1, padx=10)

    # --- Footer ---
    Label(root, text="Made by Atharva, Durga, Eshika and Rajveer",
          bg="#1e1b2e", fg="#94a3b8", font=("Segoe UI", 10)).pack(side=BOTTOM, pady=10)

    root.mainloop()

# --- Run GUI ---
if __name__ == "__main__":
    create_gui()