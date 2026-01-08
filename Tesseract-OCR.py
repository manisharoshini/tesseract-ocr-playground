import os
import cv2
from PIL import Image
import pytesseract as pt

# --------------------------------------------------
# List all image files present in the test directory
# --------------------------------------------------

test_img_path = 'Code Practice/Test_Images'
create_path = lambda f : os.path.join(test_img_path, f)
test_image_files = os.listdir(test_img_path)

for f in test_image_files:
    print(f)
    
# --------------------------------------------------
# Display an image using OpenCV
# image_path : full path of the image
# size       : window size for display
# --------------------------------------------------
def show_image(image_path, size=(800, 600)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, size)
    
    cv2.imshow("IMAGE", image) # Display the image in a window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
# --------------------------------------------------
# Extract text from an image using PyTesseract
# --------------------------------------------------
image_path = test_image_files[4] # Change the index to test with different images
path = create_path(image_path)

image = Image.open(path)
text = pt.image_to_string(image)

print(text)
show_image(path)

# Note: You need to have the language data file for Hindi installed # --------------------------------------------------
# Extract text from an image by specifying language
# Note:
# Hindi language data (hin.traineddata) must be
# installed in Tesseract for this to work
# --------------------------------------------------.
path = create_path("hindi handwritting.jpg") # this image conatins an hindi text but we get output in english language ie it renderd it into english. 
image = Image.open(path)
text = pt.image_to_string(image, lang='hin') # specify the language code for Hindi

print(text)
show_image(path)

# -- Extract text from multiple images in a directory --
# Put all the file names or image name that we want to extract and render the file or loop through all the images

# --------------------------------------------------
# Extract text with timeout handling
# OCR process will terminate if it exceeds time limit
# --------------------------------------------------
path = create_path("Bill Image.png")

image = Image.open(path)
text = "NO TEXT TO BE APPREARED"
try:
    text = pt.image_to_string(image, lang = 'eng', timeout = 12)
except RuntimeError as e:
    print("Error: ", e)
    
print(text)
show_image(path)

# --------------------------------------------------
# Get bounding box coordinates for each character
# image_to_boxes returns coordinates for every letter
# --------------------------------------------------
path = create_path("testocr.png")
image = Image.open(path) # we have opened the image as pillow image
bound_reacts = pt.image_to_boxes(image, lang  = 'eng')

print(bound_reacts) # this prints the cordinates of each and every letter present in the image (x,y,width,height)
show_image(path)

# --------------------------------------------------
# Draw bounding boxes around detected characters
# --------------------------------------------------

image = cv2.imread(path) # here we are reading the image using cv2
h, _, _ = image.shape

for b in bound_reacts.splitlines():
    b = b.strip().split(' ') # this removes the outer spaces and splits the string into list based on spaces. 
    image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0),2)
    # int(b[1]) -> X cordinate of bottom left
    # h - int(b[2]) -> Y cordinate of bottom left
    # int(b[3]) -> X cordinate of top right
    # h - int(b[4]) -> Y cordinate of top right 
    # (0,255,0) -> color of rectangle (green)
    # 2 -> thickness of rectangle
    
cv2.imshow("IMAGE WITH BOUNDING BOXES", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# --------------------------------------------------
# Get detailed OCR data
# Includes text, confidence scores, line numbers,
# word numbers, and bounding box information
# --------------------------------------------------
image_path = test_image_files[2]
path = create_path(image_path)
image = Image.open(path)
text = pt.image_to_data(image, lang = 'eng')
print(text)
show_image(path)

# --------------------------------------------------
# Get orientation and script detection information
# Works best for images with sufficient text
# --------------------------------------------------
path = create_path(image_path)
image = Image.open(path)
osd = pt.image_to_osd(image)
print(osd)
# Page number: 0 --> indicates the page number
# Orientation in degrees: 270 or 180 --> The text in the image is detected as being rotated 270 degrees, so it is not upright.
# Rotate: 90 --> The OCR engine suggests rotating the image by 90 degrees clockwise to correct the text orientation.
# Orientation confidence: 250.00 --> The OCR engine is very confident that the orientation detection is correct.
# confidence score indicating how sure the OCR engine is about the detected orientation.
# Script: Latin -> Latin → English, French, Spanish, etc. Devanagari → Hindi, Arabic → Arabic, Cyrillic → Russian. The text uses the Latin script, which is common for English and many European languages.
# Script confidence: 2.00 --> This shows how confident the OCR engine is about the detected script.
# The OCR engine detected Latin script, but with low confidence, possibly due to: Blurry image, Small amount of text, Poor contrast Noise in the image

# --------------------------------------------------
# Convert image into different output formats
# PDF  : Searchable PDF
# HOCR : HTML-based OCR output
# XML  : ALTO XML structured format
# --------------------------------------------------
image_path = "testocr.png"
path = create_path(image_path)
file_save_path = "C:\\MANISHA\\Internship Documents"

pdf = pt.image_to_pdf_or_hocr(path, extension='pdf')
file = open(os.path.join(file_save_path, 'converted_image.pdf'), 'w+b')
file.write(pdf)
file.close()

# HOCR format - open standard for representing formatted text
hocr = pt.image_to_pdf_or_hocr(path, extension='hocr')
file = open(os.path.join(file_save_path, "hocr_image.html"), 'w+b') # w+b means write and read in binary mode
file.write(hocr)
file.close()

# XML format
xml = pt.image_to_alto_xml(path)
file = open(os.path.join(file_save_path, "xml_image.xml"), 'w+b')
file.write(xml)
file.close() # xml content corresponding to the image is saved in the specified file

# --------------------------------------------------
# Custom OCR configuration
# OEM : OCR Engine Mode
# PSM : Page Segmentation Mode
# --------------------------------------------------

image_path = "ocr-scanning-example-500px.jpg"
path = create_path(image_path)
custom_oem_config = r'--oem 3 --psm 9'
image = Image.open(path)
pt.image_to_string(image,config = custom_oem_config)

# -------------------- End of File --------------------

