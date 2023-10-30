// Wait for page to load
document.addEventListener('DOMContentLoaded', function() { //After loading the whole document, do what is in the function
    const submit = document.querySelector('#next_button');
    const button = document.querySelector('#clear_button');
    // const textarea_ja= document.querySelector('#text_jaaber');
    // const textarea_nein= document.querySelector('#text_nein');
    const textarea_comment= document.querySelector('#text_comment');

    // Disable buttons and comments areas by default:
    submit.disabled = true;
    button.disabled = true;
    // textarea_ja.disabled = true;
    // textarea_nein.disabled = true;
    textarea_comment.disabled = true;

    document.querySelector('#choice_ja_aber').onclick = function() {
        // Enable text area related with "ja, aber"
        textarea_ja.disabled = false;

        // Disable and deleting content in text are related with "nein"
        textarea_nein.disabled = true;
        // textarea_nein.value = '';

        // Enable buttons when one option is selected
        submit.disabled = false;
        button.disabled = false;
    }
    document.querySelector('#choice_nein').onclick = function() {
        // Diable "ja, aber"
        textarea_ja.disabled = true;
        // textarea_ja.value = '';

        // Enable "nein"
        textarea_nein.disabled = false;  
        
        // Enable buttons when one option is selected
        submit.disabled = false;
        button.disabled = false;
    }
    document.querySelector('#choice_ja').onclick = function() {
        // Disable "ja, aber" und "nein"
        textarea_ja.disabled = true;
        // textarea_ja.value = '';
        textarea_nein.disabled = true;
        // textarea_nein.value = '';

        // Enable buttons when one option is selected
        submit.disabled = false;
        button.disabled = false;
    }

    // When clicking the clear button, we delete all the information selected and written
    document.querySelector('#clear_button').onclick = function() {

        // Clear all radio buttons
        document.querySelector('input[name="choice"]:checked').checked = false;

        // We disable the comment section, so it is not possible to write a comment without selecting a choice
        textarea_comment.disabled = true;
        textarea_comment.value = '';

        // Disable "ja, aber" und "nein"
        // textarea_ja.disabled = true;
        // textarea_ja.value = '';
        // textarea_nein.disabled = true;
        // textarea_nein.value = '';

        // Disable buttons when one option is selected
        submit.disabled = true;
        button.disabled = true;

    }

});