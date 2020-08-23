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

function print_number_status(value_id, span_id){
    amount = document.getElementById(value_id).value;
    if(is_number_valid(amount)){
        document.getElementById(span_id).innerHTML="";
    }
    else{
        document.getElementById(span_id).innerHTML="Special characters not allowed";
    }
}

function autocomplete(value_id, data){
    const suggestionsPanel = document.getElementById('suggestions')
    suggestionsPanel.innerHTML='';
    suggested_contact_numbers = [];
    var user_entered_contact_number = document.getElementById(value_id).value;
    for(i=0; i<data.length; i++){
        if((data[i].Contact_Number).toString().startsWith(user_entered_contact_number))
            suggested_contact_numbers.push(data[i].Contact_Number);
    }
    if (user_entered_contact_number!=''){
        suggested_contact_numbers.forEach(element => {
            const div = document.createElement('div');
            div.innerHTML=element;
            suggestionsPanel.appendChild(div);
        });
    }
}


function print_client_details(client_details){
    if(client_details != ''){
        document.getElementById('client_details').innerHTML = "<table ><tr><td>ID</td><td>"+client_details.custID+"</td</tr><tr><td>Name</td><td>"+client_details.Name+"</td></tr><tr><td>Date of Birth</td><td>"+client_details.DOB+"</td></tr><tr><td>Contact Number</td><td>"+client_details.Contact_Number+"</td></tr></table><br><br>";
    }
    else{
        document.getElementById('client_details').innerHTML = "Number doesn't exist";
    }
}

function get_client_details_based_on_contact_number(value_id, data){
    var client_id_or_contact_number = document.getElementById(value_id).value;
    var all_membership_based_on_shop_id = data;
    var client_details = '';
    for(i=0; i < all_membership_based_on_shop_id.length; i++)
    {
        if(client_id_or_contact_number == all_membership_based_on_shop_id[i].Contact_Number)
        {
            client_details = all_membership_based_on_shop_id[i];
            break;
        }
    }
    return client_details
}

function get_client_details_based_on_clientID(value_id, data){
    var client_id_or_contact_number = (document.getElementById(value_id).value).toUpperCase();
    console.log();
    var all_membership_based_on_shop_id = data;
    var client_details = '';
    for(i=0; i < all_membership_based_on_shop_id.length; i++)
    {
        console.log(client_id_or_contact_number);
        console.log(all_membership_based_on_shop_id[i].custID);
        if(client_id_or_contact_number == all_membership_based_on_shop_id[i].custID)
        {
            client_details = all_membership_based_on_shop_id[i];
            break;
        }
    }
    return client_details
}

function setDate(id, date){
    var d = new Date(date);
    var day = d.getDate();
    if(day<=9)
        day = '0'+day;
    var month = d.getMonth()+1;
    if(month<=9)
        month = '0'+month;
    document.getElementById(id).value = d.getFullYear()+"-"+month+"-"+day;
}