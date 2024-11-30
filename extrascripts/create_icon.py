from PIL import Image, ImageDraw

# Set icon dimensions
size = (256, 256)
image = Image.new('RGBA', size, (0, 0, 0, 0))  # Create transparent background
draw = ImageDraw.Draw(image)

# Draw blue circle
circle_color = (0, 122, 204, 255)  # RGB + Alpha (Blue)
draw.ellipse([20, 20, 236, 236], fill=circle_color)

# Draw letter 'D' in white
draw.rectangle([80, 60, 100, 196], fill='white')  # Vertical line
draw.arc([80, 60, 176, 196], 270, 90, fill='white', width=20)  # Arc

# Save as ICO file
image.save('icon.ico', format='ICO')
