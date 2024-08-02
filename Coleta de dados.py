# %%
##import spotipy
##import spotipy.util as util
##from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import base64
import seaborn as sns
import matplotlib.pyplot as plt

# %%

# Adicionando credenciais de app do Spotify para solicitar token de acesso a API
# Inserir informações de acordo com app criado no Spotify
client_id = 'INSIRA CLIENT ID'
client_secret = 'INSIRA CLIENT SECRET'



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
market = 'BR'
genre = 'rock'
limit = 5
offset = 0
url = f'https://api.spotify.com/v1/search?q=genre:{genre}&type=track&market={market}&limit={limit}&offset={offset}'
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
api_response['tracks']['items'][0]['album'].keys()
# %%
#data de lançamento do album do primeiro item
api_response['tracks']['items'][0]['album']['release_date']
# %%
#Popularidade da música do item 1
api_response['tracks']['items'][0]['popularity']
# %%
#Abaixo, filtraremos os dados que queremos selecionar e criaremos um dataframe
track_id = api_response['tracks']['items'][0]['id']
track_name = api_response['tracks']['items'][0]['name']
# ajustando valor retornado de milisegundos para minutos, como lambda nao aceita receber dictionary, criamos uma variavel que recebe retorno da API e passamos essa variael na função lambda
duration_ms = api_response['tracks']['items'][0]['duration_ms']
track_duration = lambda duration_ms : (duration_ms // 1000) // 60
duration_in_minutes = track_duration(duration_ms)
artist_name = api_response['tracks']['items'][0]['artists'][0]['name']
album_name = api_response['tracks']['items'][0]['album']['name']
album_release_date = api_response['tracks']['items'][0]['album']['release_date']
popularity = api_response['tracks']['items'][0]['popularity']
genre = 'rock'

#Criando Dataframe

track_df = pd.DataFrame(
    {
    'track_id': [track_id],
    'track_name': [track_name],
    'track_duration_ms':[duration_in_minutes],
    'artist_name': [artist_name],
    'album_name': [album_name],
    'album_release_date': [album_release_date],
    'popularity': [popularity],
    'genre': [genre]
    }
)




# %%
print(f'Dataframe possui{track_df.shape[1]} colunas')
track_df

# %%
# Para inserir todos os registros de músicas, faremos uma iteraçao sobre os registros, passando valor iteravel na chamadaa a API no api_response
# Após investigar problema referente a solicitar itens de vários generos, foi descoberto que o índice de um item na resposta da API é perdido quando um gênero possui faixas insuficientes para o valor máximo solicitado.
# Para resolver esse problema, foi implementado um comando "break" no código quando o número de itens é abaixo do limite ou igual a zero. Isso garante que cada lote de dados contenha 50 faixas. Além disso, nesta última interação da função, a variável "markets" foi adicionada para trazer dados de mais de um mercado.
def tracks_dataset(genres, markets, limit, offset, pages, access_token):
    """
    Recupera dados de faixas da API do Spotify com base nos gêneros especificados, parâmetros de paginação e token de acesso.

    Args:
        genres (list): Uma lista de nomes de gêneros para os quais as faixas precisam ser obtidas da API do Spotify.
        markets (list): Uma lista de códigos de país para os mercados disponíveis no Spotify (valor de acordo com o código de país ISO 3166-1 alpha-2).
        limit (int): O número máximo de faixas a serem obtidas por requisição à API.
        offset (int): O offset inicial para paginação para obter faixas da API.
        pages (int): O número de páginas da API a serem buscadas para cada gênero.
        access_token (str): O token de acesso necessário para autenticação com a API do Spotify.

    Returns:
        pandas.DataFrame: Um DataFrame do pandas contendo as informações das faixas extraídas, incluindo ID da faixa,
        nome da faixa, duração, nome do artista, nome do álbum, data de lançamento do álbum, popularidade e gênero.

    Funcionalidades:
        - Itera pelos gêneros e páginas de paginação especificados para obter dados de faixas da API do Spotify.
        - Extrai informações relevantes da resposta da API.
        - Combina os dados extraídos em um DataFrame do pandas e retorna o DataFrame ao chamador.

    Observações:
        - A função faz várias chamadas à API com base nos gêneros e na paginação, processando os dados em um DataFrame.
        - Usa o formato de URL do endpoint da API fornecido com espaços reservados para gênero, limite e offset.
        - Assume a existência de uma função 'api_call' para fazer requisições à API.
        - Requer o manuseio adequado do token de acesso usando a função 'get_token' ou um mecanismo semelhante.
    """

    offset_counter = offset
    track_df = []
    
    for market in markets:
        for genre in genres:  
            for page in range(pages):    
                url = f'https://api.spotify.com/v1/search?q=genre:{genre}&type=track&market={market}&limit={limit}&offset={offset}'
                api_response = api_call(url, access_token)
                num_items = len(api_response['tracks']['items'])

                if num_items == 0:
                    break

                for i in range(num_items):
                    track_id = api_response['tracks']['items'][i]['id']
                    track_name = api_response['tracks']['items'][i]['name']
                    track_duration_ms = api_response['tracks']['items'][i]['duration_ms']
                    artist_name = api_response['tracks']['items'][i]['artists'][0]['name']
                    album_name = api_response['tracks']['items'][i]['album']['name']
                    album_release_date = api_response['tracks']['items'][i]['album']['release_date']
                    popularity = api_response['tracks']['items'][i]['popularity']
                    genre = genre
                    market = market

                    track_df.append({
                        'track_id': track_id,
                        'track_name': track_name,
                        'track_duration_ms': track_duration_ms,
                        'artist_name': artist_name,
                        'album_name': album_name,
                        'album_release_date': album_release_date,
                        'popularity': popularity,
                        'genre': genre,
                        'market': market
                    })

                offset += limit

                if num_items < limit:
                    break

            offset = offset_counter

        tracks_dataset = pd.DataFrame(track_df)    
        return tracks_dataset



# %%
genres = ['alt-rock', 'alternative', 'brazil', 'blues', 'electro', 'heavy-metal', 'hip-hop', 'house', 'jazz', 'pop', 'reggae', 'rock', 'soul', 'techno', 'trance'] 
markets = ['BR']
limit = 50
offset = 0
pages = 20
access_token = access_token
# %%
tracks_df_BR = tracks_dataset(genres, markets,limit,offset,pages,access_token)
# %%
print(f'Este dataset possui {tracks_df_BR.shape[0]} linhas e {tracks_df_BR.shape[1]} colunas ')
# %%
tracks_df_BR.head()
# %%
#exportando Dataframe para CSV
tracks_df_BR.to_csv('spotify_dataset.csv')
# %%
tracks_df_BR.dtypes
# %%
# iremos alterar coluna'album_release_date' para um objeto de data e hora.
tracks_df_BR['album_release_date'] = pd.to_datetime(tracks_df_BR['album_release_date'], format='mixed')
# %%
tracks_df_BR.dtypes
# %%
tracks_df_BR.to_csv('spotify_dataset.csv')
# %%
# Para fins de análise, coletaremos dados referentes a outros mercados. A comparaçao será feita entre os 3 maiores países em streams, EUA, Brasil e México
#US
tracks_df_US = tracks_dataset(genres, ['US'],limit,offset,pages,access_token)

# %%
tracks_df_US.head()

# %%
# Mexico
tracks_df_MX = tracks_dataset(genres, ['MX'],limit,offset,pages,access_token)
tracks_df_MX.head()
# %%
tracks_df_US.shape
# %%
## Utilaremos o metódo concat do Pandas, pois com ele é possível empilhar linhas de diferentes dataframes se as colunas forem as mesmas
tracks_concat = pd.concat([tracks_df_BR,tracks_df_US,tracks_df_MX], ignore_index= True)
# %%
tracks_concat.shape
# %%
print(f'Este dataset possui {tracks_concat.shape[0]} linhas e {tracks_concat.shape[1]} colunas ')
# %%
tracks_concat
# %%
tracks_concat.to_csv('spotify_dataset_BR_US_MX.csv')
# %%
tracks_sorted= tracks_concat[['track_name','artist_name','album_release_date','genre','market','popularity']].sort_values(by='popularity', ascending=False)

# %%
tracks_sorted
# %%
tracks_sorted.sort_values(by='market', ascending=True)
# %%
# Para descobrir os dados referente a um unico cantor, como por exemplo Post Malone, realizamos filtro abaixco
post_tracks = tracks_concat[tracks_concat['artist_name'] == 'Post Malone']

post_tracks
# %%
# Filtramos as musicas mais populares do momento de Post Malone em cada Mercado. Vale dizer que o atributo popularity se refere a apenas um recorte do momento, ele é um dado atual

Post_tracks_sorted = post_tracks.sort_values(by=['market','popularity'], ascending= False)
Post_tracks_sorted
# %%
all_tracks_sorted_by_popularity_market = tracks_concat.sort_values(by=['market','popularity'], ascending=[True,False])
all_tracks_sorted_by_popularity_market.head(20)
# %%
#Durante análise dos dados do dataframe, observamos alguns campos vazios, como eram poucos, realizamos dropna nesses valores
df = pd.read_excel('spotify_dataset_BR_US_MX.xlsx')
df.isnull().sum()

# %%
df.dropna(inplace=True)
# %%
df.isnull().sum()
# %%
df.to_excel('cleaned_spotify_dataset_BR_US_MX.xlsx')
df.head()
# %%
df_cleaned = pd.read_excel('cleaned_spotify_dataset_BR_US_MX.xlsx')
df_cleaned['popularity'].hist(bins=20)
# %%
## Média de popularidade por gênero
popularity_by_genre = df_cleaned.groupby('genre')['popularity'].mean()
popularity_by_genre.plot()
# %%
#média de popularidade de genero por mercado 
popularity_by_market_by_genre = df.groupby(['market','genre'])['popularity'].mean().reset_index()


plt.figure(figsize=(14, 8))
sns.barplot(x='genre', y='popularity', hue='market', data=popularity_by_market_by_genre)
plt.title('Popularidade Média por Gênero e Mercado')
plt.xlabel('Gênero')
plt.ylabel('Popularidade Média')
plt.legend(title='Mercado', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.show()


# %%
#artistas mais populares
df_artists_popularity = df.groupby('artist_name')['popularity'].mean().sort_values(ascending=False)
df_artists_popularity
# %%
# artistas mais populares por mercado
df_artists_popularity_by_market = df.groupby(['market','artist_name'])['popularity'].mean().sort_values(ascending=False).reset_index()
df_artists_popularity_by_market
# %%
df['artist_name'] = df['artist_name'].astype(str)



# %%
plt.figure(figsize=(14, 8))
sns.barplot(x='popularity', y='artist_name', hue='market', data=df_artists_popularity_by_market, dodge=False)
plt.title('Popularidade Média por Artista e Mercado')
plt.xlabel('Popularidade Média')
plt.ylabel('Artista')
plt.legend(title='Mercado', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
# %%

df_top_artists_by_market = df_artists_popularity_by_market.groupby('market').head(10)
# %%
plt.figure(figsize=(14, 8))
sns.barplot(x='popularity', y='artist_name', hue='market', data=df_top_artists_by_market, dodge=True)
plt.title('Popularidade Média por Artista e Mercado')
plt.xlabel('Popularidade Média')
plt.ylabel('Artista')
plt.legend(title='Mercado', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
# %%
df_pivot = df_top_artists_by_market.pivot(index='artist_name', columns='market', values='popularity').head(10)

# Plotar gráfico de barras empilhadas
df_pivot.plot(kind='bar', stacked=True, figsize=(14, 8))
plt.title('Popularidade Média por Artista e Mercado')
plt.xlabel('Artista')
plt.ylabel('Popularidade Média')
plt.legend(title='Mercado')
plt.show()

# %%
