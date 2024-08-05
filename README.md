# Analise-de-dados-com-Spotify
 Este repositório contém arquivo jupyter notbook a qual busquei desenvolver conhecimentos adquiridos em projeto de análise de dados. Este projeto contém desde como trabalhar com a API no spotify, até a coleta de dados da mesma, análise exploratório sobre os dados retornados, limpeza de Dataframe gerado com os registros, bem como como disponibilização em formato excel após tratativas e visualizaçoes com intuito de explorar alguns questionamento quanto aos dados.

 Para facilitar entendimento, as etapas executadas no jupyter notbook estarão elencadas abaixo:

## Etapas

1. Acesso a API do spotify é realizada via token, primeiro realizamos solicitação de token passando parâmetros requisitados pelo spotify, estes parâmetros se referem a aplicação criada para utilização de dados no Spotify. Após obter token, é possível acessar os endpoints da API do spotify. Os endpoints dependem do que se deseja buscar, em nosso caso optamos pelo endpoint:https://api.spotify.com/v1/search?q=genre:{genre}&type=track&market={market}&limit={limit}&offset={offset}, a escolha se deu por este endpoint permitir filtrar por gênero, bem como possibilita solicitações de informações adicionais a álbuns, artistas, playlists, faixas, shows, episódios ou audiobooks.

2. Como retorno de requisição de API é em formato JSON, criamos metódo onde realizamos conversão de dicionário para uma lista e então convertemos para formato de Dataframe para que pudéssemos trabalhar utilizando a biblioteca Pandas. Adicionalmente, como desejávamos coletar dados acerca dos três principais mercados do Spotify, requisitamos uma chamada ao endpoint para cada um dos mercados:US,BR,MX(EUA, Brasil, México). Com o retorno, utilizamos função concat da biblioteca Pandas para empilhar e juntar as informações dos 3 dataframes criados.
    
3. Após termos nosso Dataframe, iniciamos processo de análise exploratória, onde buscamos entender nossos dados como um todo, identificando tipos de colunas, registros de linhas, formatação de colunas, registros faltantes, entre outros. Após identificação, realizamos tratativas para estes pontos e geramos arquivo em formato excelc contendo Dataframe tratado.
    
4. Com dados tratados, começamos a responder algumas perguntas, como: Quais são os gêneros de músicas mais populares? e por mercados? Como é o desempenho das músicas do cantor Post Malone nos mercados de Brasil, EUA e México?. Através dessas perguntas, criamos visualizações utilizando as bibliotecas Matplotlib e Seaborn para identificar as respostas.
## Referência

- [Acessando API do Spotify, por Gabril Pastega](https://medium.com/@gabrielpbreis/como-acessar-a-api-do-spotify-com-python-fb9415f29bda)
 - [Endpoint Search for item](https://developer.spotify.com/documentation/web-api/reference/search)


 
