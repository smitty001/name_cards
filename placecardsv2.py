from typing import Counter
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# for 
import csv

# Import vertical text class
from rotatedtext import verticalText

width = 5
height = 3
font_size = 26
font = 'Ace'
card_spacing = 0
spacing = 12 # smaller is a bigger space when multi-line
adjuster = 1.55 # spacing for 180 rotations

# get arguments
if len(sys.argv) == 2:
    font_size = int(sys.argv[1])

# Read in the CSV
def get_file():
    names = []
    with open('names.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')
        for row in reader:
            names.append(row)
    if len(names) % 2 != 0:
        names.append([""])
    return names


def return_array(num, div):
    counter = 0
    div_list = []
    gap = num / div
    while len(div_list) < div:
        counter = counter + gap
        div_list.append(counter)
    return div_list

def setCan(canvas):
    canvas.setFont(font, font_size)
    canvas.setLineWidth(.02)


def generate_pdf(names):
    can = canvas.Canvas('TEST.pdf', bottomup = False)
    pdfmetrics.registerFont(TTFont('Ace', 'ace.ttf'))
    setCan(can)
    PAGE_WIDTH  = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

    width_array = return_array(PAGE_HEIGHT, width)
    #height_array = return_array(PAGE_WIDTH, height)
    height_array = [PAGE_WIDTH/4, 3 * (PAGE_WIDTH/4)]

    width_line = return_array(PAGE_HEIGHT, width*4)
    width_line = width_line[::2]
    height_line = return_array(PAGE_WIDTH, height*2)
    #height_line = height_line[::2]


    def drawLine(can):
        # Draw grid lines
        # center line
        can.line(PAGE_WIDTH/2, 0, PAGE_WIDTH/2, PAGE_HEIGHT)
        for lines_w in width_line:
            for lines_h in height_line:
                # horizontal lines
                can.line(0, lines_w - font_size/4, PAGE_WIDTH, lines_w - font_size/4)
                # vertical lines
                # can.line(lines_h, 0, lines_h, PAGE_HEIGHT)

    drawLine(can)

    x_counter = 0
    y_counter = 0

    # Print Content
    for text in names:
        if x_counter == width - 1:
            y_counter = y_counter + 1
            x_counter = 0
        if y_counter == height - 1:
            can.showPage()
            setCan(can)
            drawLine(can)
            y_counter = 0
        if can.stringWidth(text[0]) > PAGE_WIDTH/2 - 40:
            text_array = text[0].split(" ", 1)
            if can.stringWidth(text_array[1]) > PAGE_WIDTH/2 - 40:
                    can.setFont(font, font_size/1.2)

            can.drawString(height_array[y_counter] - can.stringWidth(text_array[0])/2, width_array[x_counter] - width_array[0]/spacing, text_array[0])
            can.drawString(height_array[y_counter] - can.stringWidth(text_array[1])/2, width_array[x_counter] + width_array[0]/spacing, text_array[1])
            can.saveState()
            can.rotate(180)
            can.drawString(-height_array[y_counter] - can.stringWidth(text_array[1])/2, -width_array[x_counter] + height_array[0]/adjuster + width_array[0]/spacing, text_array[1])
            can.drawString(-height_array[y_counter] - can.stringWidth(text_array[0])/2, -width_array[x_counter] + height_array[0]/adjuster - width_array[0]/spacing, text_array[0])
            can.restoreState()
            setCan(can)
        else:
            can.drawString(height_array[y_counter] - can.stringWidth(text[0])/2, width_array[x_counter], text[0])
            can.saveState()
            can.rotate(180)
            can.drawString(-height_array[y_counter] - can.stringWidth(text[0])/2, -width_array[x_counter] + height_array[0]/adjuster, text[0])
            can.restoreState()
        x_counter = x_counter + 1


    can.save()

def main():
    names = get_file()
    generate_pdf(names)

main()