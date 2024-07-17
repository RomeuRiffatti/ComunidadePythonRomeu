from Comunidadeimpressionadora import database, login_manager
from datetime import datetime
import pytz
from flask_login import UserMixin

## Nullable quer dizer que não pode ficar vazia esta coluna no banco
##primary key: cada usuario vai ter umna e ela é imutável
##  Com relação ao login do usuario, no models sao duas coisas para fazer:
##      Importar o login manager criar a função que vai ser a user loader do login manager
##


@login_manager.user_loader
def load_usuario(id_usuario):
     return Usuario.query.get(int(id_usuario)) ##  o get sempre encotra algo no DB pela chave primária, que no nosso caso é o id

def agora():
        return datetime.now(pytz.timezone('America/Sao_Paulo'))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post',backref='autor', lazy=True)                       ### backref é o termmo que vou utilizar para acessar os dados do usuario. post.autor retornaria todas as 
    cursos = database.Column(database.String, nullable=False, default='Não informado')     ### informações do usuario que fez o post. Esta parte do código está dizendo que está sendo criada uma relação
                                                                                           ### com a Classe Post, e que as informações do usuario que está se relacionado
    def contar_posts(self):
         return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime,default=agora())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False )  ## ForeignKey: Chave que cria a relação entre Post e Usuario. Recebe como 
                                                                                                        ### parametro a classe e de qual coluna ela está pegando. Neste caso pega 
                                                                                                        ### como chave estrangeira o id porque quer acessar a coluna id da tabela usuario
                                                                                                        ### que é estrangeira.
    