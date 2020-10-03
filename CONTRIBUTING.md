# Contribuindo com DojoPuzzles

Sua contribuição é muito bem vinda! Você pode colaborar com o projeto de várias formas:

- [Reportando um bug](/issues)
- [Dando ideia de novas funcionalidades](/issues)
- [Enviando Pull Requests que corrijam bugs ou implementem novas funcionalidades](/pull-requests)
- [Enviando novos problemas para Dojos](http://dojopuzzles.com/contribuicoes/contribua)

## Rodando o projeto localmente

Este projeto é implementado usando [Django](https://docs.djangoproject.com/pt-br) e Python.

Para poder trabalhar em bugs e novas funcionalidades, você provavelmente vai querer rodar o projeto na sua máquina, para poder testar as alterações.

Depois de criar um "fork" do projeto em sua conta GitHub e baixar o código localmente, siga os passos a seguir para rodar o projeto localmente:

- Crie e ative um ambiente virtual para o Django

```bash
python3 -m venv venv
source venv/bin/activate
```

- Instale os requerimentos do projeto

```bash
pip install -r requirements.txt
```

- Rode as migrações do banco de dados de dentro do diretório dojopuzzles, e crie o usuário administrador do projeto

```bash
cd dojopuzzles
python manage.py makemigrations
python manage.py createsuperuser
```

Lembre o nome de usuário e senha que você fornecer para o último comando, você vai usá-lo para acessar a tela de administração do projeto.

Agora, basta iniciar o projeto!

```bash
> python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 02, 2020 - 21:25:57
Django version 3.1, using settings 'dojopuzzles.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

A tela de administração vai estar disponível em http://127.0.0.1:8000/admin, e a interface do usuário em http://127.0.0.1:8000/home.

Como o banco de dados de problemas vai estar vazio, você provavelmente vai querer adicionar um problema em http://127.0.0.1:8000/admin/problems/problem/

## Rodando os testes unitários

Para garantir que suas colaborações não vão quebrar nenhum código existente, e também que elas continuarão funcionando à medida que o código evolui, é imporante criar testes unitários e também rodar todos os testes existentes.

Para tanto basta rodar o seguinte comando de dentro do diretório dojopuzzles:

```bash
python manage.py test
```

Se tudo estiver bem, você verá ao fim um resultado mais ou menos assim:

```bash
----------------------------------------------------------------------
Ran 24 tests in 0.083s

OK
Destroying test database for alias 'default'...
```

Se por outro lado algum teste quebrar, você verá algo como o resultado abaixo. Note que o nome do teste que falhou é indicado, basta encontrá-lo no código e ver o que aconteceu

```bash
----------------------------------------------------------------------
FAIL: test_formatting_description_field (problems.tests.test_views.ProblemViewTestCase)
----------------------------------------------------------------------

AssertionError: 'b' != 'a'

----------------------------------------------------------------------
Ran 24 tests in 0.078s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

## Licença

Ao contribuir, você concorda que a mesma licença do projeto [(MIT)](./LICENSE) será mantida em sua contribuição. Em caso de dúvida por favor entre em contato com os mantenedores do projeto.
