window.onload = function() {
    loadBoxes();
};

// ... (остальной код такой же)

function loadBoxes() {
    fetch('/lab9/rest-api/boxes')
        .then(data => data.json())
        .then(boxes => {
            let area = document.getElementById('area');
            area.innerHTML = '';
            
            boxes.forEach(box => {
                let div = document.createElement('div');
                div.className = 'box';
                div.id = 'box-' + box.id;
                div.style.backgroundImage = `url(${box.img})`;
                div.style.top = box.top + '%';
                div.style.left = box.left + '%';
                
                if (box.opened) {
                    div.classList.add('opened');
                } else if (box.need_auth) {
                    div.classList.add('locked');
                    div.onclick = () => alert('🔒 Войдите через /lab5/login!');
                } else {
                    div.onclick = () => openBox(box.id);
                }
                area.appendChild(div);
            });
        })
        .catch(error => console.error('Ошибка загрузки:', error));
}


function openBox(id) {
    fetch(`/lab9/rest-api/open/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        showModal(data.text, data.img);
        document.getElementById('count').textContent = data.unopened;
        loadBoxes();
    })
    .catch(error => alert(error.message));
}

function showModal(text, img) {
    document.getElementById('text').textContent = text;
    document.getElementById('img').src = img;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

window.onclick = (event) => {
    if (event.target.id === 'modal') closeModal();
};

function resetBoxes() {
    if (!confirm('🧙 Дед Мороз наполнит все коробки подарками снова?')) return;
    
    fetch('/lab9/rest-api/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => alert('Ошибка: ' + error.message));
}
