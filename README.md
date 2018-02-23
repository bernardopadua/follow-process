# Follow Process

Uma pequena aplicação com a capacidade de registrar processos e acompanhar as mudanças realizadas nos dados cadastrados destes processos.

## Requerimentos

Os passos descritos nesse README foram testatos em ambiente Linux(Ubuntu).
Para rodar estar aplicação será necessário a instalação dos seguintes items:

- Python 3.6 : https://www.python.org/downloads/
- PyPI - the Python Package Index : https://pip.pypa.io/en/stable/installing/
- Virtualenv : https://virtualenv.pypa.io/en/stable/installation/
- RabbitMQ
- Redis

### RabbitMQ

Neste caso podemos instalar utilizando o apt do ubuntu:
```
sudo apt-get install rabbitmq-server
```

Após a instalação devemos criar o usuário, senha e as permissões.
O próprio RabbitMQ nos dá uma ferramente de gerenciamento.
```
sudo rabbitmqctl add_user followprocess followprocess
sudo rabbitmqctl add_vhost followprocess_host
sudo rabbitmqctl set_permissions -p followprocess_host followprocess ".*" ".*" ".*"
```

### Redis

No próprio site tem um tutorial de como instalar de maneira fácil.
https://redis.io/topics/quickstart

Escolha uma pasta para o download e execute os comandos:
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```

Após a conclusão do comando **make** temos duas opções, ou copiamos os binários para as pastas dos binário do sistema ou executamos um comando que faz isso automaticamente.
```
sudo make install
```

Lembrando que o comando irá copiar os binários para a pasta **/usr/local/bin**.

Agora podemos iniciar o serviço do Redis usando o comando
```
src/redis-server
```
Apenas para rodar a aplicação é válido rodar sem uma configuração. Porém em produção exige um ambiente melhor estruturado.

Para que ele rode como serviço que é o melhor devemos fazer o seguinte:
```
sudo bash utils/install_server.sh
```
Algumas perguntas irão aparecer, mas você apenas dar Enter que ele vai configurar o server padrão.
Com o serviço configurado você pode iniciar ou parar a excução a qualquer hora.
```
sudo service redis_6379 start
```
Pronto, agora o redis está iniciado.

Para verificar se o Redis está funcionando basta dar o comando:
```
redis-cli ping
```
Ele deverá responder **PONG**.

## Rodando a Aplicação

### Preparando o ambiente

Após configurar os requerimentos devemos agora instalar os pacotes utilizados pela aplicação.
Utilizamos o Virtualenv para manter os pacotes locais no projeto.

Para iniciar um virtualenv basta executar:
```
virtualenv venv
```

Agora para começar a utilizar o virtualenv é necessário executar:
```
source venv/bin/activate
```
Pronto agora o seu terminal já esta utilizando o virtualenv.

Antes de utilizar o **pip** para instalar os pacotes, devemos verificar se o pip está na versão correta.
```
pip --version
```
Verifique se a versão do Python é a 3. Se não for tente utilizar o comando:
```
pip3 --version
```
Devemos utilizar a versão do **pip** que executa pelo Python 3.

Agora temos que instalar os pacotes que a aplicação utiliza.
```
cd follow-process
sudo pip install -r requirements.txt
```
Aguarde a instalação de todos os components.

**Obs: Caso dê algum erro durante a instalação dos pacotes favor rodar o comando abaixo.** 
```
sudo apt-get install build-essential python3-dev python-dev
```

### Primeira execução

Para a primeira execução é necessário criar e inicializar o Django.
Vamos primeiro criar o banco de dados, nesse projeto utilizei o sqlite.

Vamos rodar o comando que irá fazer todo o trabalho.
```
mkdir data
python manage.py makemigrations process
python manage.py migrate
```

Agora vamos criar o usuário de admin.
```
python manage.py createsuperuser
```
Só completar os campos com os dados desejados para se logar na aplicação.

### Rodando a aplicação

Para rodar a aplicação são necessários dois terminais abertos no mesmo diretório (diretório do projeto).
No primeiro vamos rodar o server do Django.
```
python manage.py runserver
```

No segundo terminal temos que rodar o worker do Celery que irá receber as **tasks** assíncronas.
```
celery worker -A followprocess -l INFO
```
Esse comando vai inicar o serviço do worker e mostrará o log de funcionamento do serviço.

Com esses dois temrinais rodando, já podemos ir até o navegador testar a aplicação.

- Url   : http://localhost:8000
- Admin : http://localhost:8000/admin/
- Endpoints REST
  - http://localhost:8000/api/v1/process
  - http://localhost:8000/api/v1/user_process
