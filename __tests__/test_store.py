import datetime
import json

import pytest
import requests


store_id = 9223372036854775000
pet_id = 602740501
quantity = 1
ship_date = "2024-04-15T20:03:30.641+0000"                  ## Investigate datetime.date.today()
status = "placed"
complete = True


# informações em comum
url = 'https://petstore.swagger.io/v2/store/order'          # endereço
headers = { 'Content-Type': 'application/json' } 


# 2 - Incluir, consultar e excluir um pedido de compra, 
# sempre com o teste do Status Code e pelo menos 3 testes de campos do retorno.
def test_post_store_order():

    store=open('./fixtures/json/store.json')
    data=json.loads(store.read()) 

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == store_id
    assert response_body['petId'] == pet_id
    assert response_body['quantity'] == quantity
    assert response_body['shipDate'] == ship_date
    assert response_body['status'] == status
    assert response_body['complete'] == complete


def test_get_store_order():

    response = requests.get(
        url=f'{url}/{store_id}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == store_id
    assert response_body['quantity'] == quantity 
    assert response_body['status'] == status
    assert response_body['complete'] == complete

# @pytest.mark.slow
def test_delete_store_order():
    # Executa
    response = requests.delete(
        url=f'{url}/{store_id}',
        headers=headers
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(store_id)