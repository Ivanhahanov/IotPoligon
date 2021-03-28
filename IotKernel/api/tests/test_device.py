from . import *

test_device = {
    "name": "test_device",
    "module": "main",
    "description": "Test Device",
    "description_ru": "Устройство",
    "available_commands": [
        "on",
        "off",
    ]
}

short_test_device = {
    "name": "test_device",
    "module": "main",
}

db_test_device = {
    "test_device": {
        "description": "Test Device",
        "description_ru": "Устройство",
        "available_commands": [
            "on",
            "off",
        ]
    }
}


def test_add_device():
    response = client.put('/devices/add', json=test_device)
    assert response.status_code == 200
    assert test_device['name'] in response.json()['main']['devices']


def test_device_info():
    response = client.post('/devices/info', json=short_test_device)
    assert response.status_code == 200
    assert response.json() == db_test_device


def test_device_update():
    updated_device = test_device
    updated_device['available_commands'] = ['open']
    db_updated_device = db_test_device
    db_updated_device['test_device']['available_commands'] = ['open']
    response = client.post('/devices/update', json=updated_device)
    assert response.status_code == 200
    print(response.json())
    assert response.json()['main']['devices']['test_device'] == db_updated_device['test_device']


def test_device_delete():
    response = client.delete('/devices/delete', json=short_test_device)
    assert response.status_code == 200
    assert response.json()['main']['devices'].get('test_device') is None
