from app import app
from flask import request, render_template
from os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTING_FILE'] = 'app/static/original'
app.config['GENERATED_FILE'] = 'app/static/generated'

@app.route("/",methods=["GET","POST"])
def index():

	if request.method == "GET":
		return render_template("index.html")

	if request.method == "Post":
		file_upload = request.files('file_upload')
		filename = file.file_upload.filename

		uploaded_image = Image.open(file_upload).resize((250,160))
		uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'],'Image.jpg'))
    
    original_image = Image.open(os.path.join(app.config['EXISTING_FILE'],'Image.jpg')).resize((250,160))
    original_image.save(os.path.join(app.config['EXISTING_FILE'],'Image.jpg'))

    original_grey = cv2.cvtColor(original_image,cv2.COLOR_BGR2GREY)
    uploaded_grey = cv2.cvtColor(uploaded_image,cv2.COLOR_BGR2GREY)

    (score,diff) = structural_similarity(original_grey,uploaded_grey,full = True)
    diff = (diff * 255).astype("uint8")

    thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
    	(x,y,w,h) = cv2.boundingRect(c)
    	cv2.rectangle(original_image, (x,y), (x,y,w,h), (0,0,255),2)
    	cv2.rectangle(uploaded_image, (x,y), (x,y,w,h), (0,0,255),2)

    	cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
    	cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
    	cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'),diff)
    	cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), thresh)
    	return render_template('index.html',pred = str(round(score*100,2)) + '%' + 'correct')


if __name__ = '__main__':
	app.run(debug = True)
	









