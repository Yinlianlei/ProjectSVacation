function listenForTAIText(){
    console.log("add listen");
    var text = document.getElementById("text_response");
    text.addEventListener("input",function(){
        text.style.height = 300;
    });
}