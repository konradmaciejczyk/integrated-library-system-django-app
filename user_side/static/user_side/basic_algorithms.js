function toggleDivs(a, b, time_interval){
    var opacity = 0;
    var intervalID = 0; 

    function fadeIn(){
        intervalID = setInterval(toggleDivs2, time_interval);                
    }
    function fadeOut(){
        intervalID = setInterval(toggleDivs1, time_interval);                
    }

    function toggleDivs1(){
        var div = document.getElementById(a);
        opacity = Number(window.getComputedStyle(div).getPropertyValue("opacity"));

        if(opacity > 0){
            opacity = opacity-0.1;
            div.style.opacity = opacity;
        }else{
            clearInterval(intervalID);
            div.style.display = "none";
            document.getElementById(b).style.opacity = 0;
            document.getElementById(b).style.display = "block";
            fadeIn();                        
        }
    }
    function toggleDivs2(){
        var div = document.getElementById(b);
        opacity = Number(window.getComputedStyle(div).getPropertyValue("opacity"));

        if(opacity < 1){
            opacity = opacity + 0.1;
            div.style.opacity = opacity;
        }else{
            clearInterval(intervalID);
        }
    }
    fadeOut();
}