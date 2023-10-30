// Wait for page to load
document.addEventListener('DOMContentLoaded', function() { //After loading the whole document, do what is in the function
    const submit = document.querySelector('#next_button');
    const button = document.querySelector('#clear_button');
    // const textarea_comment= document.querySelector('#text_comment');
    const textarea_jaaber= document.querySelector('#text_jaaber');
    const textarea_nein= document.querySelector('#text_nein');
    const textarea_unless= document.querySelector('#text_unless');
    const div_nein_section = document.querySelector('#nein_section');

    // Disable buttons and comments areas by default:
    submit.disabled = true;
    button.disabled = true;
    // textarea_comment.disabled = true;
    textarea_jaaber.style.display = 'none';
    textarea_nein.style.display = 'none';
    textarea_unless.style.display = 'none';
    div_nein_section.style.display = 'none';


    document.querySelector('#choice_ja_aber').onclick = function() {
        // It is possible to write a comment once an option is selected 
        // textarea_comment.disabled = false;
        textarea_jaaber.style.display = 'block';
        textarea_nein.style.display = 'none';
        textarea_unless.style.display = 'none';

        // Enable buttons when one option is selected
        submit.disabled = true;
        button.disabled = false;

        // Hide nein section
        div_nein_section.style.display = 'none';

        // Remove content in nein textarea so the button is again disabled
        textarea_nein.value = '';
        textarea_unless.value = '';
    }
    document.querySelector('#choice_nein').onclick = function() {
        // It is possible to write a comment once an option is selected
        // textarea_comment.disabled = false;
        textarea_jaaber.style.display = 'none';
        textarea_nein.style.display = 'block';
        textarea_unless.style.display = 'block';

        // Enable buttons when one option is selected
        submit.disabled = true;
        button.disabled = false;

        // Show nein section
        div_nein_section.style.display = 'block';

        // Remove content in ja_aber area so submit button is again disabled
        textarea_jaaber.value = '';
    }
    document.querySelector('#choice_ja').onclick = function() {
        // It is possible to write a comment once an option is selected
        // textarea_comment.disabled = false;
        textarea_jaaber.style.display = 'none';
        textarea_nein.style.display = 'none';
        textarea_unless.style.display = 'none';

        // Enable buttons when one option is selected
        submit.disabled = false;
        button.disabled = false;

        // Hide nein section
        div_nein_section.style.display = 'none';
    }

    // When clicking the clear button, we delete all the information selected and written
    document.querySelector('#clear_button').onclick = function() {

        // Clear all radio buttons
        document.querySelector('input[name="choice"]:checked').checked = false;

        // We disable the comment section, so it is not possible to write a comment without selecting a choice
        // textarea_comment.disabled = true;
        // textarea_comment.value = '';
        textarea_jaaber.style.display = 'none';
        textarea_jaaber.value = '';
        textarea_nein.style.display = 'none';
        textarea_nein.value = '';
        textarea_unless.style.display = 'none';
        textarea_unless.value = '';


        // Disable buttons when one option is selected
        submit.disabled = true;
        button.disabled = true;

        // Hide nein section
        div_nein_section.style.display = 'none';

    }

    // Enable next page button when there is text in the comment section in both ja_aber and nein
    document.getElementById("text_jaaber").addEventListener('keyup', success_aber, false);
    document.getElementById("text_nein").addEventListener('keyup', success_nein, false);

    function success_aber() {
        if(document.getElementById("text_jaaber").value==="") { 
            submit.disabled = true;
        } else { 
            submit.disabled = false;
        }
    }

    function success_nein() {
        if(document.getElementById("text_nein").value==="") { 
            submit.disabled = true;
        } else { 
            submit.disabled = false;
        }
    }

});