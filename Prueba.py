# import sys
from PIL import Image

images = map(Image.open, ['44903hd.jpg','painting.jpg','paris.jpg'])
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
	im = im.resize((200,200))
	new_im.paste(im, (x_offset,0))
	x_offset += im.size[0]

new_im.show()

new_im.save('test.jpg')