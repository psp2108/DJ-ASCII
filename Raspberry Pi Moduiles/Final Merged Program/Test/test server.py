from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return "This is homepage"

@app.route('/insertRecordedDetails/<weight>/<temp>')
def profile(weight, temp):
    return "Your weight is " + str(weight).replace("*",".") + " and temp is " + str(temp).replace("*",".")

@app.route('/uploader', methods = ['POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file received'

if __name__ == "__main__":
    app.run(debug=True)