from typing import Counter
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
font_size = 18
font = 'Ace'
card_spacing = 0
spacing = 19
adjuster = 2.1

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
    canvas.setLineWidth(.1)


def generate_pdf(names):
    can = canvas.Canvas('TEST.pdf', bottomup = False)
    pdfmetrics.registerFont(TTFont('Ace', 'ace.ttf'))
    setCan(can)
    PAGE_WIDTH  = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

    width_array = return_array(PAGE_HEIGHT, width)
    height_array = return_array(PAGE_WIDTH, height)

    width_line = return_array(PAGE_HEIGHT, width*4)
    width_line = width_line[::2]
    height_line = return_array(PAGE_WIDTH, height*2)
    height_line = height_line[::2]


    def drawLine(can):
        # Draw grid lines
        flipper = True
        for lines_w in width_line:
            for lines_h in height_line:
                can.line(0, lines_w - font_size/4, PAGE_WIDTH, lines_w - font_size/4)
                can.line(lines_h, 0, lines_h, PAGE_HEIGHT)

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
        if can.stringWidth(text[0]) > height_array[0] - 20:
            text_array = text[0].split(" ", 1)
            if can.stringWidth(text_array[1]) > height_array[0] - 20:
                    can.setFont(font, font_size/1.5)

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