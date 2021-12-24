/* Konrad Maciejczyk, 2021-2022 */
class AddItem{
    constructor(optional_fields, copy_author_to_full_title, copy_title_to_full_title, ...ids){
       this.inputs = new Array;
       this.excluded_inputs  = new Array;
       this.inputs_states = new Array;
       this.copy_checkboxes = new Array;

       const that = this;

    //Gathering inputs and submit button(last element)
       ids.forEach(function(id){
           this.inputs.push(document.getElementById(id));
           this.inputs_states.push(false);
       }.bind(this));
       this.inputs_states.pop();

    //If copy_author checkbox is included in form add event listener in order to repeat/erase values to/from full_title
       if(copy_author_to_full_title){
        let author_index = ids.indexOf('author');
        let full_title_index = ids.indexOf('full_title');
           this.copy_checkboxes.push(document.getElementById('copy_author'));
           this.copy_checkboxes[0].addEventListener('input', function(){
               if(this.checked){
                    that.repeat_values(that.inputs[author_index], that.inputs[full_title_index]);
                    that.inputs_states[full_title_index] = that.supervise_input(that.inputs[full_title_index]);
                    that.approve_input(full_title_index);
               }
               else{
                    that.erase_values(that.inputs[author_index], that.inputs[full_title_index]);
                    that.inputs_states[full_title_index] = that.supervise_input(that.inputs[full_title_index]);
                    that.approve_input(full_title_index);
                }
           })
       }
    
    //If copy_title checkbox is included in form add event listener in order to repeat/erase values to/from full_title
       if(copy_title_to_full_title){
        let title_index = ids.indexOf('title');
        let full_title_index = ids.indexOf('full_title');
        this.copy_checkboxes.push(document.getElementById('copy_title'));
        this.copy_checkboxes[1].addEventListener('input', function(){
            if(this.checked){
                 that.repeat_values(that.inputs[title_index], that.inputs[full_title_index]);
                 that.inputs_states[full_title_index] = that.supervise_input(that.inputs[full_title_index]);
                 that.approve_input(full_title_index);
            }
            else{
                 that.erase_values(that.inputs[title_index], that.inputs[full_title_index]);
                 that.inputs_states[full_title_index] = that.supervise_input(that.inputs[full_title_index]);
                 that.approve_input(full_title_index);
             }
        })
    } 

    //Adding listeners to inputs and checking whether for is able to be submitted to server
       this.inputs.forEach(function(item){
           item.addEventListener('input', function(){
               let aux = that.inputs.indexOf(item);
               that.inputs_states[aux] = that.supervise_input(item);
               that.approve_input(aux);

               that.activate_deactivate_submit();
           })
        }) 

    //Gathering checkboxes, that exclude inputs       
       this.deactivate_checkboxes = optional_fields.map(function(item){
        document.getElementById(`no_${ids[item]}`).addEventListener('input', function(){
            that.deactivate_activate(that.inputs[item]);
            that.activate_deactivate_submit();
            that.approve_input(item);
        });
       })
    }

    //An method that activates submit button if every value in inputs are correct
    activate_deactivate_submit(){
        if(this.inputs_states.every(function(item){
            return item;
        })){
            this.activate(this.inputs.at(-1));
        }else{
            this.deactivate(this.inputs.at(-1));
        }
    }

     //An method that fires when checkboxes 'copy_author' or/and 'copy_title' is unchecked. Erase values of author or title from full_title input field.
    erase_values(from, input){
        if(from.id === 'author'){
            input.value = input.value.replace(from.value + ' - ', '');
        }else if(from.id === 'title'){
            input.value = input.value.replace(from.value, '');
        }
    }

    //An method that fires when checkboxes 'copy_author' or/and 'copy_title' is checked. Copy values from author or title input field to full_title input field.
    repeat_values(from, to){
        if(from.id === 'author'){
            to.value = from.value + ' - ' + to.value;
        }else if(from.id === 'title'){
            to.value = to.value + from.value;
        }
    }

    //An auxiliary method that paints inputs basing on input's value correctness.
    approve_input(input_index){
        if(this.inputs_states[input_index]){
            this.inputs[input_index].style.borderBottom = '2px solid green';
        }
        else{
            this.inputs[input_index].style.borderBottom = '2px solid red';
        }
    }

    //A method, that disables input field when checkbox is checked.
    deactivate(item){
        item.style.opacity = '.2'; item.style.pointerEvents = 'none';
    }

    //A method, that activates input field when checkbox is checked
    activate(item){
        item.style.opacity = '1'; item.style.pointerEvents = 'auto';
    }

    //A method, that activates or disables input field when checkbox is checked or not.
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

    //Auxilliary method, that evaluates whether value of given input is numeric or not.
    check_if_numeric(item, starts_with_0){
            const regex_with_0 = new RegExp('[0-9]+');
            const regex_without_0 = new RegExp('^[1-9][0-9]+');
            return starts_with_0 ? regex_with_0.test(item.value) : regex_without_0.test(item.value);
    }

    //A method that checks for correctness of user inputs. It needs to be implemented in child classes.
    supervise_input(item){
        throw new Error("Method supervise_input needs to be implemented!")
    }
}

class AddBook extends AddItem{

    constructor(optional_fields, copy_author_to_full_title, copy_title_to_full_title, fetch_button_id,  ...ids){
        super(optional_fields, copy_author_to_full_title, copy_title_to_full_title, ...ids);
        this.cover_preview = document.getElementById('cover_preview');
        //Getting fetch_button and adding listerener on it
        this.fetch_button_id = document.getElementById(fetch_button_id);
        this.fetch_button_id.addEventListener('click', () =>{
            if(this.supervise_input(this.inputs[0]))
                this.fetch_data(this.inputs[0].value);
            else{
                alert("Enter valid ISBN");
            }
        })

    }

    //Method below parse json, that came from googlebooks and extract from json asked informations given as arguments
    get_data_google(data, what){
        try{
            switch(what){
                case 0:{
                    return data.items['0'].volumeInfo.authors['0'] === false ? "" : data.items['0'].volumeInfo.authors['0'];
                }case 1:{
                    return data.items['0'].volumeInfo.title === undefined ? "" : data.items['0'].volumeInfo.title;
                }case 2:{
                    return data.items['0'].volumeInfo.publishedDate === undefined ? "" : data.items['0'].volumeInfo.publishedDate.substring(data.items['0'].volumeInfo.publishedDate.length - 4);
                }case 3:{
                    return data.items['0'].volumeInfo.publisher === undefined ? "" : data.items['0'].volumeInfo.publisher;
                }
                case 4:{
                    return data.items['0'].volumeInfo.pageCount === undefined ? "": 'number of pages: ' + data.items['0'].volumeInfo.pageCount;
                }
                default:{
                    return "";
                }
            }
        }catch(error){
            return "";
        }
    }

    //Method below parse json, that came from openlibrary.org and extract from json asked informations given as arguments
    get_data_openlibrary(isbn, data, what){
        try{
            switch(what){
                case 0:{
                    return data['ISBN:'+isbn].details.authors['0'].name === undefined ? false : data['ISBN:'+isbn].details.authors['0'].name;
                }case 1:{
                    return data['ISBN:'+isbn].details.title === undefined ? false : data['ISBN:'+isbn].details.title;
                }case 2:{
                    return data['ISBN:'+isbn].details.publish_date === undefined ? false : data['ISBN:'+isbn].details.publish_date.substring(data['ISBN:'+isbn].details.publish_date.length - 4)
                }case 3:{
                    return data['ISBN:'+isbn].details.publishers['0'] === undefined ? false : data['ISBN:'+isbn].details.publishers['0'];
                }case 4:{
                    return data['ISBN:'+isbn].details.number_of_pages === undefined ? false : 'Number of pages: ' + data['ISBN:'+isbn].details.number_of_pages;
                }case 5:{
                    return data['ISBN:'+isbn].details.contributions['0'] === undefined ? false : ', contributions: ' + data['ISBN:'+isbn].details.contributions['0'];
                }case 6:{
                    return data['ISBN:'+isbn].details.edition_name === undefined ? false : ', edition: ' + data['ISBN:'+isbn].details.edition_name;
                }case 7:{
                    return data['ISBN:'+isbn].details.covers[0] === undefined ? false : `https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg`;
                }
                default:{
                    return false;
                }
            }
        }
        catch(error){
            return false;
        }
    }

    //Method below invoke get_data_openlibrary and get_data_google in order to return most complete book's informations given as argument;
    fetch_book_info(isbn, data_openlibrary, data_google, what){
       switch(what){
           case 'author':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 0)){
                    console.log("Fetched author from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 0);
                }if(this.get_data_google(data_google, 0)){
                    console.log("Fetched author from google"); return this.get_data_google(data_google, 0);
                }
                return "";
            }
            case 'title':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 1)){
                    console.log("Fetched title from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 1);
                }if(this.get_data_google(data_google, 1)){
                    console.log("Fetched title from google"); return this.get_data_google(data_google, 1);
                }
                return "";
            }case 'pub_year':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 2)){
                    console.log("Fetched pub_year from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 2);
                }if(this.get_data_google(data_google, 2)){
                    console.log("Fetched pub_year from google"); return this.get_data_google(data_google, 2);
                }
                return "";
            }case 'publisher':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 3)){
                    console.log("Fetched publisher from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 3);
                }if(this.get_data_google(data_google, 3)){
                    console.log("Fetched publisher from google"); return this.get_data_google(data_google, 3);
                }  
                return "";
            }case 'pages':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 4)){
                    console.log("Fetched number of pages from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 4);
                }
                return "";
            }case 'contributions':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 5)){
                    console.log("Fetched contributors from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 5);
                }
                return "";
            }case 'edition':{
                if(this.get_data_openlibrary(isbn, data_openlibrary, 6)){
                    console.log("Fetched edition from openlibrary"); return this.get_data_openlibrary(isbn, data_openlibrary, 6);
                }
                return "";
            }case 'cover':{
                let cover = this.get_data_openlibrary(isbn, data_openlibrary, 7);
                if(cover){                    
                    console.log("Fetched cover from openlibrary"); return cover;
                }
                return "#";
            }
        }
    }

    

    //An asynchronical method that fetches data from openlibrary.org and googlebooks and then fills values of inputs, that exist in add-book-form
    async fetch_data(isbn){
        const that = this;
        // let url_openlibrary = `https://openlibrary.org/isbn/${isbn}.json`;
        let url_openlibrary = `https://openlibrary.org/api/books?bibkeys=ISBN:${isbn}&jscmd=details&format=json`;
        let url_google = `https://www.googleapis.com/books/v1/volumes?q=${isbn}+isbn&maxResults=1`;

        let response_google = await fetch(url_google);
        let data_google = await response_google.json();

        let response_openlibrary = await fetch(url_openlibrary);
        let data_openlibrary = await response_openlibrary.json();
        this.inputs[1].value = this.fetch_book_info(isbn, data_openlibrary, data_google, 'author');
        this.inputs[2].value = this.fetch_book_info(isbn, data_openlibrary, data_google, 'title');
        this.inputs[4].value = this.fetch_book_info(isbn, data_openlibrary, data_google, 'pub_year');
        this.inputs[5].value = this.fetch_book_info(isbn, data_openlibrary, data_google, 'publisher');
        this.inputs[6].value = this.fetch_book_info(isbn, data_openlibrary, data_google, 'pages') +
        this.fetch_book_info(isbn, data_openlibrary, data_google, 'contributions'); + this.fetch_book_info(isbn, data_openlibrary, data_google, 'edition');

        this.inputs[3].value = "";
        this.repeat_values(this.inputs[1], this.inputs[3]);
        this.repeat_values(this.inputs[2], this.inputs[3]);
        this.copy_checkboxes[0].checked = true; this.copy_checkboxes[1].checked = true;

        let aux_array = [1, 2, 3, 4, 5, 6];
        for(var i = 0; i < 6; i++){

            this.inputs_states[aux_array[i]] = this.supervise_input(this.inputs[aux_array[i]]);
            this.approve_input(aux_array[i]);
        }
    }

    supervise_input(item){
        switch(item.id){
            case 'isbn':{
                if(!this.excluded_inputs.includes(item))
                    return this.check_if_numeric(item, true) && item.value.length > 9 && item.value.length < 14;
            }case 'author':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'title': case 'full_title':{
                return item.value !== "";
            }case 'pub_year':{
                if(!this.excluded_inputs.includes(item))
                    return this.check_if_numeric(item, false); 
            }case 'publisher':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'description':{
                return item.value !== "";
            }case 'condition':{
                return item.value === "1" || item.value === '2';
            }case 'availability':{
                return item.value === "1" || item.value === '2';
            }case 'cover':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }
        }
    }
}

class AddMovie extends AddItem{
    supervise_input(item){
        switch(item.id){
            case 'author':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'screenwriter':{
                return item.value !== "";
            }case 'title': case 'full_title':{
                return item.value !== "";
            }case 'pub_year':{
                if(!this.excluded_inputs.includes(item))
                    return this.check_if_numeric(item, false); 
            }case 'publisher':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'description':{
                return item.value !== "";
            }case 'condition':{
                return item.value === "1" || item.value === '2';
            }case 'availability':{
                return item.value === "1" || item.value === '2';
            }case 'cover':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }
        }
    }
}

class AddSoundRecording extends AddItem{
    supervise_input(item){
        switch(item.id){
            case 'author':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }case 'title': case 'full_title':{
                return item.value !== "";
            }case 'cast':{
                return item.value !== "";
            }case 'pub_year':{
                if(!this.excluded_inputs.includes(item))
                    return this.check_if_numeric(item, false); 
            }case 'description':{
                return item.value !== "";
            }case 'condition':{
                return item.value === "1" || item.value === '2';
            }case 'availability':{
                return item.value === "1" || item.value === '2';
            }case 'cover':{
                if(!this.excluded_inputs.includes(item))
                    return item.value !== "";
            }
        }
    }
}