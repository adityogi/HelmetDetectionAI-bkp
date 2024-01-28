# from distutils.log import debug
from fileinput import filename
from flask import *
import os
from helmet_detection import check_if_helmet

app = Flask(__name__)

@app.route('/')
def main():
	return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
	# if request.method == 'POST':
	# folder_path = ".media"
	try:
		f = request.files['file']
		file_name = os.path.join("img", f.filename)
		img_file_name = os.path.join("static", "Image", f.filename)
		f.save(img_file_name)
		(helmet_detected, img_scene, labels) = check_if_helmet(img_file_name)
        #     print("Helmet detected in", img_file_name)
        #     display_helmet_in_a_box(labels, img_scene)
		if helmet_detected:
			return render_template("image.html", image = img_file_name, file_name = f.filename, detected = "detected ")
		else:
			return render_template("image.html", image = img_file_name, file_name = f.filename, detected = 'not detected')

	except Exception as e:
		return render_template("error.html", name = f.filename, error = e)


if __name__ == '__main__':
	app.run(debug=True)
