# 1 - bibliotecas
import json
import pytest       # engine / framework de teste de unidade
import requests

from utils.utils import ler_csv     # framework de teste de API

# 2 - classe (opcional no Python, em muitos casos)

# 2.1 - atributos ou variaveis
# consulta e resultado esperado
pet_id = 602740501          # codigo do animal
pet_name = "Magnum"               # nome do animal
pet_category_id = 1         # codigo da categoria do animal
pet_category_name = "dog"   # titulo da categoria
pet_tag_id = 1              # codigo
pet_tag_name = "vacinado"   # titulo de rotulo
pet_status = "available"    #satatus do animal

# informações em comum
url = 'https://petstore.swagger.io/v2/pet'          # endereço
headers = { 'Content-Type': 'application/json' }    # formato dos dados trafegados

# 2.2 - funções / métodos

def test_post_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet1.json')           # abre o arquivo json
    data=json.loads(pet.read())                 # ler o conteudo e carrega como json em uma variavel data
    # dados de saída / resultado esperado estão nos atributos acima das funçǒes
    
    # executa
    response = requests.post(       # executa o metodo post com as informacoes a seguir
        url=url,                    # endereco
        headers=headers,            # cabecalho / informacoes extras da mensagem
        data=json.dumps(data),      # a mensagem = json
        timeout=5                   # tempo limite da transmissao, em segundos
    )

    # valida
    response_body = response.json()       # cria uma variavel e carrega a resposta em formato json

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name

def test_get_pet():
    # Dados de Entrada e Saida / Resultado esperado estão na seção de atributos antes das funcoes

    response = requests.get(
        url=f'{url}/{pet_id}',    # chama o endereço do get/consulta passando o código do animal
        headers=headers
        # não tem corpo
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id    
    assert response_body['status'] == 'available'

def test_put_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet2.json')           # abre o arquivo json
    data=json.loads(pet.read())                 # ler o conteudo e carrega como json em uma variavel data
    # dados de saída / resultado esperado estão nos atributos acima das funçǒes
    
    # executa
    response = requests.put(       # executa o metodo put com as informacoes a seguir
        url=url,                    # endereco
        headers=headers,            # cabecalho / informacoes extras da mensagem
        data=json.dumps(data),      # a mensagem = json
        timeout=5                   # tempo limite da transmissao, em segundos
    ) 

    # valida
    response_body = response.json()       # cria uma variavel e carrega a resposta em formato json

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['status'] == 'sold'

def test_delete_pet():
    # Configura
    # Dados de entrada e saída virão dos atributos

    # Executa
    response = requests.delete(
        url=f'{url}/{pet_id}',
        headers=headers
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)


@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv'))
def test_post_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):
    # Configura
    pet = {}        # cria uma lista vazia chamada pet
    pet['id'] = int(pet_id)
    pet['category'] = {}
    pet['category']['id'] = int(category_id)
    pet['category']['name'] = category_name
    pet['name'] = pet_name
    pet['photoUrls'] = []
    pet['photoUrls'].append('')
    pet['tags'] = []

    tags = tags.split(';')
    for tag in tags:
        tag = tag.split('-')
        tag_formatada = {}
        tag_formatada['id'] = int(tag[0])
        tag_formatada['name'] = tag[1]
        pet['tags'].append(tag_formatada)

    pet['status'] = status

    pet = json.dumps(obj=pet, indent=4)
    print('\n' + pet)                       # visualiza como ficou o json criado dinamicamente

    # Executa
    response = requests.post(
        url=url,
        headers=headers,
        data=pet,
        timeout=5
    )
    # Compara
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == int(pet_id)
    assert response_body['name'] == pet_name
    assert response_body['status'] == status


    # Other operations dynamically
@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv'))
def test_get_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):

    tags = tags.split(';')

    # Executa
    response = requests.get(
        url=f'{url}/{pet_id}',
        headers=headers
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['category']['id'] == int(category_id)
    assert response_body['name'] == pet_name
    # assert response_body['tags'][0]['id'] == int(tag[0])        # to investigate
    for x in range(len(tags)):
        tag = tags[x]
        tag = tag.split("-")
        assert response_body['tags'][x]['id'] == int(tag[0])
        assert response_body['tags'][x]['name'] == tag[1]
    assert response_body['status'] == status

# @pytest.mark.parametrize('id, category_id, category_name, name, photoUrls, tags, status', 
#                          ler_csv('./fixtures/csv/massaPet.csv'))
# def test_get_pet_dinamico2(id, category_id, category_name, name, photoUrls, tags, status):

#     tags = tags.split(';')
#     tags_separadas = []
#     for tag in tags:
#         tags_separadas.append(tag.split('-'))

#     response = requests.get(
#         url=f'{url}/{pet_id}',
#         headers=headers,
#     )
#     response_body = response.json()

#     assert response.status_code == 200
#     assert response_body['id'] == int(id)
#     assert response_body['name'] == name

#     for x in range(len(tags)):
#         assert response_body['tags'][x]['id'] == int(tags_separadas[x][0])
#         assert response_body['tags'][x]['name'] == tags_separadas[x][1]

@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv'))
def test_put_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):
    # Configura
    pet = {}   
    pet['id'] = int(pet_id)
    pet['category'] = {}
    pet['category']['id'] = int(category_id)
    pet['category']['name'] = category_name
    pet['name'] = pet_name
    pet['photoUrls'] = []
    pet['photoUrls'].append('')
    pet['tags'] = []

    tags = tags.split(';')
    for tag in tags:
        tag = tag.split('-')
        tag_formatada = {}
        tag_formatada['id'] = int(tag[0])
        tag_formatada['name'] = tag[1]
        pet['tags'].append(tag_formatada)

    pet['status'] = 'sold'

    pet = json.dumps(obj=pet, indent=4)
    print('\n' + pet)                

    # Executa
    response = requests.put(
        url=url,
        headers=headers,
        data=pet,
        timeout=5
    )

    # Compara
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == int(pet_id)
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == int(category_id)
    assert response_body['category']['name'] == category_name
    for x in range(len(tags)):
        tag = tags[x]
        tag = tag.split("-")
        assert response_body['tags'][x]['id'] == int(tag[0])
        assert response_body['tags'][x]['name'] == tag[1]
    assert response_body['status'] == 'sold'

@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv'))
def test_delete_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):

    # Executa
    response = requests.delete(
        url=f'{url}/{pet_id}',
        headers=headers,
        timeout=5
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)