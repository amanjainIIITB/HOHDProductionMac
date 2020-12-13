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
        document.getElementById(span_id).innerHTML="Note: Special characters not allowed";
    }
}

function print_contact_number_validations_and_errors(is_suggestions_available, contact_number_id, members, client_details_id){
    // we have few suggestion
    if(is_suggestions_available){
        client_details = get_client_details_based_on_contact_number(contact_number_id, members);
        // enetered correct number
        if(client_details != ""){
            print_client_details(document.getElementById(contact_number_id).value, client_details, client_details_id);
        }
        // entered half correct number
        else{
            document.getElementById(client_details_id).innerHTML="";
        }
    }
    // Either Not exist number or invalid number
    else{
        print_client_details(document.getElementById(contact_number_id).value, "", client_details_id);
    }
}

function autocomplete(value_id, data, suggestions_id){
    // https://www.youtube.com/watch?v=MBJuTkILZYo&t=1059s
    const suggestionsPanel = document.getElementById(suggestions_id)
    suggestionsPanel.innerHTML='';
    suggested_contact_numbers = [];
    var user_entered_contact_number = document.getElementById(value_id).value;
    var suggestions_available = false;
    for(i=0; i<data.length; i++){
        if((data[i].Contact_Number).toString().startsWith(user_entered_contact_number)){
            suggested_contact_numbers.push(data[i].Contact_Number);
            suggestions_available = true;
        }
    }
    if (user_entered_contact_number!=''){
        var html = ''
        for(i=0; i<suggested_contact_numbers.length; i++){
            html = html + '<div onclick="set_contact_number(' + suggested_contact_numbers[i] + ')">'+suggested_contact_numbers[i]+'</div>';
        }
        suggestionsPanel.innerHTML = html;
    }
    return suggestions_available;
}

function create_textarea_with_data(data){
    html = "<div class=\"col-sm-6\">";
    html = html + "<div class=\"form-group\">";
    html = html + "<label>Client Details</label>";
    html = html + "<textarea class=\"form-control\" rows=\"4\"  id=\"user_details\" disabled>";
    html = html + data;
    html = html + "</textarea>";
    html = html + "</div>";
    html = html + "</div>";          
    return html;              
}

function print_client_details(value, client_details, client_details_id){
    if(client_details != ''){
        html = create_textarea_with_data("ID: "+client_details.custID+"\nName: "+client_details.Name+"\nContact Number: "+client_details.Contact_Number+"\nDOB: "+client_details.DOB);
        document.getElementById(client_details_id).innerHTML = html;
    }
    else{
        if(value == ""){
            document.getElementById(client_details_id).innerHTML = "";
        }
        else if(is_number_valid(value) == false){
            document.getElementById(client_details_id).innerHTML = "NOTE: Invalid Number";
        }
        else{
            document.getElementById(client_details_id).innerHTML = "NOTE: Number doesn't exist";
        }
    }
}

function get_client_details_based_on_contact_number(value_id, all_membership_based_on_shop_id){
    var client_id_or_contact_number = document.getElementById(value_id).value;
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

function get_client_details_based_on_clientID(value_id, all_membership_based_on_shop_id){
    var client_id_or_contact_number = (document.getElementById(value_id).value).toUpperCase();
    var client_details = '';
    for(i=0; i < all_membership_based_on_shop_id.length; i++)
    {
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

function set_card_body(panelIndex){
    tabs[0].style.color="white";
    tabs[1].style.color="white";
    if(panelIndex=="0"){
        tabs[1].style.backgroundColor="grey";
        tabs[0].style.backgroundColor="#007bff";
        panels[0].style.display="block";
        panels[1].style.display="none";
    }
    else{
        tabs[0].style.backgroundColor="grey";
        tabs[1].style.backgroundColor="#007bff";
        panels[1].style.display="block";
        panels[0].style.display="none";
    }
}

function displayPagePermissions(employee_access_id, page_permission_span_id, page_permissions, page_display_dict, is_checkbox_disable) {
    document.getElementById(page_permission_span_id).innerHTML = "";
    var span = document.getElementById(page_permission_span_id);
    employee_access = document.getElementById(employee_access_id).value;
    if (employee_access == "YES") {
        for (var key in page_display_dict){
            var label = document.createElement("LABEL");
            label.appendChild(document.createTextNode(key));

            var form_group = document.createElement("DIV");
            form_group.classList.add("form-group");

            form_group.appendChild(label);

            var div_row = document.createElement("div");
            div_row.classList.add("row");

            for (page in page_display_dict[key]){
                if(page_display_dict[key][page][3] == 1){
                    var div_col = document.createElement("div");
                    div_col.classList.add("col-md-3");

                    var div_form_check = document.createElement("div");
                    div_form_check.classList.add("form-check");

                    var label = document.createElement("LABEL");
                    label.classList.add("form-check-label");
                    label.appendChild(document.createTextNode(page_display_dict[key][page][0]));

                    var input = document.createElement("INPUT");
                    input.classList.add("form-check-input");
                    input.setAttribute("type", "checkbox");
                    if (is_checkbox_disable) {
                        input.setAttribute("disabled", true);
                    }
                    if (page_permissions.includes(page_display_dict[key][page][2])){
                        input.setAttribute("checked", true);
                    }
                    input.setAttribute("name", "page_list[]");
                    input.setAttribute("value", page_display_dict[key][page][2]);

                    div_form_check.appendChild(input);
                    div_form_check.appendChild(label);
                    div_col.appendChild(div_form_check);
                    div_row.appendChild(div_col);
                    form_group.appendChild(div_row);
                }
            }
            span.appendChild(form_group);
        }
    }
}