/* Konrad Maciejczyk, 2021 - 2022 */
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

class CheckboxController{
    constructor(ids){
        this.ids = ids;
        this.items = undefined;
        this.items_amount = 0;
        this.is_all_selected = true;

        this.find_checkboxes();
        this.select_all();
    }

    find_checkboxes(){
        this.items = document.querySelectorAll('#item_type');
        this.items_amount = this.items.length;

        for(let i=0; i<this.items_amount - 1; i++){
            this.items[i].addEventListener('click', (item) => {
                this.update_checkbox();
            })
        }

        this.items[this.items_amount - 1].addEventListener('click', (item)=>{
            this.select_deselect();
        })
    }

    select_all(){
        this.items.forEach((item) =>{
            item.checked = true;
        })
    }

    deselect_all(){
        this.items[0].checked = true;

        for(let i = 1; i<this.items_amount; i++){
            this.items[i].checked = false;
        }
    }

    select_deselect(){
        if(this.is_all_selected){
            this.deselect_all();
            this.is_all_selected = !this.is_all_selected;
        }else{
            this.select_all();
            this.is_all_selected = !this.is_all_selected;
        }
    }

    update_checkbox(){
        let checked_counter = 0;

        for(var i=0; i<this.items_amount - 1; i++){
            if(this.items[i].checked === true ){
                checked_counter++;
            }
        }
        switch(checked_counter){
            case 3:{
                this.items[this.items_amount - 1].checked = true; break;
            }
            case 0:{
                this.items[0].checked = true; break;
            }
            default:{
                this.items[this.items_amount - 1].checked = false;
            }
            
        }
    }
}