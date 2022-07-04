function herfChange(){
//    var myurl=location.href;
//    myurl=myurl.split("/");
   window.location.href="../admin_feedback";
}

function herfChange1(){
//    var myurl=location.href;
//    myurl=myurl.split("/");
   window.location.href="../admin_users";
}

function getdoctorinfo(id){
   $.post('/admin_doctors',data={'tt1':id},function(ret){

            alert(ret);

         });

}