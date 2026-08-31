#!/usr/bin/env python3.13
import itertools
import time
import tkinter as tk
import random
import sys

MINS = 60
try:
    minutes = int(sys.argv[1])
except Exception:
    minutes = 120

EXPIRES = time.time() + MINS * minutes
CANVAS_WIDTH = 120
CANVAS_HEIGHT = 60
CANVAS_CENTER_X = CANVAS_WIDTH // 2
CANVAS_CENTER_Y = CANVAS_HEIGHT // 2

root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-transparent", True)
root.config(bg='systemTransparent')

canvas = tk.Canvas(
    root,
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    bg='systemTransparent',
    bd=0,
    highlightthickness=0,
)
canvas.pack()

canvas_items = []
text_deltas = list(itertools.product((-1, 0, 1), (-1, 0, 1)))
text_deltas.remove((0, 0))

def create_text_items(color="white", outline="black", font=("Helvetica", 32, "bold")):
    global canvas_items
    for item in canvas_items:
        canvas.delete(item)
    canvas_items = []

    for dx, dy in text_deltas:
        canvas_items.append(canvas.create_text(
            CANVAS_CENTER_X + dx,
            CANVAS_CENTER_Y + dy,
            text="",
            fill=outline,
            font=font,
        ))

    # Create main text
    canvas_items.append(canvas.create_text(
        CANVAS_CENTER_X,
        CANVAS_CENTER_Y,
        text="",
        fill=color,
        font=font,
    ))

def time_format(seconds):
    mins, secs = divmod(abs(seconds), MINS)
    return f'{mins}:{secs:02d}'

def tick():
    remaining_seconds = round(EXPIRES - time.time())
    for item_id in canvas_items:
        canvas.itemconfig(item_id, text=time_format(remaining_seconds))

    if remaining_seconds < 0:
        canvas.configure(bg='red')
        root.config(bg='red')

    root.lift()
    root.wm_attributes("-topmost", True)
    canvas.after(random.randint(2_100, 4_200), tick)


root.update_idletasks()
x = root.winfo_screenwidth() - CANVAS_WIDTH - 40
y = root.winfo_screenheight() - CANVAS_HEIGHT - 20
root.geometry(f'{CANVAS_WIDTH}x{CANVAS_HEIGHT}+{x}+{y}')

create_text_items()
root.wm_attributes("-topmost", True)
tick()

try:
    root.mainloop()
except KeyboardInterrupt:
    pass
