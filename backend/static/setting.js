
// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Get the sections we want to show and hide when selecting the radio buttons
    const div_lang = document.getElementById('div_lang');
    const div_akut = document.getElementById('div_akut');
    const div_ambulant = document.getElementById('div_ambulant');
    const title_set = document.getElementById('title_set');
    const data_protection_set = document.getElementById('data_protection_set');
    const next = document.querySelector('#next_button_sett');

    // By default hide them
    div_lang.style.display = 'none';
    div_akut.style.display = 'none';
    div_ambulant.style.display = 'none';
    title_set.style.display = 'none';
    data_protection_set.style.display = 'none';
    next.disabled = true;

    // When selection each of the radio buttons we will show a different section 
    function handleRadioClick() {
        title_set.style.display = 'block';
        data_protection_set.style.display = 'block';
        next.disabled = false;
        if (document.getElementById('choice_lang').checked) {
            div_lang.style.display = 'block';
            div_akut.style.display = 'none';
            div_ambulant.style.display = 'none';
        } else if (document.getElementById('choice_akut').checked){
            div_lang.style.display = 'none';
            div_akut.style.display = 'block';
            div_ambulant.style.display = 'none';
        } else {
            div_lang.style.display = 'none';
            div_akut.style.display = 'none';
            div_ambulant.style.display = 'block';
        }
    }

    // Look if a radio button is selected
    const radioButtons = document.querySelectorAll('input[name="choice_setting"]');
    radioButtons.forEach(radio => {
    radio.addEventListener('click', handleRadioClick);
    });

    // When submiting the form check if all the mandatory fields are selected:
    document.querySelector('form').onsubmit = function(){

        // First we need to check which radio button is selected:
        if (document.getElementById('choice_lang').checked) {
            // Get mandatory checkboxes
            var lang_box3 = document.getElementById('Lang3');
            var lang_box6 = document.getElementById('Lang6');
            var lang_box7 = document.getElementById('Lang7');
            var lang_box8 = document.getElementById('Lang8');
            var lang_box13 = document.getElementById('Lang13');
            var lang_box14 = document.getElementById('Lang14');
            var lang_box15 = document.getElementById('Lang15');
            var lang_box16 = document.getElementById('Lang16');

            // If the mandatory boxes are selected we can move to the next page 
            if (lang_box3.checked && lang_box6.checked && lang_box7.checked && lang_box8.checked && lang_box13.checked && lang_box14.checked && lang_box15.checked && lang_box16.checked){
                return true;
            } else { // If not selected then we alert the user and give the option to return to the page or continue incompleate
                if (confirm("Sie haben nicht alle vom Anbieter als erforderlich eingestuften Teilnehmenden ausgewählt. Möchten Sie dennoch fortfahren?") == true) {
                    return true;
                } else {
                    return false;
                }
            }
        } else if (document.getElementById('choice_akut').checked){
            var akut_box1 = document.getElementById('Aku1');
            var akut_box2 = document.getElementById('Aku2');
            var akut_box3 = document.getElementById('Aku3');
            var akut_box7 = document.getElementById('Aku7');
            var akut_box8 = document.getElementById('Aku8');
            var akut_box10 = document.getElementById('Aku10');
            var akut_box11 = document.getElementById('Aku11');
            var akut_box12 = document.getElementById('Aku12');

            if (akut_box1.checked && akut_box2.checked && akut_box3.checked && akut_box7.checked && akut_box8.checked && akut_box10.checked && akut_box11.checked && akut_box12.checked){
                return true;
            } else { // If not selected then we alert the user and give the option to return to the page or continue incompleate
                if (confirm("Sie haben nicht alle vom Anbieter als erforderlich eingestuften Teilnehmenden ausgewählt. Möchten Sie dennoch fortfahren?") == true) {
                    return true;
                } else {
                    return false;
                }
            }

        } else {
            var ambulant_box3 = document.getElementById('Ambu3');
            var ambulant_box4 = document.getElementById('Ambu4');
            var ambulant_box7 = document.getElementById('Ambu7');
            var ambulant_box8 = document.getElementById('Ambu8');
            var ambulant_box10 = document.getElementById('Ambu10');
            var ambulant_box11 = document.getElementById('Ambu11');
            var ambulant_box15 = document.getElementById('Ambu15');
            var ambulant_box16 = document.getElementById('Ambu16');
            var ambulant_box17 = document.getElementById('Ambu17');

            if (ambulant_box3.checked && ambulant_box4.checked && ambulant_box7.checked && ambulant_box8.checked && ambulant_box10.checked && ambulant_box11.checked && ambulant_box15.checked && ambulant_box16.checked && ambulant_box17.checked){
                return true;
            } else { // If not selected then we alert the user and gibe the option to return to the page or continue incompleate
                if (confirm("Sie haben nicht alle vom Anbieter als erforderlich eingestuften Teilnehmenden ausgewählt. Möchten Sie dennoch fortfahren?") == true) {
                    return true;
                } else {
                    return false;
                }
            }

        }

    };

});
