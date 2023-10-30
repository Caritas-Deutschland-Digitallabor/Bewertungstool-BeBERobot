// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Get the elements that we want to activate and deactivate 
    const listWS_next = document.querySelector('#next_button_listWS');
    const listWS_delete = document.querySelector('#delete_button_listWS');

    // By default deactivate them
    listWS_next.disabled = true;
    listWS_delete.disabled = true;

    // Enable next and delete button when selection one option
    function handleRadioClick() {
        listWS_next.disabled = false;
        listWS_delete.disabled = false;
    }

    // Look if a radio button is selected
    const radioButtons = document.querySelectorAll('input[name="workshop_id"]');
    radioButtons.forEach(radio => {
    radio.addEventListener('click', handleRadioClick);
    });

    // Set an alert to confirm the deletion of a workshop
    document.querySelector('#delete_button_listWS').onclick = function(){
        if (confirm("Sind Sie sicher, dass Sie diesen Workshop löschen möchten?") == true) {
            return true;
        } else {
            return false;
        }

    };


    

});