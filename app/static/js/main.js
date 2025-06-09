document.addEventListener('DOMContentLoaded', function() {
    // Закрытие flash-сообщений
    document.querySelectorAll('.alert .close').forEach(function(btn) {
        btn.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // AJAX для удаления предметов без перезагрузки
    document.querySelectorAll('.delete-item-btn').forEach(function(btn) {
        btn.addEventListener('click', function(event) {
            event.preventDefault();
            const itemId = this.dataset.itemId;
            const row = document.getElementById(`item-row-${itemId}`);
            fetch(`/api/items/${itemId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status === 204) {
                    // Удаляем строку из таблицы
                    row.remove();
                } else if (response.status === 403) {
                    alert('Нет прав на удаление этого предмета.');
                } else {
                    alert('Ошибка при удалении.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Не удалось выполнить запрос.');
            });
        });
    });
});