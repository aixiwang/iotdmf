
function read_intc_code_1() {
    var url = '/dataprocess/load2';
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4) {
            read_intc_code_2();
        }
    }
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}

function read_intc_code_2() {
    var status = xmlhttp.status;
    var resptxt = xmlhttp.responseText;
    console.log('code: %o',resptxt);
    
    $("#editor").html(resptxt);
}

read_intc_code_1();

