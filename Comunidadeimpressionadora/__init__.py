

## Esse arquvi init basicamente importa o app e coloca ele pra rodar
## aqui tem que:
#   1. importar o app
#   2. criar configuração do app
#   3. Criar configuração do banco de dados
#   4. importar as rotas
#     
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)

bcrypt = Bcrypt(app)
## informações do login_manager, que serve para bloquear páginas para usuário não logados e fazer redirecionamento inteligente para usuarios que fazem login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  ## para uso do login_required. ele diz para que função vai redirecionar quando o usuario tentar acessar uma pagina tem login¨_required
login_manager.login_message_category = 'alert-info' ## classe do bootstrap de caixa azul

from Comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("base de dados criada")
else:
    print("base de dados ja existente")


##Esse import está aqui em baixo porque primeiro o init acessa a pasta e inicia o programa e depois ele pega os routes com a pasta já aberta, se importar antes a pasta de routes ainda nao foi aberta. 
## o app ainda nao foi criado

from Comunidadeimpressionadora import routes

