scor=0
function scoreFun(object, opts) {
    var defaults = {
        fen_d: 16,
        ScoreGrade: 10,
        types: ["非常不满意", "相当不满意", "很不满意", "不满意", "普通", "一般", "还不错", "满意", "很满意", "相当满意", "非常满意"],
        nameScore: "fenshu",
        parent: "star_score",
        attitude: "attitude"
    };
    options = $.extend({},
    defaults, opts);
    var countScore = object.find("." + options.nameScore);
    var startParent = object.find("." + options.parent);
    var atti = object.find("." + options.attitude);
    var now_cli;
    var fen_cli;
    var atu;
    var fen_d = options.fen_d;
    var len = options.ScoreGrade;
    startParent.width(fen_d * len);
    var preA = (5 / len);
    for (var i = 0; i < len; i++) {
        var newSpan = $("<a href='javascript:void(0)'></a>");
        newSpan.css({
            "left": 0,
            "width": fen_d * (i + 1),
            "z-index": len - i
        });
        newSpan.appendTo(startParent)
    }
    startParent.find("a").each(function(index, element) {
        $(this).click(function() {
            now_cli = index;
            show(index, $(this))
        });
        $(this).mouseenter(function() {
            show(index, $(this))
        });
        $(this).mouseleave(function() {
            if (now_cli >= 0) {
                scor = preA * (parseInt(now_cli) + 1);

                startParent.find("a").removeClass("clibg");
                startParent.find("a").eq(now_cli).addClass("clibg");
                var ww = fen_d * (parseInt(now_cli) + 1);
                startParent.find("a").eq(now_cli).css({
                    "width": ww,
                    "left": "0"
                });
                if (countScore) {
                    countScore.text(scor)
                }
            } else {
                startParent.find("a").removeClass("clibg");
                if (countScore) {
                    countScore.text("")
                }
            }
        })
    });
    function show(num, obj) {
        var n = parseInt(num) + 1;
        var lefta = num * fen_d;
        var ww = fen_d * n;
        var scor = preA * n;
        atu = options.types[parseInt(num)];
        object.find("a").removeClass("clibg");
        obj.addClass("clibg");
        obj.css({
            "width": ww,
            "left": "0"
        });
        countScore.text(scor);
        atti.text(atu);
    }

};

$(function() {
       $("#fankuibt").on('click',function(){
//          var form1 = $("#comment_score1").val();
          var form1 = scor;
          if (scor===0){
            alert("请评分");
             return false
            }
//          alert(form1);
          var form2 = $("#comment_content").val();
//          alert(form2);
          $.post('/user_comment/0',data={'tt1':form1,'tt2':form2},function(ret){

            if(ret==='well'){
              alert("评价成功");}
            else{
              alert("请稍后重试"); }

          })
       });
});