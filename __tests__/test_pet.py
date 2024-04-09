# 1 - bibliotecas
import json
import pytest       # engine / framework de teste de unidade
import requests     # framework de teste de API

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
    assert response_body['status'] == pet_status