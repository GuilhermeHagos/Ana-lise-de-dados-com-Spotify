# %%
##import spotipy
##import spotipy.util as util
##from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import base64

# %%

# Adicionando credenciais de app do Spotify para solicitar token de acesso a API
# Inserir informações de acordo com app criado no Spotify
client_id = '5f229361801a4b62a9cf37e0ae65c5a2'
client_secret = '4691930e87594fa78f3f55b68620e16e'



# %%
# codiificar credenciais em base 64
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
# %%

#Headers e dados a serem passados na solicitação

headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'client_credentials'
}
# %%
# enviando solicitação via POST
response = requests.post('https://accounts.spotify.com/api/token',headers = headers,data = data)

# %%
if response.status_code ==200:
    token_info = response.json()
    access_token = token_info['access_token']
    print(f'Access Token: {access_token}')
else:
    print(f"Failed to retrieve access token: {response.status_code}")
    print(response.json())
# %%

##criando função para realziar chamada a API, recebe url ( endpoint que estamos acessando) e token de acesso como parâmetros
def api_call(url, access_token):
    """
    Chama a API do Spotify usando um endpoint de URL e um token de acesso para recuperar dados no formato JSON.

    Args:
        url (str): Endpoint de URL para acessar dados de faixas disponíveis.
            URL padrão fornecida - https://api.spotify.com/v1/search?q=genre:{genre}&type=track&market={market}&limit={limit}&offset={offset}
        
        access_token (str): Token de acesso à API do Spotify fornecido com o uso da função get_token.

    Returns:
        dict: Objeto JSON com a resposta da API.
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers= headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Chamada a API falhou:{response.status_code}')
        return response.json()
    
    

# %%

#realizando chamada a endpoint que retorna generos e informações acerca de album, traks, shows etc
url = 'https://api.spotify.com/v1/search?q=genre:rock&type=track&market=BR&limit=20&offset=0'
api_response = api_call(url, access_token)
api_response

# %%
api_response.keys()
# %%
api_response['tracks']
# %%
api_response['tracks'].keys()
# %%
##na Key itens é onde podemos observar os dados relacionados a faixas
api_response['tracks']['items'][0].keys()
# %%
## é possíel acessar as musicas de albuns acessando a chave items e passando indice de musica
api_response['tracks']['items'][0]
# %%

## Podemos selecionar alguns dados para análise, filtraremos alguns dados
## Popularidade de genêros ao longo dos anos
api_response['tracks']['items'][0]['id']

# %%
# Os acessos são dados através da entrada na lista e percorrendo os indices e as chaves que queremos acessar, como abaixo onde acessamos as informacoes da Banda
api_response['tracks']['items'][0]['artists'][0].keys()
# %%
#  abaixo onde acessamos o ID da banda
api_response['tracks']['items'][0]['artists'][0]['id']

# %%
#acessando id de primeira musica
api_response['tracks']['items'][0]['id']
# %%
api_response['tracks']['items'][0].keys()
# %%
## Nome da primeira musica
api_response['tracks']['items'][0]['name']

# %%
## Duração da primeira música em milisegundos
duracao = api_response['tracks']['items'][0]['duration_ms']
# %%
## Como resultado vem em milisegundos, abaixo segue operaçao para encontrar em minutos
musica_minutos = (duracao // 1000) //60 
print( str(musica_minutos) + ' ' + 'Minutos')
# %%
## Nome do artista do primeiro item
api_response['tracks']['items'][0]['artists'][0]['name']
# %%
##Nome do album da primeira música
api_response['tracks']['items'][0]['album']['name']
# %%
