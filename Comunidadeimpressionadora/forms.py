from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])  ### Os qerros que chamamos no html e que aparecem para o usuario, são resultado destes validators.
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self,email): ## essa função é uma função do próprio flaskform para verificar se o email está no DB
        usuario = Usuario.query.filter_by(email=email.data).first() ## Busca no db um email igual ao passado para a função. O primeiro email é o noem do atributo da classe e o segundo o valor 
        if usuario:                                                 ## passado para ela que a função recebeu
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login.')                                                                  



class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarPefil(FlaskForm):  ## sempre que voce tiver que subir um arquivo, para funcionar a validação de tipo de arquivo, eu vou ter que passar um parâmetro para o html junto com o POST, tem que passar o enctype=multipart/form-data
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Length(6,20)])
    foto_perfil = FileField('Atualizar Foto do Perfil',validators=[FileAllowed(['jpg','png','jpeg'])])
    curso_excel = BooleanField('Excel impressionador')
    curso_vba = BooleanField('VBA impressionador')
    curso_powerbi = BooleanField('Power BI impressionador')
    curso_python = BooleanField('Python impressionador')
    curso_ppt = BooleanField('Apresentações impressionador')
    curso_sql = BooleanField('SQL impressionador')
    botao_submit_editarperfil = SubmitField('Salvar alterações')

    def validate_email(self,email): 
        ## verificar se o cara trocou de email
        ## se mudou de email. eu tenho que pesquisar se tem outro usuário com esse mesmo email
        ## se não tiver ngm com aquele email mudamos o email
        ## se ele nao trocou de email, só mudar o username porque podem ter dois iguais
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first() 
            if usuario:                                                 
                raise ValidationError('Já existe usuário com este email. Cadastre outro email')   

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField("Criar Post")