function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
        
            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText = films[i].title;
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);
 
            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    });
}

function deleteFilm(id, title) {
    if(!confirm('Вы точно хотите удалить фильм "' + title + '"?'))
        return; 
    
    fetch('/lab7/rest-api/films/' + id, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}

function showModal() {
    document.getElementById('description-error').innerText = '';
    document.querySelector('div.modal').style.display = 'block';
    document.querySelector('.modal-backdrop').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
    document.querySelector('.modal-backdrop').style.display = 'none';
}

function cancel() {
    hideModal();
}

function clearForm() {
    document.getElementById('film-id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').innerText = '';
}

function addFilm() {
    clearForm();
    showModal();
}

function editFilm(id) {
    clearForm();
    fetch('/lab7/rest-api/films/' + id)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('film-id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}

function saveFilm() {
    const filmId = document.getElementById('film-id').value;
    const filmData = {
        title_ru: document.getElementById('title-ru').value,
        title: document.getElementById('title').value,
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

    if (!filmData.description || filmData.description.trim() === '') {
        document.getElementById('description-error').innerText = 'Заполните описание';
        return;
    }
    
    let url = '/lab7/rest-api/films/';
    let method = 'POST';
    
    if (filmId !== '') {
        url += filmId;
        method = 'PUT';
    }
    
    document.getElementById('description-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(filmData)
    })
    .then(function(resp) {
        if (resp.ok) {
            hideModal();
            fillFilmList();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors && errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
    });
}
