import csv
import reportlab

from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.pdfbase.pdfmetrics import stringWidth, getFont
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm

# Import vertical text class
from rotatedtext import verticalText

# Fonts
_baseFontName  ='Times'
_baseFontNameB ='Times-Bold'
_baseFontNameI ='Times-Oblique'
_baseFontNameBI='Times-BoldOblique'

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


def generate_pdf(names):

	styles = getSampleStyleSheet()

	doc = SimpleDocTemplate("test.pdf")

	elements = []

	ttab_empty = ""
	table_data = []
	counter = 0
	while counter < len(names)-1:
		temp = []
		temp.append(verticalText(names[counter][0]))
		temp_counter = counter + 1
		temp.append(verticalText(names[temp_counter][0]))
		table_data.append(temp)

		temp = []
		temp.append(names[counter][0])
		temp_counter = counter + 1
		temp.append(names[temp_counter][0])
		table_data.append(temp)

		counter = counter + 2
	
	print(table_data)


	table_data.append([ttab_empty, ttab_empty]) #tab_empy are empty strings

	ts = [('ALIGN',(1,1),(100,100),'CENTER'),
		('VALIGN', (1,1), (100,100), 'MIDDLE'),
		#('GRID', (0,0), (100,100), 1, colors.black),
		('FONTSIZE', (1, 1), (100, 100), 18),
		('BOX', (1,1), (100, 100), .5, colors.grey)
		]

	table = Table(table_data, rowHeights=100, colWidths=250, style=ts)


	elements.append(table)

	doc.multiBuild(elements)

def main():
	names = get_file()
	pdf = generate_pdf(names)


main()