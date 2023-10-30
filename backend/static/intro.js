// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    const intro1 = document.querySelector("#intro1");
    const intro2 = document.querySelector("#intro2");
    const intro3 = document.querySelector("#intro3");
    const intro4 = document.querySelector("#intro4");

    // The first time we access the webpage we show the first slide of the introduction
    intro2.style.display = 'none';
    intro3.style.display = 'none';
    intro4.style.display = 'none';

    // Move to slide 2
    document.querySelector("#button_intro1").onclick = function (){
        intro1.style.display = 'none';
        intro2.style.display = 'block';
        intro3.style.display = 'none';
        intro4.style.display = 'none';
    }

    // Move to slide 3
    document.querySelector("#button_intro2").onclick = function (){
        intro1.style.display = 'none';
        intro2.style.display = 'none';
        intro3.style.display = 'block';
        intro4.style.display = 'none';
    }

    // Move to slide 4
    document.querySelector("#button_intro3").onclick = function (){
        intro1.style.display = 'none';
        intro2.style.display = 'none';
        intro3.style.display = 'none';
        intro4.style.display = 'block';
    }

    // Move back to slide 1
    document.querySelector("#button_intro_back2").onclick = function (){
        intro1.style.display = 'block';
        intro2.style.display = 'none';
        intro3.style.display = 'none';
        intro4.style.display = 'none';
    }

    // Move back to slide 2
    document.querySelector("#button_intro_back3").onclick = function (){
        intro1.style.display = 'none';
        intro2.style.display = 'block';
        intro3.style.display = 'none';
        intro4.style.display = 'none';
    }

    // Move back to slide 3
    document.querySelector("#button_intro_back4").onclick = function (){
        intro1.style.display = 'none';
        intro2.style.display = 'none';
        intro3.style.display = 'block';
        intro4.style.display = 'none';
    }

});
