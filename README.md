# Projeto ETL utilizando a plataforma Sympla

Este projeto tem como objetivo criar uma pipeline de dados, para que ocorra a integração e o armazenamento de informações provenientes da plataforma *Sympla*. Tendo em vista um MVP, no qual apenas se consomem dados de eventos criados na plataforma, o objetivo principal é fornecer escalabilidade para futuras implementações, além de garantir o tratamento e a normalização dos dados, versionamento e rastreabilidade.

## Funcionalidades  
- Possui uma página *home* estilizada e intuitiva, sendo possível utilizar uma chave de API própria ou uma pré-definida, além de poder definir quantos objetos quer consumir da *API* do sympla e sua página.  
- Possui um sistema de navegação entre páginas de forma fácil.  
- Possui uma página de listagem, na qual mostra os eventos importados e sua carga específica (permitindo um histórico de importações).  
- Possui regras que não permitem salvar dados já existentes no banco de dados, porém só serão salvos novamente caso esses dados sejam alterados de alguma forma, ficando em uma carga diferente da sua primeira versão.  
- Possui uma *API* que permite acessar dados salvos no banco de dados, disponibilizando *query params* para filtragem e paginação.  
- Possui a documentação da *API* feita no Swagger, que permite entendê-la e utilizá-la de forma intuitiva. Além disso, é acessível pelo front-end sem muita burocracia.  

## Tecnologias Utilizadas
- Python
- Django
- Django Rest Framework
- Docker
- Docker Compose
- PostegreSQL
- Swagger
- HTML
- CSS (Bootstrap)

## Documentação
- 👉 [decisões técnicas](https://github.com/ThomasNicholas21/ProjetoSympla/blob/main/docs/tecnical_decision/tecnical.md)
- 👉 [desafios encontrados](https://github.com/ThomasNicholas21/ProjetoSympla/blob/main/docs/challenges/challenge.md)
- 👉 [estrutura da pipeline](https://github.com/ThomasNicholas21/ProjetoSympla/blob/main/docs/pipeline_structure/pipeline.md)
- 👉 [modelagem de dados](https://github.com/ThomasNicholas21/ProjetoSympla/blob/main/docs/data_modeling/model.md)
- 👉 [futura implementações](https://github.com/ThomasNicholas21/ProjetoSympla/blob/main/docs/future_implementations/future.md)

## Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/ThomasNicholas21/ProjetoSympla.git
```

### 2. Configurar Arquivo `.env`
Crie um arquivo `.env` na raiz do projeto e defina as variáveis necessárias, siga o exemplo do .env-example:
```txt
SECRET_KEY="CHANGE-ME"

# 0 False, 1 True
DEBUG="1"

# Comma Separated values
ALLOWED_HOSTS="127.0.0.1, localhost"

DB_ENGINE="django.db.backends.postgresql"
POSTGRES_DB="CHANGE-ME"
POSTGRES_USER="CHANGE-ME"
POSTGRES_PASSWORD="CHANGE-ME"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
```
👉 [.env-example](https://github.com/ThomasNicholas21/ProjetoSympla/blob/main/dotenv_files/.env-example)

**Dica**: caso não tenha um *SECRET_KEY* para colocar, utilize o seguinte comando no seu *prompt*:
```cmd
# python -c "import string as s;from random import SystemRandom as sr;print(''.join(sr().choices(s.ascii_letters + s.punctuation, k=64)))"
```
Lembre-se de retirar aspas de dentro da chave, para que não haja conflito.

### 3. Construir e Subir os Containers
```bash
docker-compose up --build
```

### 4. Criar Superusuário
```bash
docker-compose run --rm app_sympla python manage.py createsuperuser
```

### 5. Acessar a Aplicação
- **Frontend**: `http://localhost:8000`
- **Admin**: `http://localhost:8000/admin`

## Como executar testes
```bash
docker-compose run --rm app_sympla python manage.py tests
```

## Autor
Projeto desenvolvido por **Thomas Nicholas**.

