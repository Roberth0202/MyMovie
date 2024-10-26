// Filmes
const listaContainer = document.getElementById('lista'); // Selecionando a div pelo ID
const btnEsquerda = document.getElementById('btn-esquerda');
const btnDireita = document.getElementById('btn-direita');

function rolarEsquerda() {
  listaContainer.scrollLeft -= 400;
} 

function rolarDireita() {
  listaContainer.scrollLeft += 400;
}

btnEsquerda.addEventListener('click', rolarEsquerda);
btnDireita.addEventListener('click', rolarDireita);

// Séries
const listaContainer2 = document.getElementById('lista2'); // Selecionando a div pelo ID
const btnEsquerda2 = document.getElementById('btn-esquerda2');
const btnDireita2 = document.getElementById('btn-direita2');

function rolarEsquerda2() {
  listaContainer2.scrollLeft -= 400;
} 

function rolarDireita2() {
  listaContainer2.scrollLeft += 400;
}

btnEsquerda2.addEventListener('click', rolarEsquerda2);
btnDireita2.addEventListener('click', rolarDireita2);



document.addEventListener('DOMContentLoaded', function() {
    let input = document.querySelector('input[name="q"]');
    let results = document.getElementById('search-results');
    
    input.addEventListener('input', async function() {
        if (input.value.length > 0) {
            let response = await fetch('/search?q=' + input.value);
            let shows = await response.json();
            results.innerHTML = '';
            shows.forEach(show => {
                let li = document.createElement('li');
                li.textContent = show.name;
                results.appendChild(li);
            });
        } else {
            results.innerHTML = '';
        }
    });
});