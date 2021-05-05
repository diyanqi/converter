from flask import *
import os
import json
import time
import lib
from flask_apscheduler import APScheduler # 引入APScheduler
#Toby打个卡（az
app = Flask(__name__, static_folder="static", template_folder='templates')


#服务器会多一个static目录，下面放的文件直接 地址/static/文件名
#Toby:我吃饭去了ok
def touch(path):
    with open(path, 'w+'):
        os.utime(path, None)


root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")

'download系列'
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory("./complete/",filename)

'convert系列'
@app.route('/convert/audio2video',methods=['POST'])
def convert_audio2video():
    data=request.json
    fn=data['file_name']
    try:
        lib.audio2video('\"upload/'+fn+"\"",'\"complete/'+fn[:fn.rfind('.')]+"."+data['convert_type']+"\"")
    except:
        return json.dumps({"status":"failed"})
    return json.dumps({"status":"ok","filename":fn[:fn.rfind('.')]+"."+data['convert_type']})

@app.route('/convert/video2audio',methods=['POST'])
def convert_video2audio():
    data=request.json
    fn=data['file_name']
    try:
        lib.video2audio('\"upload/'+fn+"\"",'\"complete/'+fn[:fn.rfind('.')]+"."+data['convert_type']+"\"")
    except:
        return json.dumps({"status":"failed"})
    return json.dumps({"status":"ok","filename":fn[:fn.rfind('.')]+"."+data['convert_type']})

@app.route('/convert/audio2audio',methods=['POST'])
def convert_audio2audio():
    data=request.json
    fn=data['file_name']
    try:
        lib.audio2audio('\"upload/'+fn+"\"",'\"complete/'+fn[:fn.rfind('.')]+"."+data['convert_type']+"\"")
    except:
        return json.dumps({"status":"failed"})
    return json.dumps({"status":"ok","filename":fn[:fn.rfind('.')]+"."+data['convert_type']})

@app.route('/convert/video2video',methods=['POST'])
def convert_video2video():
    data=request.json
    fn=data['file_name']
    try:
        lib.video2video('\"upload/'+fn+"\"",'\"complete/'+fn[:fn.rfind('.')]+"."+data['convert_type']+"\"")
    except:
        return json.dumps({"status":"failed"})
    return json.dumps({"status":"ok","filename":fn[:fn.rfind('.')]+"."+data['convert_type']})

@app.route('/convert/img2video',methods=['POST'])
def convert_img2video():
    data=request.json
    fn=data['file_name']
    try:
        lib.img2video('\"upload/'+fn+"\"",'\"complete/'+fn[:fn.rfind('.')]+"."+data['convert_type']+"\"")
    except:
        return json.dumps({"status":"failed"})
    return json.dumps({"status":"ok","filename":fn[:fn.rfind('.')]+"."+data['convert_type']})

@app.route('/convert/img2img',methods=['POST'])
def convert_img2img():
    data=request.json
    fn=data['file_name']
    try:
        lib.img2img('\"upload/'+fn+"\"",'\"complete/'+fn[:fn.rfind('.')]+"."+data['convert_type']+"\"")
    except:
        return json.dumps({"status":"failed"})
    return json.dumps({"status":"ok","filename":fn[:fn.rfind('.')]+"."+data['convert_type']})

'upload系列'
@app.route('/uploadvideo', methods=['post'])
def upload_video():
    upload_path = './upload'
    file = request.files['file']
    if not file:
        return {"status": "fail"}
    filename = file.filename
    extension = filename.split('.')[-1]
    print(filename)
    touch(os.path.join(upload_path, filename))
    file.save(os.path.join(upload_path, filename))
    result = {"status": 200, "type": extension, "name": filename}
    return result

'pages系列'
@app.route('/video2audio', methods=['POST', 'GET'])
def video2audio():
    with open('templates/video2audio.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "视频转音频")

@app.route('/gif', methods=['POST', 'GET'])
def gif():
    with open('templates/gif.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "GIF编辑")

@app.route('/custom', methods=['POST', 'GET'])
def custom():
    with open('templates/custom.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "自定义命令行")

@app.route('/video2video', methods=['POST', 'GET'])
def video2video():
    with open('templates/video2video.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "视频格式互转")

@app.route('/img2video', methods=['POST', 'GET'])
def img2video():
    with open('templates/img2video.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "图片转视频")

@app.route('/img2img', methods=['POST', 'GET'])
def img2img():
    with open('templates/img2img.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "图片格式互转")

@app.route('/audio2audio', methods=['POST', 'GET'])
def audio2audio():
    with open('templates/audio2audio.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "音频格式互转")

@app.route('/audio2video', methods=['POST', 'GET'])
def audio2video():
    with open('templates/audio2video.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "音频转视频")

@app.route('/dlg', methods=['POST', 'GET'])
def dlg():
    with open('templates/dlg.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "赞助&说明")

@app.route('/', methods=['POST', 'GET'])
def home():
    with open('templates/home.htm') as fp:
        a = fp.read()
    return render_template("框架.htm").replace('<!-- { content } -->', a).replace('<!-- {page_name} -->', "首页")


#html的这样传 js?
#原理：从templates目录下找到index.htm渲染
#路径：服务器地址/static/index.js
#自动分配的，我开了静态目录
#不需要route了，内部代码定义，访问使用/static/index.js

if __name__ == '__main__':
    app.run(port=8080, debug=True, host="0.0.0.0")
