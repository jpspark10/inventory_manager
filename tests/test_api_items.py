def test_add_and_get_item(logged_in_client, app):
    # Добавляем предмет
    response = logged_in_client.post('/api/items/', json={
        'name': 'Test Item',
        'description': 'This is a test'
    })
    assert response.status_code == 201
    item_id = response.get_json()['id']

    # Получаем список предметов
    response = logged_in_client.get('/api/items/')
    assert response.status_code == 200
    items = response.get_json()
    assert any(item['id'] == item_id for item in items)


def test_delete_item(logged_in_client, app):
    # Создание предмета
    response = logged_in_client.post('/api/items/', json={
        'name': 'To be deleted',
        'description': ''
    })
    item_id = response.get_json()['id']

    # Удаление предмета
    response = logged_in_client.delete(f'/api/items/{item_id}')
    assert response.status_code == 204

    # Проверка отсутствия
    response = logged_in_client.get('/api/items/')
    assert all(item['id'] != item_id for item in response.get_json())
