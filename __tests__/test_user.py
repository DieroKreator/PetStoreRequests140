import json

import pytest
import requests


user_id = 60814379198
username = "figotti"
first_name = "Fidel"
last_name = "Santos"                  
email = "figotti@gmail.com"
password = "123456"
phone = "51452895685"
user_status = 1

url = 'https://petstore.swagger.io/v2/user'          # endereço
headers = { 'Content-Type': 'application/json' } 

def test_post_user():
    user=open('./fixtures/json/user1.json')
    data=json.loads(user.read()) 

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == "unknown"
    assert response_body['message'] == str(user_id)

def test_get_user():
    response = requests.get(
        url=f'{url}/{username}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == user_id
    assert response_body['username'] == username 
    assert response_body['firstName'] == first_name
    assert response_body['lastName'] == last_name
    assert response_body['email'] == email
    assert response_body['password'] == password
    assert response_body['phone'] == phone
    assert response_body['userStatus'] == user_status

def test_put_user():
    user=open('./fixtures/json/user2.json')
    data=json.loads(user.read()) 

    response = requests.put(
        url=f'{url}/{username}',
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == "unknown"
    assert response_body['message'] == str(user_id)

def test_delete_user():
    response = requests.delete(
        url=f'{url}/{username}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == "unknown"
    assert response_body['message'] == username