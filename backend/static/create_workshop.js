// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Get the elements that we want to activate and deactivate 
    const createWS_next = document.querySelector('#next_button_createWS');

    createWS_next.disabled = true;
    document.getElementById("text_name_workshop").addEventListener('keyup', success, false);

    function success() {
        if(document.getElementById("text_name_workshop").value==="") { 
            createWS_next.disabled = true;
        } else { 
            createWS_next.disabled = false;
        }
    }

    

});