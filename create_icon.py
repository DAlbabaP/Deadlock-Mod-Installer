from PIL import Image, ImageDraw


size = (256, 256)
image = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)


circle_color = (0, 122, 204, 255) 
draw.ellipse([20, 20, 236, 236], fill=circle_color)


draw.rectangle([80, 60, 100, 196], fill='white')  
draw.arc([80, 60, 176, 196], 270, 90, fill='white', width=20)  


image.save('icon.ico', format='ICO')
