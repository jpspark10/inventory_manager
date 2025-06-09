def test_register_and_login(client, app):
    # Регистрация
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'password': 'newpass',
        'confirm_password': 'newpass'
    }, follow_redirects=True)
    assert b'Registration successful' in response.data

    # Вход
    response = client.post('/auth/login', data={
        'username': 'newuser',
        'password': 'newpass'
    }, follow_redirects=True)
    assert b'Item' in response.data  # редирект на список предметов
