#!/usr/bin/env python3

import cv2
import subprocess
import os
from pathlib import Path
from datetime import datetime

DIR = os.path.dirname(os.path.realpath(__file__))

IMAGE_IN = os.path.join(DIR, 'picture.jpg')
IMAGE_OUT = os.path.join(DIR, f'bg_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.jpg')
NOTES = os.path.join(DIR, 'notes.txt')

OSA_SET_DESKTOP = f'tell application "System Events" to tell the first desktop to set picture to "{IMAGE_OUT}"'

def draw_text(img, text, pos=(50, 50),
        font=cv2.FONT_HERSHEY_DUPLEX, font_scale=2, font_thickness=2, font_color=(0, 0, 0),
        bg_color=(255, 255, 255), bg_padding=20):

    x, y = pos
    (_, line_h), _ = cv2.getTextSize('pP', font, font_scale, font_thickness)
    for line in text.split('\n'):
        if line != '':
            (line_w, _), _ = cv2.getTextSize(line, font, font_scale, font_thickness)
            rect = img.copy()
            cv2.rectangle(rect, (x, y),
                    (x + line_w + bg_padding * 2,
                     y + line_h + bg_padding * 2),
                    bg_color, -1)
            cv2.addWeighted(img, 0.5, rect, 0.5, 0, dst=img)
            cv2.putText(img, line,
                    (x + bg_padding,
                     y + bg_padding + line_h + font_scale - 1),
                    font, font_scale, font_color, font_thickness)
        y += bg_padding * 2 + line_h + 1

def set_desktop():
    subprocess.call(f'osascript -e \'{OSA_SET_DESKTOP}\'', shell=True)

def get_notes():
    Path(NOTES).touch()
    subprocess.call(['vim', NOTES])
    with open(NOTES) as note_file:
        notes = note_file.read()[:-1]
        return notes if notes != '\n' else ''

def clear_pictures():
    for pic in Path(DIR).glob('bg_*.jpg'):
        os.remove(pic)

if __name__ == '__main__':
    clear_pictures()
    image = cv2.imread(IMAGE_IN)
    notes = get_notes()
    draw_text(image, notes)
    cv2.imwrite(IMAGE_OUT, image)
    set_desktop()

