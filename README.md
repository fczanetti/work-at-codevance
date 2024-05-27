![Static Badge](https://img.shields.io/badge/Python-3.11-blue?link=https%3A%2F%2Fwww.python.org%2F)
![Static Badge](https://img.shields.io/badge/Django-5.0.4-green?link=https%3A%2F%2Fwww.djangoproject.com%2F)
[![codecov](https://codecov.io/gh/fczanetti/work-at-codevance/graph/badge.svg?token=vffyZTHCt3)](https://codecov.io/gh/fczanetti/work-at-codevance)

This project is hosted on Fly.io, you can visit [via this link](https://work-at-codevance.fly.dev/) and test the
functionalities using the following operator account:

- user: operator@email.com
- password: operatorpass123#

# Content

- [Instalation](https://github.com/fczanetti/work-at-codevance?tab=readme-ov-file#instala%C3%A7%C3%A3o)
- [Users and permissions](https://github.com/fczanetti/work-at-codevance?tab=readme-ov-file#tipos-de-usu%C3%A1rio-e-permiss%C3%B5es)
- [Deploy on Fly.io](https://github.com/fczanetti/work-at-codevance?tab=readme-ov-file#deploy-no-flyio)
- [Requirements - Work at Codevance](https://github.com/fczanetti/work-at-codevance?tab=readme-ov-file#trabalhe-na-codevance)


## Instalation

For local instalation Docker will be required, since PostgreSQL database and RabbitMQ will be executed in containers.

The folowing instructions are required to execute this application locally.

Clone this repository using the command:

```
git clone git@github.com:fczanetti/work-at-codevance.git
```

Create a virtual environment to install the required libraries:

```
pipenv shell
```

Install libraries running the following command:

```
pipenv sync -d
```

Copy the content from env-sample file located inside 'contrib' folder, in project's root, and paste the content
in a new file called .env, also in project's root.

Set the following environment variables in .env as listed below:

- SECRET_KEY=secret
- DEBUG=True
- ALLOWED_HOSTS=localhost, 127.0.0.1,
- CSRF_TRUSTED_ORIGINS= // this one can have no value for now

- CELERY_BROKER_URL=pyamqp://rabbituser:rabbitpass@localhost:5672/

The value of DATABASE_URL should not be changed in env-sample file, since it is the one used by GitHub Actions when
pushing. In the new file called .env, you have to override the variable as follows:

- DATABASE_URL=postgres://dbuser:dbpass@localhost:5437/codevance_db
- POSTGRES_PASSWORD=dbpass
- POSTGRES_USER=dbuser
- POSTGRES_DB=codevance_db

The next variable is the rate applied when creating anticipations and, for a 3%/month rate, the value should be as
follows:

- INTEREST_RATE=0.03

To test sending emails locally we can just fill EMAIL_BACKEND, and Django will print the email in the console instead
of sending real emails at this moment:

- EMAIL_HOST=
- EMAIL_PORT=
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=
- EMAIL_USE_TLS=
- DEFAULT_FROM_EMAIL=
- EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

To execute the project locally the follwoing ones can be blank:

- AWS_ACCESS_KEY_ID=
- AWS_SECRET_ACCESS_KEY=
- AWS_STORAGE_BUCKET_NAME=

After setting the variables in .env, run the following command to start PostgreSQL and RabbitMQ services in Docker
containers. This command will create a '.pgdata' folder in project's root, and it will be responsible for persisting
data from our PostgreSQL database.

```
docker compose up -d
```

Having a running database available, apply the migrations:

```
python manage.py migrate
```

In another terminal, activate the virtual environment and use the following command to start a Celery's worker:

```
celery -A workatcodev worker -l info
```

After these first settings, we can run 'pytest' in our terminal to make sure all tests are passing.

Create a superuser through the command:

```
python manage.py createsuperuser
```

Start Django server:

```
python manage.py runserver
```

With a superuser created it is possible to login in our application and create a new operator. To create, you just have
to click in 'New User' link and fill the required data, and remember to mark the 'Is Operator' option. With a new
operator, you can logout from your superuser account and login using your new operator one, and then you will be able
to test the application.
You can also create a supplier to see how it works. First, it's necessary to create a common user (the same process
of creating an operator, but this time do not mark the 'Is Operator' option). Having a common user you can click on
'New Supplier', select the user you have just created and fill some other required information.
Remember that, when logging using your supplier account, you will be restricted to supplier permissions, and some
resources won't be available. Follow this tutorial for more information about it.


After creating an operator and a supplier it is possible to create some payments related to this supplier on the link
'New Payment'. With a payment available you can request an anticipation for it, and it will be approved or denied by
an operator. Requesting anticipations, approving or denying creates a log, and these logs can be checked using the 'Logs'
link. Every time a log is created, an email will be sent to the supplier (in the email used when registering). This email
can also be checked in the console, the one we used to start Celery's worker.


## Users and permissions

### Operator
- can add a new user;
- can add a new supplier;
- can add payments for any supplier;
- can request anticipations for any supplier's payments;
- can see any supplier's payments, anticipations and logs;
- can approve or deny any supplier's anticipation.

### Supplier
- can add payments only for himself;
- can request anticipations only for his own payments;
- can see only his own payments, anticipations and logs.

### Common user
- can see any supplier's payments, anticipations and logs.


## Deploy on Fly.io

To deploy, as a suggestion, Fly.io can be used. Besides Fly.io, some other integrations will be necessary for the
application to work as a whole.

### Sendgrid integration

To send emails, SendGrid platform can be used. Follow this step by step to have the necessary values to set Fly.io
when deploying:

- create an account on SendGrid website;
- na seção 'Marketing', criar um 'Sender' que servirá para o envio de emails. O email também deverá ser verificado;
- na seção 'Email API, clique no link 'Integration Guide' e em seguida escolha a opção 'SMTP Relay';
- crie uma API key informando um nome, e em seguida salve os valores exibidos na tela (Server, Ports, Username, Password).
Usaremos esses dados para configurar a plataforma Fly.io.

### Serviço RabbitMQ

Para que tenhamos um serviço de RabbitMQ, necessário para o envio de emails em conjunto com o Celery, uma sugestão é
utilizar a plataforma CloudAMQP. No website do CloudAMQP, siga estes passos:

- acesse criando uma conta ou fazendo login com GitHub, por exemplo;
- crie uma instância gratuita do RabbitMQ e acesse sua página principal;
- na seção 'AMQP details', copie e salve o valor da URL para ser usado posteriormente.

### Conta AWS para arquivos estáticos

Este projeto foi pré configurado para enviar os arquivos estáticos para um Buckets S3 da AWS. Para utilizar este
recurso os seguintes passos devem ser seguidos:

- criar um usuário IAM na plataforma AWS e anexar a este uma política de permissão chamada AmazonS3FullAccess;
- criar uma access key para este usuário. A access key terá um ID e seu real valor, ambos serão utilizados;
- criar um bucket S3 para arquivos estáticos e anexar uma política de permissão que permita ao usuário IAM a ação
'PutObject' no bucket e em todas as suas pastas;

### Deploy

- instale o flyctl executando o seguinte comando no terminal, pode ser na pasta do projeto:

Este comando é para usuários Linux. Para outras opções, [acesse este link](https://fly.io/docs/hands-on/install-flyctl/);
```
curl -L https://fly.io/install.sh | sh
```

- crie uma conta através do seguinte comando. Você deve ser direcionado para o site da plataforma para concluir a conta.

```
fly auth signup
```

- após a criação, novamente no terminal, utilize o seguinte comando para login:

```
fly auth login
```

- execute este comando de dentro da pasta raiz do projeto para criar um novo aplicativo na plataforma:

```
fly launch --no-deploy
```

- o Fly identificará que já existe um arquivo fly.toml criado, e ao perguntar se deseja copiar as configurações deste
arquivo para o novo aplicativo responda com a opção 'y' (yes);
- as configurações iniciais serão exibidas, e não será necessário alterá-las caso seja questionado novamente pelo Fly;
- o Fly deve questionar também se deseja substituir o arquivo .dockerignore e o Dockerfile, o que também não será
necessário;
- pode ser que o Fly altere a configuração 'release_command' do arquivo fly.toml existente e, caso isso aconteça, corrija
esta com o valor './start.sh' que estava configurado anteriormente;
- criar um cluster do PostgreSQL no Fly.io através do comando:

```
fly postgres create
```

- escolha um nome para o banco de dados;
- selecione uma região;
- selecione a configuração Development pois já é suficiente;
- por último escolha a opção 'scale node pg to zero after one hour', que desligará a VM após uma hora se o banco de dados
não estiver sendo utilizado;
- após o cluster ser criado, utilize o seguinte comando para vincular o bando de dados ao applicativo no Fly.io:

```
fly postgres attach NOME_DO_BANCO_CRIADO -a work-at-codevance (este último é o nome do aplicativo)
```

Neste momento já temos um aplicativo no Fly.io, que podemos acessar para configurar as variáveis de ambiente. Estas
podem ser configuradas diretamente pela plataforma clicando na aplicação e acessando o link 'Secrets'. Caso opte por
configurar pelo terminal, é possível através do seguinte comando:

```
fly secrets set NOME_DA_VARIAVEL=valor_da_variavel
```

- configure as variáveis de ambiente na plataforma com os seguintes valores:

- SECRET_KEY= (configurada automaticamente pelo Fly, não alterar)
- ALLOWED_HOSTS=work-at-codevance.fly.dev (nome_do_aplicativo.fly.dev)
- CSRF_TRUSTED_ORIGINS=https://work-at-codevance.fly.dev (https://nome_do_aplicativo.fly.dev)

- CELERY_BROKER_URL= (valor da URL da instância do RabbitMQ criada no site CloudAMQP)

- INTEREST_RATE=0.03

- EMAIL_HOST=(valor do 'Server' salvo no site SendGrid)
- EMAIL_PORT=587
- EMAIL_HOST_USER=(valor do 'Username' salvo no site SendGrid)
- EMAIL_HOST_PASSWORD=(valor do 'Password' salvo no site SendGrid)
- EMAIL_USE_TLS=True
- DEFAULT_FROM_EMAIL=(email utilizado na criação do 'Sender' no site SendGrid)
- EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

- AWS_ACCESS_KEY_ID=(ID da access key criada na plataforma AWS)
- AWS_SECRET_ACCESS_KEY=(valor da access key criada na plataforma AWS)
- AWS_STORAGE_BUCKET_NAME=(nome do bucket criado na plataforma AWS)

- após todas as variáveis configuradas, utilizar o seguinte comando para deploy:

```
fly deploy
```

- assim que finalizado, utilizar o comando a seguir para acessar o console do aplicativo já em execução:

```
fly ssh console
```

- feito o acesso, podemos criar um superuser e iniciar o uso do aplicativo hospedado no Fly.io:

```
python manage.py createsuperuser
```

Com um superuser criado já é possível logar no aplicativo e iniciar o uso.


# Trabalhe na Codevance

A [Codevance](https://codevance.com.br) é uma software house que tem como missão otimizar os resultados e gerar valor ao seu negócio utilizando tecnologia como meio.

Somos especialistas em Python, nosso time atua todo de forma remota e nossos clientes possuem grandes desafios tecnológicos.

Se você:

- Tem sangue no olho e é, ou busca ser, um ótimo programador;
- Tem interesse em crescer profissionalmente;
- É organizado, tem disciplina e autonomia para trabalhar do conforto da sua casa;
- Gosta da linguagem Python ou já utilizou em algum projeto profissional;

Eu te convido a clonar esse repositório, meter a mão na massa e mostrar pra gente as suas qualidades.

Temos vagas para todos os perfis. Não é preciso ter experiência e não fazemos nenhum tipo de distinção.

## Como participar

1. Clone este repositório
1. Siga as instruções abaixo
1. Suba o projeto em algum lugar (heroku, de preferência)
1. Envie um e-mail para ronaldo *dot* oliveira *at* codevance *dot* com *dot* br

## Especificações

Você vai desenvolver um sistema de antecipação de pagamentos.

Imagine que haja uma série de pagamentos a serem feitos por uma empresa no decorrer dos próximos meses, mas a empresa quer fazer um plano com seus fornecedores para fazer estes pagamentos de forma adiantada, concedendo um desconto relacionado a quantidade de dias de diferença entre a data de vencimento original do pagamento e a nova data de pagamento.

O objetivo é fornecer melhor fluxo de caixa ao fornecedor e rentabilizar o caixa da empresa através dos descontos.

Para descobrir o novo valor a ser pago nesta antecipação, o cálculo a ser feito é:

```
NOVO_VALOR = VALOR_ORIGINAL - (VALOR_ORIGINAL * ((3% / 30) * DIFERENCA_DE_DIAS))
```

Vamos a um exemplo prático:

```
DATA DE VENCIMENTO ORIGINAL = 01/10/2019
VALOR ORIGINAL = R$ 1.000,00
NOVA DATA DE VENCIMENTO = 15/09/2019

NOVO VALOR = 1000 - (1000 * ((3% / 30) * 16))
NOVO VALOR = 1000 - (1000 * 0,016)
NOVO VALOR = 1000 - 16

NOVO VALOR = R$ 984,00
```

### Características

- O sistema deve armazenar os pagamentos e suas informações básicas
  - id do pagamento, data de emissão, data de vencimento, valor original, a qual fornecedor pertence, dados cadastrais básicos deste fornecedor, como razão social e CNPJ.
- Para um pagamento ser adiantado, o fornecedor deve fazer uma solicitação, então o operador da empresa escolhe se libera a antecipação ou nega a antecipação. Toda essa movimentação deve ficar armazenada em um log.
  - Essa solicitação pode vir via sistema ou por outras vias. Quando vier por outras vias, o operador da empresa fará a solicitação no sistema.
- O fornecedor deve ter acesso a uma área, através de autenticação via email e senha, onde ele possa solicitar a antecipação de um pagamento. É necessário também que ele veja todos os pagamentos disponíveis para antecipação, todos os pagamentos aguardando liberação, todos os aprovados e todos os negados.
  - Importantíssimo que um fornecedor não veja os pagamentos de outro
- Para cada ação sobre um pagamento (solicitação, liberação, negação) o sistema deve enviar um email ao fornecedor.
  - Este envio de email deve ser feito de forma assíncrona (`celery` é seu amigo)
- Caso um pagamento chegue até sua data de vencimento sem ser antecipado, o mesmo deve ser indisponibilizado para operação, mas mantido no histórico.
  - Fornecedores não podem ver pagamentos indisponibilizados disponíveis para antecipação
- Deve haver uma API Rest básica com dois endpoints:
  - Um endpoint que liste as operações de um fornecedor, que estará autenticado via JWT. Este endpoint deve permitir filtro por estado do pagamento (indisponível, disponível, aguardando confirmação, antecipado, negado)
  - Outro endpoint que será responsável pela solicitação de antecipação de um pagamento. Este endpoint deve receber o identificador do pagamento e, obviamente, um usuário logado só pode solicitar antecipação dos pagamentos associados ao seu usuário.

## Requisitos técnicos

- Utilize Python 3.7 (ou mais recente) como linguagem e PostgreSQL como banco de dados;
- Utilize um framework (dica: com django é mais fácil);
- O código deve estar em inglês (commits podem estar em pt-br);
- O sistema deve estar online, rodando, em algum lugar (dica: com heroku é mais fácil);
- O sistema deve ter testes automatizados (dica: com pytest é mais fácil);
- O repositório deve conter documentação sobre como fazer deployment e como testar;
- Deve conter uma documentação da API;

## Recomendações e dicas

- Caso for utilizar Django, temos [nosso cookiecutter](https://github.com/codevance/cookiecutter-django) que pode servir de ponto de partida (mas não é obrigatório);
- Use boas práticas de programação;
- Modele os dados com cuidado;
- Se preocupe com arquitetura e qualidade de código, não se preocupe com estética (dica: bootstrap é seu amigo).

**Divirta-se!**
