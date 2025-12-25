const API_BASE = '/bank/api';

async function apiCall(method, params = {}) {
    try {
        const response = await fetch(`${API_BASE}/${method}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        
        if (response.status === 401 || response.status === 403) {
            window.location.href = '/bank/login';
            return null;
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Ошибка сервера');
        }
        
        return await response.json();
        
    } catch (error) {
        console.error(`API Error (${method}):`, error);
        throw error;
    }
}

function showNotification(elementId, message, isError = true) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.className = isError ? 'error show' : 'success show';
        
        setTimeout(() => {
            element.className = isError ? 'error' : 'success';
        }, 5000);
    }
}

function showToast(message, isSuccess = true) {
    const toast = document.createElement('div');
    toast.className = isSuccess ? 'success show' : 'error show';
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '10000';
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const login = document.getElementById('login').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!login || !password) {
                showNotification('loginError', 'Заполните все поля');
                return;
            }
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Вход...';
            submitBtn.disabled = true;
            
            try {
                const response = await fetch('/bank/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ login, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    showNotification('loginError', data.error || 'Ошибка авторизации');
                }
                
            } catch (error) {
                console.error('Login error:', error);
                showNotification('loginError', 'Ошибка подключения к серверу');
            } finally {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        });
    }
});

function setupTransferForm() {
    const transferForm = document.getElementById('transferFormElement');
    if (transferForm) {
        transferForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const recipient = document.getElementById('recipient').value.trim();
            const amount = parseFloat(document.getElementById('amount').value);
            
            if (!recipient) {
                showToast('Введите данные получателя', false);
                return;
            }
            
            if (!amount || amount <= 0) {
                showToast('Введите корректную сумму', false);
                return;
            }
            
            try {
                const result = await apiCall('transfer', { recipient, amount });
                if (result) {
                    const balanceEl = document.getElementById('balance');
                    if (balanceEl) {
                        balanceEl.textContent = result.new_balance.toFixed(2);
                    }
                    
                    document.getElementById('transferForm').classList.add('hidden');
                    transferForm.reset();
                    
                    showToast(result.message || '✅ Перевод успешно выполнен', true);
                    
                    loadHistory();
                }
            } catch (error) {
                showToast(error.message || 'Ошибка перевода', false);
            }
        });
    }
}

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history`);
        
        if (response.status === 401) {
            window.location.href = '/bank/login';
            return;
        }
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки истории');
        }
        
        const history = await response.json();
        const historyList = document.getElementById('historyList');
        
        if (historyList && Array.isArray(history)) {
            if (history.length === 0) {
                historyList.innerHTML = '<div class="history-item"><em>История операций пуста</em></div>';
            } else {
                historyList.innerHTML = history.map(t => `
                    <div class="history-item">
                        <div>
                            <strong>${new Date(t.date).toLocaleString('ru-RU')}</strong><br>
                            <small>${t.from_user} → ${t.to_user}</small>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: ${t.type === 'incoming' ? '#28a745' : '#dc3545'}; font-weight: bold;">
                                ${t.type === 'incoming' ? '+' : '-'}${parseFloat(t.amount).toFixed(2)} ₽
                            </span><br>
                            <small>${t.type === 'incoming' ? 'Входящий' : 'Исходящий'}</small>
                        </div>
                    </div>
                `).join('');
            }
            
            document.getElementById('historySection').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error loading history:', error);
        showToast('Ошибка загрузки истории операций', false);
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/users`);
        
        if (response.status === 403) {
            showToast('Доступ запрещен. Требуются права менеджера.', false);
            return;
        }
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки пользователей');
        }
        
        const users = await response.json();
        const usersList = document.getElementById('usersList');
        
        if (usersList && Array.isArray(users)) {
            if (users.length === 0) {
                usersList.innerHTML = '<div class="user-item"><em>Нет пользователей</em></div>';
            } else {
                usersList.innerHTML = users.map(u => `
                    <div class="user-item ${u.is_manager ? 'manager' : ''}">
                        <div>
                            <strong>${u.full_name}</strong><br>
                            <small>Логин: ${u.login} | Счёт: ${u.account_number}</small><br>
                            <small>Телефон: ${u.phone || 'не указан'}</small>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: bold; color: ${u.balance >= 0 ? '#28a745' : '#dc3545'}">
                                ${parseFloat(u.balance).toFixed(2)} ₽
                            </div>
                            <div style="margin-top: 5px;">
                                ${u.is_manager ? '<span class="badge">👨‍💼 Менеджер</span>' : '<span class="badge">👤 Клиент</span>'}
                            </div>
                            <button class="btn btn-danger btn-sm" onclick="deleteUser(${u.id})" style="margin-top: 5px;">
                                Удалить
                            </button>
                        </div>
                    </div>
                `).join('');
            }
            
            document.getElementById('usersSection').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error loading users:', error);
        showToast('Ошибка загрузки списка пользователей', false);
    }
}

async function deleteUser(userId) {
    if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) {
        return;
    }
    
    try {
        const result = await apiCall('users', { id: userId });
        if (result) {
            showToast(result.message || '✅ Пользователь удален', true);
            loadUsers();
        }
    } catch (error) {
        showToast(error.message || 'Ошибка удаления пользователя', false);
    }
}

function setupCreateUserForm() {
    const createUserForm = document.getElementById('createUserFormElement');
    if (createUserForm) {
        createUserForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                full_name: formData.get('full_name').trim(),
                login: formData.get('login').trim(),
                password: formData.get('password'),
                phone: formData.get('phone').trim(),
                is_manager: formData.get('is_manager') === 'on'
            };
            
            if (!data.full_name || !data.login || !data.password) {
                showToast('Заполните обязательные поля', false);
                return;
            }
            
            try {
                const result = await apiCall('users', data);
                if (result) {
                    showToast(result.message || '✅ Пользователь создан', true);
                    this.reset();
                    loadUsers();
                }
            } catch (error) {
                showToast(error.message || 'Ошибка создания пользователя', false);
            }
        });
    }
}

function showTransferForm() {
    document.getElementById('transferForm').classList.remove('hidden');
    document.getElementById('recipient').focus();
}

function hideTransferForm() {
    document.getElementById('transferForm').classList.add('hidden');
    document.getElementById('transferFormElement').reset();
}

function hideHistory() {
    document.getElementById('historySection').classList.add('hidden');
}

function showCreateUserForm() {
    document.getElementById('createUserForm').classList.remove('hidden');
}

function hideCreateUserForm() {
    document.getElementById('createUserForm').classList.add('hidden');
    document.getElementById('createUserFormElement').reset();
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Банковская система загружена');
    
    setupTransferForm();
    setupCreateUserForm();
    
    const style = document.createElement('style');
    style.textContent = `
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            background: #6c757d;
            color: white;
            border-radius: 4px;
        }
        .text-success { color: #28a745; }
        .text-danger { color: #dc3545; }
    `;
    document.head.appendChild(style);
});