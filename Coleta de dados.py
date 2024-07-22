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
