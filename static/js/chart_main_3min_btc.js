  
// start to create chart
require.config({
    paths: {
        echarts: './js'
    }
});
 
require(
    [
        'echarts',
        'echarts/chart/bar',
        'echarts/chart/line',
    ],

    function (ec) {
        var points_array = []
        var point_names = []
        var x_series = []
        var option_series = []
        var x_axis_linuxtime = []
        var x_axis = []  
    
        //--- 折柱 ---
        var myChart = ec.init(document.getElementById('main_3min'));

        var option = {
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data: point_names
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {show: true, type: ['line', 'bar']},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            xAxis : [
                {
                    type : 'category',
                    data : x_axis,                        
                }
            ],
            yAxis : [
                {
                    type : 'value',
                    splitArea : {show : true}
                }
            ],
            series : option_series
        };
        
        // generate x_axis string array
        var now = new Date();
        var len = 20*24;
        while (len--) {
            x_axis_linuxtime.unshift(now)
            x_axis.unshift(now.toLocaleDateString() + ' ' + now.toLocaleTimeString());
            now = new Date(now - 1000*180);
        }
     
        // insert data to chart from data web server GET data
        function read_temps() {
            var url = "/thermal";
            xmlhttp=new XMLHttpRequest();
            xmlhttp.onreadystatechange=function() {
                if (xmlhttp.readyState==4) {
                    proc_get_thermal_resp();
                }
            }
            xmlhttp.open("GET",url,true);
            xmlhttp.send();
        }
        // proc_get_thermal_resp
        function proc_get_thermal_resp() {
            var status = xmlhttp.status;
            var resptxt = xmlhttp.responseText;
            var resp = JSON.parse(resptxt);
            if (resp['code'] == 0) {
                t_arr = resp['data']
                
                // fill x_series[][]
                for (var i = 0; i < points_array.length; i++) {
                    x_series[i] = []
                }                  
                for (var i = 0; i < points_array.length; i++) {
                    for (var j = 0; j < t_arr.length; j++) {
                    if (t_arr[j]['id'] == points_array[i]['id']){
                        k = find_nearest_time(x_axis_linuxtime,t_arr[j]['time']);
                        v = t_arr[j]['value'];
                        x_series[i][k] = v;
                        
                    }                   
                  }  
                }  
                /*
                // fill undefined value with last defined value
                for (var i = 0; i < points_array.length; i++) {                    
                    for (var j = 1; j < x_series[i].length; j++) {
                        if (x_series[i][j] == undefined)
                            x_series[i][j] = x_series[j-1];
                    }        
                } */

                // create points_names from dynamic data structure
               for (var i = 0; i < points_array.length; i++) {
                    desp = decode_hex(points_array[i]['description'])
                    option_series[i] = {
                                    name:desp,
                                    type:'line',
                                    data:x_series[i],
                                    }
                } 

                
            }
            
            myChart.setOption(option);

        } 
        // read_points
        function read_points() {
            var url = "/view/datapoints/thermal";
            xmlhttp=new XMLHttpRequest();
            xmlhttp.onreadystatechange=function() {
                if (xmlhttp.readyState==4) {
                    proc_get_points_resp();
                }
            }
            xmlhttp.open("GET",url,true);
            xmlhttp.send();
        }
        // proc_get_points_resp
       function proc_get_points_resp() {
            var status = xmlhttp.status;
            var resptxt = xmlhttp.responseText;
            var resp = JSON.parse(resptxt);
            if (resp["code"] == 0) {  
                points_array = resp["data"];
                // create points_names from dynamic data structure
               for (var i = 0; i < points_array.length; i++) {
                        desp = decode_hex(points_array[i]['description'])
                        point_names[i] = desp
                } 
            // proc_get_points_resp                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                read_temps()
            }                                                                                                                                                                                                                                               
        }
        // read_points
        read_points();
        // 3min refresh screen
        // setInterval(read_points, 60*3); 
    }
);
