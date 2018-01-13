var xmlhttp;
// decode_hex
function decode_hex(data)
{
    rets = ''
    for(i=0;i<data.length;i=i+4){
        s = data.substring(i, i+4)
        unicode_code = parseInt(s,16)
        rets +=String.fromCharCode(unicode_code)
        
    }
    return rets  
}

// find nearest time index        
function find_nearest_time(time_arry,time){
    var min = 0xffffffff;
    var min_i = 0;
    for (var i = 0; i < time_arry.length; i++) {
        if (Math.abs(time_arry[i] - time*1000) < min){
            min_i = i;
            min = Math.abs(time_arry[i] - time*1000);
        }    
    }
    return min_i;
}


// acculate_powercost        
function acculate_powercost(t1, t2, t_arr){
    var v = 0;
    for (var j=0; j < t_arr.length; j++) {
        var f3 = parseFloat(t_arr[j]['time']);
        if ((f3 >= t1) && (f3 <= t2)){
            var f4 = parseFloat(t_arr[j]['value'])
            v = v + f4;
        }
    }
    return v;
}

//-----------------------------------------
// read & process jpgs & jpgs2
//-----------------------------------------            
function show_unprocessed_jpgs_handle() {
    var status = xmlhttp.status;
    var resptxt = xmlhttp.responseText;
    var resp = JSON.parse(resptxt);
    if (resp["code"] == 0) {

        // 待处理表计图片
        var div_all = document.createElement('div');
        div_all.innerHTML='<h3>待处理表计图片</h3>';                
        document.body.appendChild(div_all);                    
        jpgs_array = resp['jpgs'];
        if (jpgs_array.length == 0){
                var div1 = document.createElement('div');
                div1.innerHTML='<br>无<br>';                
                document.body.appendChild(div1);   
            
        } else {
        
            for (var i = 0; i < jpgs_array.length; i++) {
                linkage = jpgs_array[i]['linkage']
                name = jpgs_array[i]['name']

                var div1 = document.createElement('div');
                div1.innerHTML='<br>' + name + '<br>';                
                document.body.appendChild(div1);   
            
                var img = document.createElement("img");
                img.src=linkage;
                img.setAttribute("id", name);                        
                document.body.appendChild(img);    
            }
        }
        
    }                                                                                                                                                                                                                                               
}
// read_jpgnames
function show_unprocessed_jpgs() {                                                                                                            
    var url = "/jpgnames";
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
            show_unprocessed_jpgs_handle();
        }
    }
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}            

function show_invalid_jpgs_handle() {
    var status = xmlhttp.status;
    var resptxt = xmlhttp.responseText;
    var resp = JSON.parse(resptxt);
    if (resp["code"] == 0) {
        // 处理异常的的表计图片
        var div_all = document.createElement('div');
        div_all.innerHTML='<h3>处理异常的的表计图片</h3>';                
        document.body.appendChild(div_all);                    
        jpgs_array = resp['jpgs2'];
        if (jpgs_array.length == 0){
                var div1 = document.createElement('div');
                div1.innerHTML='<br>无<br>';                
                document.body.appendChild(div1);   
            
        } else {
        
            for (var i = 0; i < jpgs_array.length; i++) {
                linkage = jpgs_array[i]['linkage']
                name = jpgs_array[i]['name']

                var div1 = document.createElement('div');
                div1.innerHTML='<br>' + name + '<br>';                
                document.body.appendChild(div1);   
            
                var img = document.createElement("img");
                img.src=linkage;
                img.setAttribute("id", name);                        
                document.body.appendChild(img);    
            }
        }
        
    }                                                                                                                                                                                                                                               
}
// read_jpgnames
function show_invalid_jpgs() {                                                                                                            
    var url = "/jpgnames";
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
            show_invalid_jpgs_handle();
        }
    }
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}


function show_jpgmasks_handle() {
    var status = xmlhttp.status;
    var resptxt = xmlhttp.responseText;
    var resp = JSON.parse(resptxt);
    if (resp["code"] == 0) {
        // 处理异常的的表计图片
        var div_all = document.createElement('div');
        div_all.innerHTML='<h3>图片配置信息</h3>';                
        document.body.appendChild(div_all); 



        var div1 = document.createElement('div');
        gray_limit = ['gray_limit']
        div1.innerHTML='<br>表计节点ID：' + resp['data']['k'];                
        document.body.appendChild(div1);   
        
        mask_cfg = JSON.parse(resp['data']['v'])
        
        var div1 = document.createElement('div');
        gray_limit = mask_cfg['gray_limit']
        div1.innerHTML='<br>灰度阈值：' + gray_limit;                
        document.body.appendChild(div1);
        
        var div1 = document.createElement('div');
        div1.innerHTML='<br>点值：';
        document.body.appendChild(div1);   
        document.body.appendChild(div1);   

        masks = mask_cfg['masks']
        for (var i = 0; i < masks.length; i++) {
            var div1 = document.createElement('div');
            div1.innerHTML='<br>' + masks[i];                
            document.body.appendChild(div1);
        
        }            
        
    }                                                                                                                                                                                                                                               
}
// show_jpgmasks
function show_jpgmasks() {                                                                                                            
    var url = "/jpgmasks";
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
            show_jpgmasks_handle();
        }
    }
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}
