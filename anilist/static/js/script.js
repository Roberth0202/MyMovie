//----------------------------------- SLIDE DA FILME ESQUERDA E DIREITA -------------------------------------
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

//-------------------------------------- SLIDE DA SÉRIE ESQUERDA E DIREITA ------------------------------------------
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

//------------------------------------- FAZ O MENU FUNCIONAR -------------------------------------
function toggleMenu() {
    const hamburger = document.querySelector('.hamburger-icon');
    const navLinks = document.querySelector('.nav-links');
    
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('active');
    
    // Impedir rolagem quando o menu está aberto
    document.body.classList.toggle('menu-open');
}

//----------------- FECHA O MENU QUANDO APERTA EM UM LINK --------------------
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
    const hamburger = document.querySelector('.hamburger-icon');
    const navLinks = document.querySelector('.nav-links');

    hamburger.classList.remove('open');
    navLinks.classList.remove('active');
    document.body.classList.remove('menu-open');
    });
});

//------------------ FECHA O MENU AO CLICAR FORA -------------------
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



//------------------------------------- SISTEMA DE PESQUISA PRA MOBILE -------------------------------------
// Adicione esta função ao seu JavaScript
function setupOutsideClickHandler() {
    document.addEventListener('click', function(event) {
        const searchContainer = document.getElementById('content-search-mobile');
        const searchIcon = document.getElementById('mobile-search-icon');
        
        // Verifica se o elemento de pesquisa está visível
        if (searchContainer.classList.contains('active')) {
            // Verifica se o clique foi fora do container de pesquisa E fora do ícone de pesquisa
            if (!searchContainer.contains(event.target) && !searchIcon.contains(event.target)) {
                // Esconde o container de pesquisa
                searchContainer.classList.remove('active');
            }
        }
    });
}

// Modifique sua função toggleSearch
function ToggleSearch(event) {
    // Impede que o evento de clique se propague para o documento
    event.stopPropagation();
    
    const searchContainer = document.getElementById('content-search-mobile');
    searchContainer.classList.toggle('active');
    
    if (searchContainer.classList.contains('active')) {
        setTimeout(() => {
            searchContainer.querySelector('input').focus();
        }, 300);
    }
}

// Inicialize o handler quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    setupOutsideClickHandler();
    
    // Impede que cliques dentro da área de pesquisa fechem ela
    const searchContainer = document.getElementById('content-search-mobile');
    searchContainer.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});


//----------------------------------------------- PESQUISA --------------------------------------------------
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

//------------------------------------- EVITA O REENVIO DO FORMULARIO ----------------------------------
const form = document.getElementById('favorito-form');
form.addEventListener('submit', function(event) {
    //salva os dados do formulario em uma variavel local ou processa como necessário
    sessionStorage.setItem('formSubmitted', 'true');
});

if (sessionStorage.getItem('formSubmitted')){
    //se o formulário foi enviado, impede o reenvio
    sessionStorage.removeItem('formSubmitted');
    window.location.href = window.location.href; //redireciona para a mesma página
}

//------------------------------- SISTEMA AJAX PRA IMPERDIR O REINICIO DA PAGINA AO ADICIONAR AOS FAVORITOS ----------------------------------
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('favorito-form');
    const button = document.getElementById('favorito-btn');
    const img = document.getElementById('coracao-img');

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // impedir recarregamento

        const mediaId = document.querySelector('[name="media_id"]').value;
        const midiaType = document.querySelector('[name="midia_type"]').value;
        const action = button.getAttribute('value'); // pega o value do botão

        fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: new URLSearchParams({
                media_id: mediaId,
                midia_type: midiaType,
                action: action,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "added") {
                button.setAttribute('value', 'remove'); // MUDA O VALUE
                button.setAttribute('name', 'action');  // mantém o name correto
                img.src = "/static/img/coração_preenchido.svg";
            } else if (data.status === "removed") {
                button.setAttribute('value', 'add'); // MUDA O VALUE
                button.setAttribute('name', 'action');
                img.src = "/static/img/coração_vazio.svg";
            }
        })
        .catch(error => console.error("Erro no AJAX:", error));
    });
});

//--------------------------------- NOTIFICAÇÃO ---------------------------
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