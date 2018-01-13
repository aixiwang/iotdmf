function dispTime(){
	var now = new Date();
	var time = now.getFullYear() + "/" + f2(now.getMonth()+1) + "/" + f2(now.getDate()) + " " + f2(now.getHours()) + ":" + f2(now.getMinutes());
	//element = document.getElementById("clock");
	//if (element != null){
		//element.childNodes[0].nodeValue = time;
	//} else{
	   $('#clock').html(time);
	//}
}

function f2(x){
	return (x < 10) ? '0' + x : x;
}
