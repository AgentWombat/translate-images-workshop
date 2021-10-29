from easyocr import Reader
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from deep_translator import GoogleTranslator
import numpy as np

l_source = input("Input the language code of the language from which you want to translate:\n>> ")

# Get text reader
r = Reader([l_source])

# Get translator
t = GoogleTranslator(source=l_source, target='en')

while True:

	file_name = input("What is the name of the image you want to scan and translate?\n>> ")

	# See if input file name is valid; if not, reprompt user.
	try:

		path = "./images/"+file_name
		img = Image.open(path)

	except Exception as e:
		print(e)
		continue

	# Convert image to format readable by EasyOCR
	np_img = np.asarray(img)

	# Analize image
	readings = r.readtext(np_img)


	# Mark up image with translations of text therewithin.
	draw = ImageDraw.Draw(img)

	for reading in readings:


		text = reading[1]

		# Deep translate throws an error if the input contains only integers. This resolves the problem.
		if text.isdigit():
			translated_text = text
		else:
			translated_text = t.translate(text)

		# Get top left and bottom right coordinates of current text box.
		x1,y1  = reading[0][0]
		x2, y2 = reading[0][2]

		font_size = int(0.4*(y2 - y1))

		# Print out translations
		print(text, ": TRANSLATED :", translated_text)


		# Superimpose translations upon image
		font = ImageFont.truetype("fonts/arial.ttf", font_size)
		draw.rectangle(((x1,y1),(x2,y2)), fill=(0,0,0))
		draw.text((x1,y1), translated_text, (255,255,255), font = font)


	new_np_img = np.asarray(img)

	plt.imshow(new_np_img)
	plt.show()



