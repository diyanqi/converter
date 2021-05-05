var data;
function uploadvideo() {
    var files = document.getElementById('mp4').files; //files是文件选择框选择的文件对象数组
    if(files.length == 0) return;
    var form = new FormData(),
        url = '/uploadvideo', //服务器上传地址
        file = files[0];
    form.append('file', file);
    var xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
document.getElementById("upb").innerHTML=`上传中……`;
document.getElementById("upb").disabled="disabled";
document.getElementById("mp4").disabled="disabled";
//上传进度事件
    xhr.upload.addEventListener("progress", function(result) {
        if (result.lengthComputable) {
            //上传进度
            var percent = (result.loaded / result.total * 100).toFixed(2);
            document.getElementById("upjindu").innerHTML=`
            <div class="mdui-progress">
                <div class="mdui-progress-determinate" style="width: `+String(percent)+`%;"></div>
            </div>
            `;
        }
    }, false);

    xhr.addEventListener("readystatechange", function() {
        var result = xhr;
        if (result.status != 200) { //error
            document.getElementById("upb").innerHTML=`上传失败`;
            console.log('上传失败', result.status, result.statusText, result.response);
        }
        else if (result.readyState == 4) { //finished
            document.getElementById("upb").innerHTML=`上传成功`;
            result=JSON.parse(result['responseText']);
            data=result;
            console.log('上传成功', result);
            document.getElementById("tijiao").removeAttribute("disabled");
            document.getElementById("tijiao").innerHTML="提交任务并转换！";
            document.getElementById("dbt").innerHTML=`<a download class="mdui-btn mdui-btn-raised mdui-ripple mdui-color-theme-accent" id="download" disabled>下载（请先转换）</a>`;
            mdui.mutation();
        }
    });
    xhr.send(form); //开始上传
}

document.getElementById("type_select").addEventListener("closed.mdui.select",function(){
    if(document.getElementById("type_select").value=="other"){
        document.getElementById("inputbox").innerHTML=`
            <div class="mdui-textfield mdui-textfield-floating-label">
            <label class="mdui-textfield-label">请输入 自定义格式的 后缀名……</label>
            <input class="mdui-textfield-input" type="text" id="othername"/>
            </div>`;
    }else{
        document.getElementById("inputbox").innerHTML='';
    }
});

function go(){
    var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
    httpRequest.open('POST', '/convert/cmd', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
    httpRequest.setRequestHeader("Content-type", "application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };
    var obj={};
    var tp=document.getElementById("type_select").value;
    if(tp=="other"){
            obj={
                "file_name":data['name'],
                "convert_type":document.getElementById("othername").value
            }
    }else{
        obj={
                "file_name":data['name'],
                "convert_type":tp
            }
    }
    document.getElementById("tijiao").innerHTML="转换中，请稍后……";
    document.getElementById("tijiao").setAttribute("disabled","disabled");
    document.getElementById("waitingconvert").innerHTML=`<div class="mdui-progress">
                                                        <div class="mdui-progress-indeterminate"></div>
                                                        </div>`;
    httpRequest.send(JSON.stringify(obj));//发送请求 将json写入send中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
    if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
        var json = JSON.parse(httpRequest.responseText);//获取到服务端返回的数据
        console.log(json);
        if(json['status']=='ok'){
            document.getElementById("tijiao").innerHTML="转换成功";
            document.getElementById("waitingconvert").innerHTML='';
            document.getElementById("download").removeAttribute("disabled");
            document.getElementById("download").innerHTML="下载！";
            document.getElementById("download").setAttribute("href","/download/"+json['filename']);
        }else{
            document.getElementById("tijiao").innerHTML="再次转换";
            document.getElementById("tijiao").removeAttribute("disabled");
            mdui.snackbar("转换失败，请重试！");
        }
    }
    };
}