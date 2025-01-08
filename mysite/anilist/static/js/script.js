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


//Aguarde o Dom carregar
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todas as mensagens com ID 'notification'
    const notifications = document.querySelectorAll('#notification');

    //Define o tempo de exibição da mensagem
    const duration = 1500; // 3 segundos

    notifications.forEach(notification => {
        //configura o tempo de exibição para cada mensagem
        setTimeout(() => {
            //Configura a mensagem para desaparecer
            notification.style.transition = "opacity 0.3s ease"; // transição de 0.5 segundos suave
            notification.style.opacity = 0; //esconde a mensagem
            setTimeout(() => notification.remove(), 500); //remove a mensagem após 0.5 segundos
        }, duration);
    });
});

//Evita o reenvio do formulário
const form = document.getElementById('form');
form.addEventListener('submit', function(event) {
    //salva os dados do formulario em uma variavel local ou processa como necessário
    sessionStorage.setItem('formSubmitted', 'true');
});

if (sessionStorage.getItem('formSubmitted')){
    //se o formulário foi enviado, impede o reenvio
    sessionStorage.removeItem('formSubmitted');
    window.location.href = window.location.href; //redireciona para a mesma página
}
