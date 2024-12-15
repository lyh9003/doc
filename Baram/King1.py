import time
import random
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from pynput import keyboard
from pynput.keyboard import Key  # 추가
import tkinter as tk
from tkinter import ttk
import threading

# Keyboard and mouse controllers
keyboard_controller = KeyboardController()
mouse = MouseController()

# Global variable to track if the macro is running
macro_running = False
hotkey_listener = None

def reset_hotkey_listener():
    global hotkey_listener
    if hotkey_listener:
        hotkey_listener.stop()
    hotkey_listener = keyboard.GlobalHotKeys({
        '<shift>+a': run_macro_thread,  # Start macro
        '<shift>+q': stop_macro         # Stop macro
    })
    hotkey_listener.start()

def run_macro():
    global macro_running
    macro_running = True
    try:
        total_iterations = int(iterations_var.get())

        for _ in range(total_iterations):
            if not macro_running:
                break

            # Macro sequence
            mouse.click(Button.left, 2)  # Mouse double click
            print("Mouse double-clicked")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press(' ')  # Spacebar
            keyboard_controller.release(' ')
            print("Space pressed")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press(' ')  # Spacebar
            keyboard_controller.release(' ')
            print("Space pressed")
            time.sleep(random.uniform(0.4, 0.5))

            keyboard_controller.press(Key.down)  # Down arrow
            keyboard_controller.release(Key.down)
            print("Down arrow pressed")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press(' ')  # Spacebar
            keyboard_controller.release(' ')
            print("Space pressed")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press(' ')  # Spacebar
            keyboard_controller.release(' ')
            print("Space pressed")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press(' ')  # Spacebar
            keyboard_controller.release(' ')
            print("Space pressed")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press('s')  # S key
            keyboard_controller.release('s')
            print("S key pressed")
            time.sleep(random.uniform(0.3, 0.4))

            keyboard_controller.press(Key.page_down)  # Page down
            keyboard_controller.release(Key.page_down)
            print("Page down pressed")
            time.sleep(random.uniform(0.1, 0.2))

            keyboard_controller.press(Key.page_down)  # Page down
            keyboard_controller.release(Key.page_down)
            print("Page down pressed")
            time.sleep(random.uniform(0.1, 0.2))

        print("Macro completed!")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    finally:
        macro_running = False
        reset_hotkey_listener()  # Reset hotkey listener
        print("Macro state reset.")

def run_macro_thread():
    if not macro_running:  # Prevent multiple macro instances
        print("Starting macro in a new thread...")
        threading.Thread(target=run_macro).start()
    else:
        print("Macro is already running!")

def stop_macro():
    global macro_running
    macro_running = False
    print("Macro stopped!")

def on_activate_start():
    run_macro_thread()

def on_activate_stop():
    stop_macro()

# Initialize hotkey listener
reset_hotkey_listener()

# Create the GUI window
root = tk.Tk()
root.title("Keyboard and Mouse Macro")

# UI Elements
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

iterations_label = ttk.Label(frame, text="Total Iterations:")
iterations_label.grid(row=0, column=0, sticky=tk.W)
iterations_var = tk.StringVar(value="1")
iterations_entry = ttk.Entry(frame, textvariable=iterations_var)
iterations_entry.grid(row=0, column=1)

start_button = ttk.Button(frame, text="Start Macro", command=run_macro_thread)
start_button.grid(row=1, column=0, columnspan=1, pady=10)

stop_button = ttk.Button(frame, text="Stop Macro", command=stop_macro)
stop_button.grid(row=1, column=1, columnspan=1, pady=10)

# Run the GUI event loop
root.mainloop()

# Stop the hotkey listener when the program exits
if hotkey_listener:
    hotkey_listener.stop()
