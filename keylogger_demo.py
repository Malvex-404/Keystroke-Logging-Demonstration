import tkinter as tk
from pynput import keyboard
from datetime import datetime
import os

# -------------------- Global Variables --------------------
listener = None
logging_active = False
keystrokes = []

# Create reports folder if not exists
if not os.path.exists("reports"):
    os.makedirs("reports")

# -------------------- Functions --------------------
def on_press(key):
    if logging_active:
        try:
            keystrokes.append(key.char)
        except AttributeError:
            keystrokes.append(f"[{key}]")

def start_logging():
    global listener, logging_active
    if not logging_active:
        logging_active = True
        status_label.config(text="Status: Logging Started", fg="green")
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

def stop_logging():
    global listener, logging_active
    if logging_active:
        logging_active = False
        if listener:
            listener.stop()
        status_label.config(text="Status: Logging Stopped", fg="red")
        generate_report()

def generate_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/keystroke_report_{timestamp}.txt"

    with open(filename, "w") as file:
        file.write("Keystroke Logging Demonstration Report\n")
        file.write("-----------------------------------\n")
        file.write(f"Date & Time: {datetime.now()}\n\n")
        file.write("Captured Keystrokes:\n")
        file.write("".join(keystrokes))

    keystrokes.clear()
    report_label.config(text=f"Report Generated: {filename}", fg="blue")

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("Keystroke Logging Demonstration")
root.geometry("450x300")
root.resizable(False, False)

title_label = tk.Label(root, text="Keystroke Logging Demo", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

status_label = tk.Label(root, text="Status: Idle", font=("Arial", 12), fg="black")
status_label.pack(pady=5)

start_button = tk.Button(root, text="Start Logging", width=20, bg="green", fg="white", command=start_logging)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Logging", width=20, bg="red", fg="white", command=stop_logging)
stop_button.pack(pady=10)

report_label = tk.Label(root, text="", font=("Arial", 9))
report_label.pack(pady=10)

disclaimer = tk.Label(
    root,
    text="Educational use only.\nUser consent required.",
    font=("Arial", 8),
    fg="gray"
)
disclaimer.pack(side="bottom", pady=5)

root.mainloop()
