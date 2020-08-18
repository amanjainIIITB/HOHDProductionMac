function validate_client(){
    var client_id_or_contact_number = (document.getElementById('Contact_Number').value);
    var all_membership_based_on_shop_id = {{membership_based_on_shop_id|safe}};
    for(i=0; i < all_membership_based_on_shop_id.length; i++)
    {
        var membership_found = false;
        if(client_id_or_contact_number == all_membership_based_on_shop_id[i].Contact_Number)
        {
            document.getElementById('client_details').innerHTML = "<table ><tr><td>ID</td><td>"+all_membership_based_on_shop_id[i].custID+"</td</tr><tr><td>Name</td><td>"+all_membership_based_on_shop_id[i].Name+"</td></tr><tr><td>Date of Birth</td><td>"+all_membership_based_on_shop_id[i].DOB+"</td></tr><tr><td>Contact Number</td><td>"+all_membership_based_on_shop_id[i].Contact_Number+"</td></tr></table><br><br>";
            membership_found = true;
            break;
        }
    }
    if(membership_found == false){
        if(client_id_or_contact_number == "")
            document.getElementById('client_details').innerHTML = "Please Enter Client Contact Number";
        else
            document.getElementById('client_details').innerHTML = "Entered Number doesn't exist";
    }
}