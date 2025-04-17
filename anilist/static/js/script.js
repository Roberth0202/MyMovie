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

//fazer o menu funcionar
function toggleMenu() {
    const hamburger = document.querySelector('.hamburger-icon');
    const navLinks = document.querySelector('.nav-links');
    
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('active');
    
    // Impedir rolagem quando o menu está aberto
    document.body.classList.toggle('menu-open');
}

  // Fechar o menu ao clicar em um link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
    const hamburger = document.querySelector('.hamburger-icon');
    const navLinks = document.querySelector('.nav-links');

    hamburger.classList.remove('open');
    navLinks.classList.remove('active');
    document.body.classList.remove('menu-open');
    });
});

// Fechar o menu quando clicar fora dele
document.addEventListener('click', (event) => {
    const hamburger = document.querySelector('.hamburger-icon');
    const navLinks = document.querySelector('.nav-links');
    
    // Verificar se o menu está aberto e se o clique não foi no menu ou no ícone
    if (navLinks.classList.contains('active') && 
        !event.target.closest('.nav-links') && 
        !event.target.closest('.hamburger-icon')) {
        
        hamburger.classList.remove('open');
        navLinks.classList.remove('active');
        document.body.classList.remove('menu-open');
    }
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

//Aguarde o Dom carregar
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todas as mensagens com ID 'notification'
    const notifications = document.querySelectorAll('#notification');

    //Define o tempo de exibição da mensagem
    const duration = 10000; // 5 segundos

    notifications.forEach(notification => {
        //configura o tempo de exibição para cada mensagem
        setTimeout(() => {
            //Configura a mensagem para desaparecer
            notification.style.transition = "opacity 0.5s ease"; // transição de 0.5 segundos suave
            notification.style.opacity = 0; //esconde a mensagem
            setTimeout(() => notification.remove(), 500); //remove a mensagem após 0.5 segundos
        }, duration);
    });
});