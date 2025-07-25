# Decisões técnicas - documentação  

## Tecnologia  

As tecnologias utilizadas foram selecionadas por serem de conhecimento técnico do desenvolvedor e, como o objetivo era entregar uma aplicação robusta e funcional, que fosse escalável de forma rápida, optou-se pela linguagem *Python* e pelas frameworks *Django* e *Django Rest Framework*.  

Além disso, foi utilizado o banco de dados relacional *PostgreSQL* por possuir uma ótima integração com a framework utilizada e também por sua excelente escalabilidade em nível corporativo. Para a configuração do ambiente, foi utilizada a ferramenta *Docker* e *Docker-Compose*, devido à sua praticidade e isolamento de dependências.  

- **Python**: A linguagem é robusta e possui diversas bibliotecas úteis, que auxiliam na criação de pipelines, inteligência artificial, leitura de PDFs, entre outros. Tendo isso em vista, ela foi escolhida devido ao conhecimento técnico do desenvolvedor e às suas funcionalidades. Neste projeto, foram utilizadas as seguintes bibliotecas:  
    - **requests**: Essa biblioteca permite o consumo de APIs, oferecendo diversos métodos e formas de interação com o serviço. Ela foi utilizada em *app_sympla/events/service.py*, possibilitando a interação com a *API Sympla*, incluindo autenticação, paginação e tratamento de erros (foram utilizadas as exceções da biblioteca, mas convertidas em exceções nativas do Python). O serviço foi modularizado em uma função responsável por consumir os dados da *API* e tratar erros, chamada *sympla_service*, além de uma função complementar para normalização e tratamento dos dados, chamada *normalize_data*.  

    - **python-dotenv**: Essa biblioteca realiza a leitura de chaves e valores de um arquivo *.env*. Ela foi utilizada para ler as variáveis de ambiente declaradas no *.env* da aplicação. Dessa forma, tanto o *Python* quanto a framework *Django* reconhecem essas configurações, sendo carregadas nos seguintes arquivos: *project/settings.py*, *project/asgi.py*, *project/wsgi.py* e *app_sympla/manage.py*. Esses arquivos foram escolhidos por serem responsáveis pela configuração geral da aplicação.  

- **Django**: A framework foi escolhida por ser robusta, segura e de fácil desenvolvimento, além de ser de conhecimento do desenvolvedor. Ela também oferece diversas funcionalidades que auxiliam na construção de uma pipeline sem muita burocracia.  
    - **MVT**: Utiliza a arquitetura *Model View Template*, que facilita a comunicação entre os componentes da aplicação, sendo esta uma aplicação *Full Stack*, contando tanto com Front End (*Templates*) quanto com Back End (*Views* e *Models*).  

    - **Templates**: Aqui foi desenvolvida toda a parte do Front End, com templates dinâmicos e devidamente organizados. O Django Template permite aplicar lógica de programação utilizando HTML, além de renderizar estilizações tanto da aplicação quanto externas. Neste projeto, foi utilizado o *Bootstrap*. Também foi implementada a paginação para a listagem dos dados coletados da *API Sympla*.  

    - **Views**: Nas *views* é feita a comunicação tanto com o banco de dados (*Models*) quanto com o serviço da *API Sympla*, sendo responsável por toda a lógica do sistema, incluindo:  
        - **Registrar Logs**: Contendo carga, mensagem coletada da operação, quantidade de eventos importados e status (sucesso ou falha).  

        - **Validar regra**: Na *view*, utilizando *atomic* (método que permite a manipulação de objetos seguindo os princípios ACID), é feita a validação do evento que está sendo criado, verificando se já foi registrado no sistema através do *sympla_id*. Caso já exista, cada atributo é validado para verificar se houve modificações. Se houver alterações, um novo objeto é criado com uma carga diferente.  

        - **Paginação**: Responsável por renderizar e passar o objeto dentro do contexto dos templates, evitando consumo excessivo de recursos do servidor ao acessar um template com renderização.  
        - **Class Based Views**: Foi utilizada para garantir uma estrutura mais modular, fácil de testar e manter, além de oferecer recursos que facilitam o desenvolvimento como um todo.  

    - **Tests**: Oferece um sistema de testes integrado à framework, baseado no *Unittest*, mas com recursos adicionais. Foi utilizado na aplicação para verificar o funcionamento adequado de todas as funcionalidades e manter uma melhor rastreabilidade do desenvolvimento.  

    - **Admin**: A framework inclui um painel administrativo que auxilia significativamente no desenvolvimento, permitindo interagir diretamente com os *models*. Nesta aplicação, foi utilizado tanto para acompanhar o desenvolvimento quanto para visualizar a criação dos objetos. O painel foi personalizado para ser mais intuitivo aos desenvolvedores, incluindo paginação e ordenação de campos.  

- **Django Rest Framework**: Considerado um complemento da framework *Django*, o *Django Rest Framework* (ou *DRF*) foi utilizado por permitir a criação de APIs RESTful seguindo a arquitetura HTTP. Foram criadas APIs para coleta de informações da pipeline, possibilitando visualizar todos os dados salvos nos *models* através do método *GET*.  
    - **Views**: No DRF, é possível utilizar diversas classes e funções para criar APIs RESTful. Nesta aplicação, foram usadas as *ModelViewSets*, que oferecem métodos prontos para os verbos HTTP, como *GET*, *POST*, *PATCH*, *PUT* e *DELETE* (embora apenas o *GET* tenha sido utilizado).  
    - **Serializer**: A framework disponibiliza serializers, cujo objetivo principal é converter objetos do Django em formatos como *JSON* (serialização) e realizar o processo inverso (desserialização).  
    - **drf spectacular**: Essa biblioteca foi utilizada para facilitar a documentação da API, utilizando a OpenAPI para criar um Swagger integrado à aplicação, acessível através do Front End do projeto.  

- **PostgreSQL**: Foi escolhido por ser um banco de dados relacional altamente escalável, adequado para este projeto. Além disso, sua configuração é simples e possui ótima integração com a framework utilizada. Ele também segue os princípios *ACID*.  

- **Docker e Docker-Compose**: Além de ser uma ótima ferramenta de desenvolvimento, principalmente por isolar aplicações, o Docker oferece praticidade na execução de projetos. Neste caso, foi utilizado para facilitar a comunicação entre dois containers (*Python* e *PostgreSQL*).