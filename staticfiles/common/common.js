function popup_confirmation(message, url){
    var input = confirm(message);
    if (input == true) {
        window.location = url;
    }
}

function is_number_valid(number){
    for(var i=0; i<number.length; i++){
        if(number[i]<'0' || number[i] >'9')
            return false;
    }
    return true;
}

function valid_number_status(value_id, span_id){
    amount = document.getElementById(value_id).value;
    if(is_number_valid(amount)){
        document.getElementById(span_id).innerHTML="";
    }
    else{
        document.getElementById(span_id).innerHTML="Special characters not allowed";
    }
}