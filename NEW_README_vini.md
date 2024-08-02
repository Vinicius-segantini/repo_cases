### /notebook: 
Dentro da pasta **notebook** temos os arquivos:<br>
1. **Notebook.ipynb** : arquivo extraído do DataBricks e formatado misturando MarkDown com código em PySpark respondendo as 18 perguntas, usando as APIs externas fornecidas.
2. **Notebook.dbc**: arquivo extraído do DataBricks igual o arquivo acima mas no formato *'.dbc'*.
3. **modelo_notebook.ipynb**: arquivo que separa as features e target, treina o modelo, gera algumas métricas e gera o arquivo pickle.
4. **model.pkl**: arquivo pickle com o modelo carregado.

### /src:
Dentro da pasta **src** dois arquivos foram modificados:<br>
1. **database**: gera a classe InMemoryDatabase para simular um banco de dados em memória.
2. **main**: contendo o micro serviço que vai carregar o modelo e contem os endpoints previstos no case.

### /tests:
Contem arquivo **test_integration** em que foram adicionados diversos testes para prever comportamento da API antes de inicializar o container no Docker.

### Arquivos no dir:
1. **model.txt**: arquivo usado para testar uso errado do endpoint */model/load*.
2. **model.pkl**: arquivo .pkl carregado com o modelo.
3. **requirements.txt**: arquivo com requisitos para instalação.
4. **pytest.ini**: facilita importação do 'app' no diretório */tests* para uso do pytest.
5. **Dockerfile**: nesse caso, usado pelo arquivo docker-compose para construir container.
6. **docker-compose**: arquivo usado para construir container.
a. Construir container no Docker desktop: **>** *docker compose -f docker-compose up*

### pytest:
1. Ao rodar o comando: *pytest* diretório do case a expectativa é encontrar 10 testes, sendo:
- 8 normais
- 2 do tipo xfail
