from machine import Pin
import time

# Your actual GPIO pins (1–20, skipping 15, 17, 19)
button_pins = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 18, 22
]

# Create input pins with pull-up resistors
buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in button_pins]

# Track previous state to detect new presses
last_state = [1] * 16

print("Macropad firmware started")

while True:
    for i, b in enumerate(buttons):
        val = b.value()

        # Button pressed (active low)
        if val == 0 and last_state[i] == 1:
            print(f"KEY:{i+1}")

        last_state[i] = val

    time.sleep(0.01)