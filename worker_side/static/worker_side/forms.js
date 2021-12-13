/* Konrad Maciejczyk, 2021-2020 */
class AddBook{
    constructor(optional_fields, ...ids){
       this.inputs = new Array;
       this.excluded_inputs  = new Array;
       this.inputs_states = new Array;

    //Gathering inputs and submit button(last element)
       ids.forEach(function(id){
           this.inputs.push(document.getElementById(id));
           this.inputs_states.push(false);
       }.bind(this));
       this.inputs_states.pop();
       const that = this;

    //Adding listeners to inputs and checking whether for is able to be submitted to server
       this.inputs.forEach(function(item){
           item.addEventListener('input', function(){
               that.inputs_states[that.inputs.indexOf(item)] = that.supervise_input(item);
               that.activate_deactivate_submit();
               console.log(that.inputs_states);
           })
        }) 

    //Gathering checkboxes, that exclude inputs       
       this.deactivate_checkboxes = optional_fields.map(function(item){
        document.getElementById(`no_${ids[item]}`).addEventListener('input', function(){
            that.deactivate_activate(that.inputs[item]);
            that.activate_deactivate_submit();
            console.log(that.inputs_states);
        });
       })
    }

    activate_deactivate_submit(){
        if(this.inputs_states.every(function(item){
            return item;
        })){
            this.activate(this.inputs.at(-1));
        }else{
            this.deactivate(this.inputs.at(-1));
        }
    }

    //Method, that disables input field when checkbox is checked
    deactivate(item){
        item.style.opacity = '.2'; item.style.pointerEvents = 'none';
    }

    //Method, that activates input field when checkbox is checked
    activate(item){
        item.style.opacity = '1'; item.style.pointerEvents = 'auto';
    }

    //Method, that activates or disables input field when checkbox is checked or not
    deactivate_activate(item){
        if(item.style.pointerEvents === "none"){
            this.activate(item);
            this.inputs_states[this.inputs.indexOf(item)] = false;
            let aux = this.excluded_inputs.indexOf(item);
            if(aux != -1)
                this.excluded_inputs.splice(aux, 1);
            
        }else{
            item.value = "";
            this.inputs_states[this.inputs.indexOf(item)] = true;
            this.deactivate(item);
            this.excluded_inputs.push(item);
        }     
    }

    //Auxilliary method, that evaluates whther value of given input is numeric or not
    check_if_numeric(item){
        if (isNaN(item.value) || item.value === ""){
            return false;
        }else{
            return true;
        }
    }

    supervise_input(item){
        switch(item.id){
            case 'isbn':{
                if(!this.excluded_inputs.includes(item))
                    return this.check_if_numeric(item);
                else
                    return true; 
            }case 'author':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'title': case 'full_title':{
                return item.value !== "";
            }case 'pub_year':{
                if(!this.excluded_inputs.includes(item))
                    return this.check_if_numeric(item); 
            }case 'pub':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'description':{
                return item.value !== "";
            }case 'condition':{
                return item.value === "1" || item.value === '2';
            }case 'status':{
                return item.value === "1" || item.value === '2';
            }case 'cover':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }
        }
    }
}

add_book_form_controler = new AddBook([0, 1, 4, 5, 9], 'isbn', 'author', 'title', 'full_title', 'pub_year', 'pub', 'description', 'condition', 'status', 'cover', 'submit');


        // function deactivate_input(id){
        //     let input = document.getElementById(id);
        //     if(input.style.pointerEvents === 'none'){
        //         input.style.opacity = '1'; input.style.pointerEvents = 'auto';
        //     }else{
        //         input.value = "";
        //         input.style.opacity = '.2'; input.style.pointerEvents = 'none';
        //     }
        // }
        
        // //----------ISBN Deactivation-----------//
        // const no_isbn = document.getElementById('no_isbn');
        // no_isbn.addEventListener('input', function(){
        //     let input = document.getElementById('isbn');
        //     deactivate_input('isbn');            
        // })

        // //----------Author Deactivation---------//
        // const no_author = document.getElementById('no_author');
        // no_author.addEventListener('input', function(){
        //     let input = document.getElementById('author');
        //     deactivate_input('author');            
        // })

        // //---------Publication year Deactivation-----------/
        // const no_pub_year = document.getElementById('no_pub_year');
        // no_pub_year.addEventListener('input', function(){
        //     let input = document.getElementById('pub_year');
        //     deactivate_input('pub_year');            
        // })

        // //---------Publisher Deactivation-----------/
        // const no_pub = document.getElementById('no_pub');
        // no_pub.addEventListener('input', function(){
        //     let input = document.getElementById('pub');
        //     deactivate_input('pub');            
        // })

        // //---------Cover Deactivation-----------/
        // const no_cover = document.getElementById('no_cover');
        // no_cover.addEventListener('input', function(){
        //     let input = document.getElementById('cover');
        //     deactivate_input('cover');            
        // })