import os

cmd=os.system

# 所有的 a b 均为路径（不是单单一个后缀名）
# 从a转换到b
# 所有a b路径务必带上引号，以防止路径中有特殊字符

def img2img(a,b):
    print("ffmpeg -i "+a+" "+b)
    if not cmd("ffmpeg -i "+a+" "+b)==0:
      raise TypeError('failed')

def img2video(a,b):
    if not cmd("ffmpeg -r 1/5 -pattern_type glob -i "+a+" "+b)==0:
      raise TypeError('failed')

def video2img(a,b):
    cmd("ffmpeg -r 10 -i "+a+" -f image2 "+b)

def video2video(a,b):
    cmd("ffmpeg -i "+a+" "+b)

def video2audio(a,b):
    cmd("ffmpeg -i "+a+" -vn -y -acodec copy "+b)

def audio2audio(a,b):
    cmd("ffmpeg -i "+a+" "+b)

def audio2video(a,b):
    cmd('''
    ffmpeg -i '''+a+''' -filter_complex \
"[0:a]showcqt,format=yuv420p[v]" \
-map "[v]" -map 0:a 
    '''+b)