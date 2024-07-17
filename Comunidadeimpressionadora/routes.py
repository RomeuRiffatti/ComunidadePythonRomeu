from flask import render_template,redirect, url_for, flash, abort, request
from Comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPefil, FormCriarPost
from Comunidadeimpressionadora.models import Usuario, Post
from Comunidadeimpressionadora import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required  ## current_user é usado lá no html em uma condição para verificar se o usuário está logado
import secrets                                                                 ## login_required é uma função que usamos como decorator para atribuir caracteristicas para nossa 
import os  
from PIL import Image                                                                    ## função

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form: ## validate on submit roda as validações pré setadas nos forms e todas as funções com validate_ do forms tbm
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):  ## primeiro o texto encriptado que esta salvo no db e depois a senha que o usuario está colocando no formulário
            login_user(usuario, remember=form_login.lembrar_dados.data)  ## aqui é a função que faz login, e o remember é o parâmetro sobre manter logado e recebe True ou False. Esse lembrar dados retorna um booleano tbm, olhar nos forms onde declarei    
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect (par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login, Email ou Senha incorretos.', 'alert-danger') ## alerta é classe do bootstrap
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def logout():
    logout_user()
    flash('Logout feito com sucesso.','alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))    ## todos lugares onde o usuario esta logado eu posso usar o current_user pr pegar
    return render_template('perfil.html', foto_perfil=foto_perfil)                                                              ## atributo dele, aqui no caso o nome do arquivo da foto
    

@app.route('/post/criar', methods=['GET','POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data,corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com Sucesso','alert-succes')
        return redirect(url_for('home'))
    return render_template('criarpost.html',form=form)

## função para salvar nome da imagem e imagem reduzida
# adicionar um codigo aleatorio ao nome da imagem
            # reduzir o tamanho da imagem
            # salvar a imagem na pasta fotos-perfil
            # mudar o campo foto_perfil do usuario para o novo nome da imagem
            # como é muita coisa vou fazer em uma função fora
def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path,'static/fotos_perfil',nome_arquivo)  
    tamanho =(200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'. join(lista_cursos)

@app.route('/perfil/editar',methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPefil()
    if form.validate_on_submit():
        current_user.email = form.email.data   ## aqui eu posso editar o DB direto porque o usuario ja foi adicionado eu só chamo o valor e altero como se fosse um dado python 
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)  ##  nome do arquivo da imagem
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)  
        database.session.commit()
        flash('Perfil atualizado com sucesso','alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<post_id>',methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id) ##com chave primaria pode pegar com o get
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        ##lógica de editar Post
        elif form.validate_on_submit:
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso')
            return redirect(url_for('home'))
    else:
        form = None    
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir',methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort()



