import json

import pytest
import requests

from utils.utils import ler_csv


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

# 1 - Incluir, consultar, alterar e excluir um usuário, 
# sempre com o teste do Status Code e pelo menos 3 testes de campos do retorno.
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


# 3 - Altere a função Post e Delete da entidade User 
# para que executem os testes a partir de uma massa com json dinamico
@pytest.mark.parametrize('user_id,username,first_name,last_name,email,password,phone,user_status',
                         ler_csv('./fixtures/csv/user.csv'))
def test_post_user_dinamico(user_id,username,first_name,last_name,email,password,phone,user_status):

    # Configura
    user = {}  
    user['id'] = user_id
    user['username'] = username
    user['firstName'] = first_name
    user['lastName'] = last_name
    user['email'] = email
    user['password'] = password
    user['phone'] = phone
    user['userStatus'] = user_status

    user = json.dumps(obj=user, indent=4)
    print('\n' + user)                       # visualiza como ficou o json criado dinamicamente

    # Executa
    response = requests.post(
        url=url,
        headers=headers,
        data=user,
        timeout=5
    )
    # Compara
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == "unknown"
    assert response_body['message'] == str(user_id)

@pytest.mark.parametrize('user_id,username,first_name,last_name,email,password,phone,user_status',
                         ler_csv('./fixtures/csv/user.csv'))
def test_get_user_dinamico(user_id,username,first_name,last_name,email,password,phone,user_status):

    # Executa
    response = requests.get(
        url=f'{url}/{username}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == int(user_id)
    assert response_body['username'] == username 
    assert response_body['firstName'] == first_name
    assert response_body['lastName'] == last_name
    assert response_body['email'] == email
    assert response_body['password'] == password
    assert response_body['phone'] == phone
    assert response_body['userStatus'] == int(user_status)

@pytest.mark.parametrize('user_id,username,first_name,last_name,email,password,phone,user_status',
                         ler_csv('./fixtures/csv/user.csv'))
def test_put_user_dinamico(user_id,username,first_name,last_name,email,password,phone,user_status):

    # Configura
    user = {}  
    user['id'] = user_id
    user['username'] = username
    user['firstName'] = first_name
    user['lastName'] = last_name
    user['email'] = email
    user['password'] = password
    user['phone'] = phone
    user['userStatus'] = '0'

    user = json.dumps(obj=user, indent=4)
    print('\n' + user)                       # visualiza como ficou o json criado dinamicamente

    # Executa
    response = requests.put(
        url=f'{url}/{username}',
        headers=headers,
        data=user,
        timeout=5
    )
    # Compara
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == "unknown"
    assert response_body['message'] == str(user_id)

@pytest.mark.parametrize('user_id,username,first_name,last_name,email,password,phone,user_status',
                         ler_csv('./fixtures/csv/user.csv'))
def test_delete_user_dinamico(user_id,username,first_name,last_name,email,password,phone,user_status):

    # Executa
    response = requests.delete(
        url=f'{url}/{username}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == "unknown"
    assert response_body['message'] == username