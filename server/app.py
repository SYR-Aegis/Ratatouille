import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#파일 확장자 검사
def allowed_file(filename):
    ext = os.path.splitext(filename)[-1].lower()
    if ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

#url 요청 
@app.route('/GetRecipe', methods=['GET','POST'])
def GetRecipe():
    #http 통신이후 request 값 초기
    response = {}
    #method 검사
    if request.method == 'POST':
        # check if the post request has the file part
        #파일 필드 검사
        if 'file' not in request.files:
            response["success"] = False
            response["msg"] = "no part file"
            return str(response)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        #파일 이름 검사
        if file.filename == '':
            response["success"] = False
            response["msg"] = "no selected file"
            return str(response)

        #파일 실체 및 확장자 검사 여기서 통과되면 API script실행
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #일단 저장
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            response["success"] = True
            #추후 msg에 레시피 링크 넘김
            response["msg"] = "success"
            return str(response)
        else:
            response["success"] = False
            response["msg"] = "invalid externsion."
            return str(response)
    else:
        response["success"] = False
        response["msg"] = "using POST method"
        return str(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
