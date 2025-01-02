// movimenta os Filmes pra esqueda ou direita
document.addEventListener('DOMContentLoaded', function() {
  const btnEsquerda = document.getElementById('btn-esquerda');
  const btnDireita = document.getElementById('btn-direita');
  const lista = document.getElementById('lista');

  btnEsquerda.addEventListener('click', function() {
      lista.scrollBy({
          left: -400,
          behavior: 'smooth'
      });
  });

  btnDireita.addEventListener('click', function() {
      lista.scrollBy({
          left: 400,
          behavior: 'smooth'
      });
  });
});

//movimenta as Séries pra esqueda ou direita
document.addEventListener('DOMContentLoaded', function() {
  const btnEsquerda2 = document.getElementById('btn-esquerda2');
  const btnDireita2 = document.getElementById('btn-direita2');
  const lista2 = document.getElementById('lista2');

  btnEsquerda2.addEventListener('click', function() {
      lista2.scrollBy({
          left: -400,
          behavior: 'smooth'
      });
  });

  btnDireita2.addEventListener('click', function() {
      lista2.scrollBy({
          left: 400,
          behavior: 'smooth'
      });
  });
});

//pesquisa
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

