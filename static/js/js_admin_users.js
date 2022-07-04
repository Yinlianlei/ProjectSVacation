
function herfChange(){
//    var myurl=location.href;
//    myurl=myurl.split("/");
   window.location.href="../admin_doctors";
}

function herfChange1(){
//    var myurl=location.href;
//    myurl=myurl.split("/");
   window.location.href="../admin_feedback";
}

window.onload=function(){
        $.post('/get_userdata',function(ret){
            res=ret.split(",");


            var option11 = myChart1.getOption();
            option11.series[0].data = [{ value: res[0], name: '男' },{ value: res[1], name: '女' },];
            myChart1.setOption(option11);

            var yeardata1=[res[9], res[10], res[11], res[12], res[13], res[14], res[15]];
            var yeardata2=[res[2], res[3], res[4], res[5], res[6], res[7], res[8]];
            var option00 = myChart.getOption();
            option00.series[0].data = yeardata1;
            option00.series[1].data = yeardata2;
            myChart.setOption(option00);

            var option22 = myChart2.getOption();
            option22.series[0].data=[
               {name: '北京',value: res[16]}, {name: '天津',value: res[17]}, {name: '上海',value: res[18]}, {name: '重庆',value: res[19]},
               {name: '河北',value: res[20]}, {name: '河南',value: res[21]}, {name: '云南',value: res[22]},
               {name: '辽宁',value: res[23]}, {name: '黑龙江',value: res[24]}, {name: '湖南',value: res[25]},
               {name: '安徽',value: res[26]}, {name: '山东',value: res[27]},{name: '新疆',value: res[28]},
               {name: '江苏',value: res[29]}, {name: '浙江',value: res[30]}, {name: '江西',value: res[31]},
               {name: '湖北',value: res[32]}, {name: '广西',value: res[33]}, {name: '甘肃',value: res[34]},
               {name: '山西',value: res[35]}, {name: '内蒙古',value: res[36]}, {name: '陕西',value: res[37]},
               {name: '吉林',value: res[38]}, {name: '福建',value: res[39]}, {name: '贵州',value: res[40]},
               {name: '广东',value: res[41]}, {name: '青海',value: res[42]}, {name: '西藏',value: res[43]},
               {name: '四川',value: res[44]}, {name: '宁夏',value: res[45]}, {name: '海南',value: res[46]},
               {name: '台湾',value: res[47]}, {name: '香港',value: res[48]}, {name: '澳门',value: res[49]}
            ];
            myChart2.setOption(option22);


            option33 = myChart3.getOption();
            var arrdata = [];
            for ( var i = 50; i < res.length; i=i+2){
                arrdata.push({name: res[i],value:res[i+1]})
            }
            option33.series[0].data=arrdata;
//            option33.series[0].data=[
//                        {name: res[],value:res[]},{name: res[],value: res[]}, {name: res[],value: res[]},
//                        {name: res[],value: res[]}, {name: res[],value: res[]}, {name: res[],value: res[]},
//                        {name: res[],value: res[]}, {name: res[],value: res[]}, {name: res[],value: res[]},
//                        {name: res[],value: res[]}
//                        ];
            myChart3.setOption(option33);

//            option22.series[0].data = yeardata1;
//            if(ret==='wait'){
//            alert("请稍后重试");}
//            else if(ret==='already'){
//            alert("用户已存在"); }
//            else{
//            alert("前去登录")}
        });
}












//
//
//
//    // 基于准备好的dom，初始化echarts实例
//    var myChart = echarts.init(document.getElementById('p1'));
//
//    // 指定图表的配置项和数据
//    var option;
//
//    option = {
//     title: {
//       text: '男女年龄比例'
//     },
//     tooltip: {
//       trigger: 'axis',
//       axisPointer: {
//         type: 'shadow'
//       }
//     },
//     legend: {},
//     grid: {
//       left: '3%',
//       right: '4%',
//       bottom: '3%',
//       containLabel: true
//     },
//     xAxis: {
//       type: 'value',
//       boundaryGap: [0, 0.01]
//     },
//     yAxis: {
//       type: 'category',
//       data: ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60','>60']
//     },
//     series: [
//       {
//         name: '男',
//         type: 'bar',
//         data: [3, 14, 20, 35, 25, 10,5]
//       },
//       {
//         name: '女',
//         type: 'bar',
//         data: [2, 9, 25, 43, 22, 18,3]
//       }
//     ]
//    };
//    option && myChart.setOption(option);
//
//
//
//    // 基于准备好的dom，初始化echarts实例
//    var myChart2 = echarts.init(document.getElementById('p2'));
//
//    // 指定图表的配置项和数据
//    var option2;
//
//    option2 = {
//     title: {
//       text: '男女性别比例',
//       left: 'center'
//     },
//     tooltip: {
//       trigger: 'item'
//     },
//     legend: {
//       orient: 'vertical',
//       left: 'left'
//     },
//     series: [
//       {
//         name: 'Access From',
//         type: 'pie',
//         radius: '50%',
//         data: [
//           { value: 97, name: '男' },
//           { value: 76, name: '女' },
//
//         ],
//         emphasis: {
//           itemStyle: {
//             shadowBlur: 10,
//             shadowOffsetX: 0,
//             shadowColor: 'rgba(0, 0, 0, 0.5)'
//           }
//         }
//       }
//     ]
//    };
//    option2 && myChart2.setOption(option2);
//
//
//
//    // 基于准备好的dom，初始化echarts实例
//    var myChart3 = echarts.init(document.getElementById('p3'));
//
//    // 指定图表的配置项和数据
//    var option3;
//
//    option3 = {
//       title: {
//           text: '用户分布地图',
//           left: 'center'
//       },
//       tooltip: {
//           trigger: 'item'
//       },
//       legend: {
//           orient: 'vertical',
//           left: 'left',
//           data: ['中国疫情图']
//       },
//       visualMap: {
//           type: 'piecewise',
//           pieces: [
//               {min: 1000, max: 1000000, label: '大于等于1000人', color: '#372a28'},
//               {min: 500, max: 999, label: '500-999人', color: '#4e160f'},
//               {min: 100, max: 499, label: '100-499人', color: '#974236'},
//               {min: 10, max: 99, label: '10-99人', color: '#ee7263'},
//               {min: 1, max: 9, label: '1-9人', color: '#f5bba7'},
//           ],
//           color: ['#E0022B', '#E09107', '#A3E00B']
//       },
//       toolbox: {
//           show: true,
//           orient: 'vertical',
//           left: 'right',
//           top: 'center',
//           feature: {
//               mark: {show: true},
//               dataView: {show: true, readOnly: false},
//               restore: {show: true},
//               saveAsImage: {show: true}
//           }
//       },
//       roamController: {
//           show: true,
//           left: 'right',
//           mapTypeControl: {
//               'china': true
//           }
//       },
//       series: [
//           {
//               name: '人数',
//               type: 'map',
//               mapType: 'china',
//               roam: false,
//               label: {
//                   show: true,
//                   color: 'rgb(249, 249, 249)'
//               },
//               data: [
//                  {
//                     name: '北京',
//                     value: 212
//                   }, {
//                     name: '天津',
//                     value: 60
//                   }, {
//                     name: '上海',
//                     value: 208
//                   }, {
//                     name: '重庆',
//                     value: 337
//                   }, {
//                     name: '河北',
//                     value: 126
//                   }, {
//                     name: '河南',
//                     value: 675
//                   }, {
//                     name: '云南',
//                     value: 117
//                   }, {
//                     name: '辽宁',
//                     value: 74
//                   }, {
//                     name: '黑龙江',
//                     value: 155
//                   }, {
//                     name: '湖南',
//                     value: 593
//                   }, {
//                     name: '安徽',
//                     value: 480
//                   }, {
//                     name: '山东',
//                     value: 270
//                   }, {
//                     name: '新疆',
//                     value: 29
//                   }, {
//                     name: '江苏',
//                     value: 308
//                   }, {
//                     name: '浙江',
//                     value: 829
//                   }, {
//                     name: '江西',
//                     value: 476
//                   }, {
//                     name: '湖北',
//                     value: 13522
//                   }, {
//                     name: '广西',
//                     value: 139
//                   }, {
//                     name: '甘肃',
//                     value: 55
//                   }, {
//                     name: '山西',
//                     value: 74
//                   }, {
//                     name: '内蒙古',
//                     value: 34
//                   }, {
//                     name: '陕西',
//                     value: 142
//                   }, {
//                     name: '吉林',
//                     value: 42
//                   }, {
//                     name: '福建',
//                     value: 179
//                   }, {
//                     name: '贵州',
//                     value: 56
//                   }, {
//                     name: '广东',
//                     value: 797
//                   }, {
//                     name: '青海',
//                     value: 15
//                   }, {
//                     name: '西藏',
//                     value: 1
//                   }, {
//                     name: '四川',
//                     value: 282
//                   }, {
//                     name: '宁夏',
//                     value: 34
//                   }, {
//                     name: '海南',
//                     value: 79
//                   }, {
//                     name: '台湾',
//                     value: 10
//                   }, {name: '香港',value: 15}, {name: '澳门',value: 9}
//               ]
//           }
//       ]
//    };
//    option3 && myChart3.setOption(option3);

