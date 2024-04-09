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
    pet=('./fixtures/json/pet1.json')           # abre o arquivo json
    data=json.loads(pet.read())                 # ler o conteudo e carrega como json em uma variavel data
    # dados de saída / resultado esperado estão nos atributos acima das funçǒes
    
    # executa
    response = requests.post(
        url=url,                    # endereco
        headers=headers,            # cabecalho / informacoes extras da mensagem
        data=json.dumps(data),      # a mensagem = json
        timeout=5                   # tempo limite da transmissao, em segundos
    )



    # valida