// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    const show_pass_delete_user = document.querySelector("#show_pass_delete_user");
    const submit = document.querySelector('#delete_button_user');


    // Hide the section to introduce the password of the user to confirm the deletion and disable submit button
    show_pass_delete_user.style.display = 'none';
    submit.disabled = true;

    // Show password section when selection one option
    function handleRadioClick() {
        show_pass_delete_user.style.display = 'block';
    }

    // Look if a radio button is selected
    const radioButtons = document.querySelectorAll('input[name="user_id"]');
    radioButtons.forEach(radio => {
    radio.addEventListener('click', handleRadioClick);
    });

    // Enable delete button when there is text in the password section 
    document.getElementById("password_text").addEventListener('keyup', success_pass, false);

    function success_pass() {
        if(document.getElementById("password_text").value==="") { 
            submit.disabled = true;
        } else { 
            submit.disabled = false;
        }
    }

});