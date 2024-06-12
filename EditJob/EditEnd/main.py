from flask import Flask, json, request, jsonify
from flask_cors import CORS
import pymysql
import cv2
import numpy as np
import os
import paddle
from paddleocr import PaddleOCR, draw_ocr


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

@app.route('/adduser', methods=['get', 'post'])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    return "已接收用户信息"

@app.route('/uploadimages', methods=['get', 'post'])
def uploadimages():
    username = request.form.get("username")
    img = request.files['file']
    picname=img.filename
    file = img.read()

    file = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)  # 解码为ndarray
    imgfile1_path = "./static/images/"+username+"/"

    if not os.path.exists(imgfile1_path):
        os.makedirs(imgfile1_path)
    img1_path = os.path.join(imgfile1_path, picname)
    cv2.imwrite(filename=img1_path, img=file)

    img_path=imgfile1_path+picname
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)
    url = "http://127.0.0.1:5000/static/images/"+username+"/" + picname
    print(url)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', charset='utf8')
    cursor = conn.cursor()
    conn.commit()
    cursor.execute('use editdata')
    sql = "INSERT INTO  `imgpath` (`username`,`url`,`picname`) VALUES('" + str(username) + "','" + str(url) + "','" + str(picname) + "');"
    ""
    print(sql)
    count = cursor.execute(sql)
    # print(count)
    conn.commit()
    cursor.close()
    conn.close()

    tempmap = {"url": url}
    return jsonify(tempmap)

    return "已接收用户图片信息"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
