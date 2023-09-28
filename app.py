# Importações do Flask
from flask import (
    Flask, render_template, request, redirect, url_for, 
    jsonify, abort, Response, flash
)
from flask_admin import Admin
from flask_bootstrap import Bootstrap5
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

# Importações do SQLAlchemy
from sqlalchemy import (
    Table, Column, Integer, ForeignKey, Boolean, String,
    create_engine, inspect
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_serializer import SerializerMixin

# Outras importações
import json
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    TextAreaField, SelectField, SelectMultipleField, FieldList
)
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField
from flask import Flask, request, send_file
import subprocess
import open_ai  # Importe o script open_ai.py
import os
import requests
from flask import Flask, redirect, url_for
from flask_login import LoginManager, logout_user, login_required
from key import SECRET_KEY
import traceback
from flask_login import current_user



app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap5(app)
app.static_folder = 'static'
admin = Admin(app, name='app', template_mode='bootstrap5')

class CybersecurityCategories(db.Model):
    __tablename__ = 'CybersecurityCategories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable=False)
    requirements = db.relationship('CybersecurityRequirements', back_populates='category')

class CybersecurityRequirements(db.Model):
    __tablename__ = 'CybersecurityRequirements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requirement_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('CybersecurityCategories.id'), nullable=False)
    category = db.relationship('CybersecurityCategories', back_populates='requirements')
    projects = db.relationship('ProjectCybersecurityRequirements', back_populates='requirement')

class Project(db.Model):
    __tablename__ = 'projeto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    arquiteto_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    compliance_projeto = db.Column(db.Boolean)
    debitos_tecnicos = db.Column(db.String(100), nullable=False)
    status_projeto = db.Column(db.Text, nullable=False)
    componentes_multi = db.Column('componentes_multi', db.JSON, default=[])
    tecnologias_multi = db.Column('tecnologias_multi', db.JSON, default=[])
    arquitetura_cloud_multi = db.Column('arquitetura_cloud_multi', db.JSON, default=[])
    modelagem_ameacas = db.Column(db.Text, nullable=False)

    arquiteto = db.relationship('User', back_populates='project')
    requirements = db.relationship('ProjectCybersecurityRequirements', back_populates='project')

    
class ProjectCybersecurityRequirements(db.Model):
    __tablename__ = 'ProjectCybersecurityRequirements'
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('CybersecurityRequirements.id'), primary_key=True)
    attainment = db.Column(db.Boolean, default=True)
    project = db.relationship('Project', back_populates='requirements')
    requirement = db.relationship('CybersecurityRequirements', back_populates='projects')
    
    #Cores das Categorias
    
    cores_categorias = {
    "Autenticação e Acesso": "bg-danger",
    "Rede e Infraestrutura": "bg-warning",
    "Desenvolvimento e Monitoramento": "bg-success",
    "Governança e Treinamento": "bg-info"
}

    ### JSON processing for arrays ###

    @property
    def componentes_multi(self):
        return json.loads(self._componentes_multi)

    @componentes_multi.setter
    def componentes_multi(self, value):
        self._componentes_multi = json.dumps(value)

    @property
    def tecnologias_multi(self):
        return json.loads(self._tecnologias_multi)

    @tecnologias_multi.setter
    def tecnologias_multi(self, value):
        self._tecnologias_multi = json.dumps(value)

    @property
    def arquitetura_cloud_multi(self):
        return json.loads(self._arquitetura_cloud_multi)

    @arquitetura_cloud_multi.setter
    def arquitetura_cloud_multi(self, value):
        self._arquitetura_cloud_multi = json.dumps(value)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Alterado de username para email
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

# Definindo a classe SignupForm
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Novo campo
    password = PasswordField('Password', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

def get_architect_choices():
    users = User.query.all()
    return [(str(user.id), user.username) for user in users]
    
class ProjectForm(FlaskForm):
    nome = StringField('Nome do Projeto', validators=[DataRequired()])
    arquiteto = SelectField('Arquiteto', validators=[DataRequired()])    
    descricao = TextAreaField('Descrição do Projeto', validators=[DataRequired()])
    modelagem_ameacas = TextAreaField('Modelagem de Ameaca')
    debitos_tecnicos = TextAreaField('Débitos Técnicos')
    status_projeto = SelectField('Fase de Envolvimento', choices=[
        ('Requisito', 'Requisito'),
        ('Design', 'Design'),
        ('Deploy', 'Deploy'),
        ('Sustentação', 'Sustentação')
    ])
    compliance_projeto = BooleanField('Compliance')
    componentes_multi = SelectMultipleField('Componentes do Projeto', choices=[
        ('aplicacoes_web', 'Aplicações Web'),
        ('aplicacoes_moveis', 'Aplicações Móveis'),
        ('aplicacoes_desktop', 'Aplicações Desktop'),
        ('aplicacoes_backend', 'Aplicações Backend'),
        ('apis', 'APIs'),
        ('web_services', 'WebServices'),
        ('brokers_demensagens', 'Brokers de Mensagens'),
        ('etls', 'ETLs'),
        ('arquitetura_orientada_servicos', 'Arquitetura Orientada a Serviços'),
        ('orquestracao', 'Orquestração'),
        ('descobertade_servicos', 'Descoberta de Serviços'),
        ('gateway_de_api', 'Gateway de API'),
        ('bancos_de_dados', 'Bancos de Dados'),
        ('servicos_de_cache', 'Serviços de Cache'),
        ('balanceadores_de_carga', 'Balanceadores de Carga'),
        ('cdn', 'Redes de Entrega de Conteúdo'),
        ('servicos_de_filas_e_streaming', 'Serviços de Filas e Streaming')
    ])

    tecnologias_multi = SelectMultipleField('Tecnologias do Projeto', choices=[
        ('servidores_fisicos', 'Servidores Físicos'),
        ('virtualizacao', 'Virtualização'),
        ('armazenamento', 'Armazenamento'),
        ('containers', 'Containers'),
        ('vpn', 'VPN'),
        ('sdwan', 'SD-WAN'),
        ('protocolos_de_comunicacao', 'Protocolos de Comunicação'),
        ('firewalls', 'Firewalls'),
        ('ids_ips', 'IDS/IPS')
    ])

    arquitetura_cloud_multi = SelectMultipleField('Arquitetura Cloud', choices=[
        ('iaas', 'IaaS'),
        ('paas', 'PaaS'),
        ('saas', 'SaaS'),
        ('multicloud', 'MultiCloud'),
        ('onprem', 'OnPrem'),
        ('hybrid_cloud', 'HybridCloud'),
        ('cloud_privada', 'Cloud Privada'),
        ('cloud_comunitaria', 'Cloud Comunitária'),
        ('edge_computing', 'Edge Computing'),
        ('faas', 'FaaS'),
        ('kubernetes', 'Kubernetes')
    ])
    submit = SubmitField('Salvar')
   
@app.route('/adicionar_projeto', methods=['GET', 'POST'])
@login_required
def adicionar_projeto():
    form = ProjectForm()
    form.arquiteto.choices = get_architect_choices() 
    requirements = CybersecurityRequirements.query.all()
    categories = CybersecurityCategories.query.all()

    for req in requirements:
        field_name = "requirement-" + str(req.id)
        field = BooleanField(req.requirement_name)
        setattr(ProjectForm, field_name, field)

    #form = ProjectForm()  # Crie uma nova instância do formulário após adicionar todos os campos dinâmicos

    try:
        if form.validate_on_submit():
            projeto = Project(
                nome=form.nome.data,
                descricao=form.descricao.data,
                arquiteto_id=form.arquiteto.data, 
                compliance_projeto=form.compliance_projeto.data,
                status_projeto=form.status_projeto.data,
                debitos_tecnicos=form.debitos_tecnicos.data,
                componentes_multi=form.componentes_multi.data,
                tecnologias_multi=form.tecnologias_multi.data,
                arquitetura_cloud_multi=form.arquitetura_cloud_multi.data,
                modelagem_ameacas=form.modelagem_ameacas.data or 'Modelagem de Ameaças ainda não realizada.'

            )

            db.session.add(projeto)
            db.session.flush()

            for req in requirements:
                field_name = "requirement-" + str(req.id)
                if getattr(form, field_name).data:
                    pr = ProjectCybersecurityRequirements(projeto_id=projeto.id, requirement_id=req.id, attainment=True)
                else:
                    pr = ProjectCybersecurityRequirements(projeto_id=projeto.id, requirement_id=req.id, attainment=False)
                db.session.add(pr)

            db.session.commit()
            return redirect(url_for('index'))

        return render_template('adicionar_projeto.html', form=form, categories=categories, requirements=requirements)

    except Exception as e:
        db.session.rollback()
        error_info = traceback.format_exc()  # Obtenha o stack trace completo
        print(error_info)  # Imprima o stack trace no console
        return jsonify(success=False, error=f"Erro ao adicionar projeto: {str(e)}\n{error_info}"), 500


@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(projeto_id):
    projeto = Project.query.get_or_404(projeto_id)  # Se não encontrar o projeto, retorna 404
    form = ProjectForm()
    form.arquiteto.choices = get_architect_choices() 

    requirements = CybersecurityRequirements.query.all()
    categories = CybersecurityCategories.query.all()

    for req in requirements:
        field_name = "requirement-" + str(req.id)
        field = BooleanField(req.requirement_name)
        setattr(ProjectForm, field_name, field)

    if form.validate_on_submit():
        try:
            projeto.nome = form.nome.data
            projeto.descricao = form.descricao.data
            projeto.arquiteto_id = form.arquiteto.data 
            projeto.compliance_projeto = form.compliance_projeto.data
            projeto.status_projeto = form.status_projeto.data
            projeto.debitos_tecnicos = form.debitos_tecnicos.data
            projeto.componentes_multi = form.componentes_multi.data
            projeto.tecnologias_multi = form.tecnologias_multi.data
            projeto.arquitetura_cloud_multi = form.arquitetura_cloud_multi.data
            projeto.modelagem_ameacas=form.modelagem_ameacas.data

            # Atualizando os requirements
            all_requirements_ids = [r.id for r in CybersecurityRequirements.query.all()]
            for req_id in all_requirements_ids:
                req_id = int(req_id)
                requirement_key = 'requirement-' + str(req_id)
                requirement_obj = ProjectCybersecurityRequirements.query.filter_by(
                    projeto_id=projeto_id, requirement_id=req_id).first()

                # Verificando se requirement_obj é None e criando um novo objeto, se necessário
                if requirement_obj is None:
                    requirement_obj = ProjectCybersecurityRequirements(
                        projeto_id=projeto_id,
                        requirement_id=req_id,
                        attainment=getattr(form, requirement_key).data
                    )
                    db.session.add(requirement_obj)
                else:
                    requirement_obj.attainment = getattr(form, requirement_key).data

            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, error=f"Erro ao editar projeto: {str(e)}"), 500

    else:
        # Pre-fill form data with existing project data
        form.nome.data = projeto.nome
        form.descricao.data = projeto.descricao
        form.arquiteto.data = projeto.arquiteto
        form.compliance_projeto.data = projeto.compliance_projeto
        form.status_projeto.data = projeto.status_projeto
        form.debitos_tecnicos.data = projeto.debitos_tecnicos
        form.componentes_multi.data = projeto.componentes_multi
        form.tecnologias_multi.data = projeto.tecnologias_multi
        form.arquitetura_cloud_multi.data = projeto.arquitetura_cloud_multi
        form.modelagem_ameacas.data= projeto.modelagem_ameacas


        # Add existing requirements attainment data to form
        for req in requirements:
            field_name = "requirement-" + str(req.id)
            requirement_obj = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, requirement_id=req.id).first()
            getattr(form, field_name).data = requirement_obj.attainment if requirement_obj else False

        attained_requirement_ids = [req.id for req in requirements if ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, requirement_id=req.id, attainment=True).first()]

        # Passar a lista de IDs de requisitos atingidos para o template
        return render_template('adicionar_projeto.html', form=form, categories=categories, requirements=requirements, projeto=projeto, attained_requirement_ids=attained_requirement_ids)
      
@app.route('/dados-do-banco', methods=['GET'])
@login_required
def obter_dados_do_banco():
    try:          
        # Consulta todos os projetos
        projetos = Project.query.all()

        requisitos_nao_verificados = {req.requirement_name: 0 for req in CybersecurityRequirements.query.all()}


        # Loop por todos os projetos para verificar seus requisitos
        for projeto in projetos:
            # Consulta os requisitos de segurança associados ao projeto que NÃO estão verificados
            requisitos_projeto = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto.id, attainment=False).all()
            
            # Loop pelos requisitos não verificados e atualiza a contagem
            for req in requisitos_projeto:
                nome_requisito = CybersecurityRequirements.query.get(req.requirement_id).requirement_name
                if nome_requisito in requisitos_nao_verificados:
                    requisitos_nao_verificados[nome_requisito] += 1
                    
           # Crie listas de rótulos e dados para o gráfico
        categories = CybersecurityCategories.query.all()
        categorias = {categoria.category_name: [req.requirement_name for req in categoria.requirements] for categoria in categories}
        
        numero_de_projetos = len(projetos)
        #print(f"Total de projetos: {numero_de_projetos}")

        percentuais_categorias = {}
        for categoria, requirements in categorias.items():
            total_requisitos_por_projeto = len(requirements)
            total_requisitos = total_requisitos_por_projeto * numero_de_projetos

          #  print(f"\nCategoria: {categoria}")
          #  print(f"Total de requisitos por projeto: {total_requisitos_por_projeto}")
          #  print(f"Total de requisitos considerando todos os projetos: {total_requisitos}")

            # Calcular o número de requisitos não atendidos
            nao_atendidos = sum(requisitos_nao_verificados.get(requisito, 0) for requisito in requirements)
          #  print(f"Total de requisitos não atendidos: {nao_atendidos}")

            # Calcular o número de requisitos atendidos
            atendidos = total_requisitos - nao_atendidos
          #  print(f"Total de requisitos atendidos: {atendidos}")

            # Calcular a porcentagem de requisitos atendidos
            percentual_atendido = (atendidos / total_requisitos) * 100
          #  print(f"Porcentagem de requisitos atendidos: {percentual_atendido}%")

            percentuais_categorias[categoria] = round(percentual_atendido, 2)

       # print("\nPercentuais finais por categoria:", percentuais_categorias)


           
        labels = list(requisitos_nao_verificados.keys())
        dados = list(requisitos_nao_verificados.values())
        requisitos_sum = sum(dados)
        
        return jsonify({'requisitos': requisitos_nao_verificados, 'labels': labels, 'dados': dados, 'requisitos_sum': requisitos_sum, 'percentuais_categorias':percentuais_categorias})

    except Exception as e:
        return abort(500, description=f"Erro ao buscar dados do banco: {str(e)}")


@app.route('/projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def obter_dados_do_projeto(projeto_id):
    projeto = Project.query.get_or_404(projeto_id)  # Se não encontrar o projeto, retorna 404
    #projeto = ProjectForm()

    try:
        # Para o método GET:
        categories = CybersecurityCategories.query.all()
        requirements = CybersecurityRequirements.query.all()
        attained_requirements = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, attainment=True).all()
        not_attained_requirements = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, attainment=False).all()
        attained_requirement_ids = [req.requirement_id for req in attained_requirements]
        not_attained_requirement_ids = [req.requirement_id for req in not_attained_requirements]
        not_attained_requirement_names = [req.requirement.requirement_name for req in not_attained_requirements]

        # Verificar se o cliente deseja resposta em JSON
        if request.headers.get('Accept') == 'application/json':
            response_data = {
                'projeto': {
                    'id': projeto.id,
                    'nome': projeto.nome,
                    'descricao': projeto.descricao,
                    'debitos_tecnicos': projeto.debitos_tecnicos,
                    'status_projeto' : projeto.status_projeto,
                    'componentes_multi': projeto.componentes_multi,
                    'tecnologias_multi': projeto.tecnologias_multi,
                    'arquitetura_cloud_multi': projeto.arquitetura_cloud_multi
                },
                'categorias_avaliadas': [category.category_name for category in categories],
                'requirements': [req.requirement_name for req in requirements],
                'not_attained_requirements': not_attained_requirement_names,
            }
            formatted_json = json.dumps(response_data, indent=4, ensure_ascii=False)
            return Response(formatted_json, content_type='application/json; charset=utf-8')
            #return jsonify(response_data)

        return render_template('adicionar_projeto.html'
                            , categories=categories
                            , requirements=requirements
                            , projeto=projeto
                            , attained_requirement_ids=attained_requirement_ids
                            , not_attained_requirement=not_attained_requirements 
                            )
    except Exception as e:
        return jsonify({'error': f"Erro ao buscar os dados: {str(e)}"}), 500

 ###### Gerar Relatório #######
 
@app.route('/gerar-relatorio', methods=['POST'])
@login_required
def gerar_relatorio():
    projeto_id = request.form.get('projeto_id')  # obtendo o projeto_id do corpo da requisição
    if not projeto_id:
        return jsonify({'error': 'projeto_id não fornecido'}), 400

    # Fazendo uma requisição interna para obter os dados do projeto
    response = requests.get(
    f'http://127.0.0.1:5000/projeto/{projeto_id}',
    headers={'Accept': 'application/json'}
)
    if response.status_code != 200:
        return jsonify({'error': 'Erro ao obter dados do projeto'}), response.status_code

    projeto_data = response.json()
    # Agora envia os dados do projeto para o módulo open_ai
    report = open_ai.generate_threat_modeling_report(projeto_data)

    projeto = Project.query.get(projeto_id)
    if projeto:
        projeto.modelagem_ameacas = report
        db.session.commit()
        return jsonify({'message': 'Relatório de modelagem de ameaças atualizado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Projeto não encontrado'}), 404

    
    
 ###### Excluir Projeto #######   
    
@app.route('/excluir_projeto/<int:projeto_id>', methods=['POST'])
@login_required
def excluir_projeto(projeto_id):
    try:
        # Buscando o projeto pelo ID
        projeto = Project.query.get_or_404(projeto_id)
        
        # Deletando todas as relações de requirements relacionadas a esse projeto
        ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id).delete()

        # Deletando o projeto
        db.session.delete(projeto)
        db.session.commit()

        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=f"Erro ao excluir projeto: {str(e)}"), 500

@app.route('/')
@login_required
def index():
    projetos = Project.query.all()
    
    # Obter dados do banco
    response = obter_dados_do_banco()
    
    # Supondo que a função obter_dados_do_banco retorne um objeto JSON, converta-o em um dicionário Python
    dados_do_banco = json.loads(response.data.decode('utf-8'))
    
    dados = dados_do_banco.get("dados", {})
    requisitos_sum = dados_do_banco.get("requisitos_sum", {})
    percentuais_categorias = dados_do_banco.get("percentuais_categorias", {})
    
    cores_categorias = {
        "Autenticação e Acesso": "bg-aa",
        "Rede e Infraestrutura": "bg-ri",
        "Desenvolvimento e Monitoramento": "bg-dm",
        "Governança e Treinamento": "bg-gt"
    }

    return render_template('index.html',
                       projetos=projetos,
                       dados=dados_do_banco,
                       requisitos_sum=requisitos_sum,
                       percentuais_categorias=percentuais_categorias,
                       cores_categorias=cores_categorias)
    
@app.route('/minhas_modelagens')
@login_required
def index_arch():
    arquiteto_id = current_user.id  # Obtém o ID do arquiteto logado
    projetos = Project.query.filter_by(arquiteto_id=arquiteto_id).all()  # Filtra os projetos pelo arquiteto logado

    # O restante do código permanece o mesmo...
    response = obter_dados_do_banco()

    dados_do_banco = json.loads(response.data.decode('utf-8'))

    dados = dados_do_banco.get("dados", {})
    requisitos_sum = dados_do_banco.get("requisitos_sum", {})
    percentuais_categorias = dados_do_banco.get("percentuais_categorias", {})

    cores_categorias = {
        "Autenticação e Acesso": "bg-aa",
        "Rede e Infraestrutura": "bg-ri",
        "Desenvolvimento e Monitoramento": "bg-dm",
        "Governança e Treinamento": "bg-gt"
    }

    return render_template('index_arch.html',
                           projetos=projetos,
                           dados=dados_do_banco,
                           requisitos_sum=requisitos_sum,
                           percentuais_categorias=percentuais_categorias,
                           cores_categorias=cores_categorias)


    
        #### Login ####

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Alterado de username para email
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Adicionado campo de nome de usuário

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    project = db.relationship('Project', back_populates='arquiteto')

    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/index')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # lógica da rota
    return render_template('profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('teste')
    if form.validate_on_submit():  
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        print('teste2')
        if user and user.check_password(password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')  # Mensagem de sucesso
            return redirect(url_for('index')) # Redirecionar para o dashboard depois de fazer login
        else:
            flash('Usuário ou senha incorretos. Por favor, tente novamente.', 'danger')  # Mensagem de erro
            print('teste3')
    print('teste4')
    return render_template('login.html', form=form)  # Passar o formulário para o template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data  # Novo campo
        password = form.password.data
        new_user = User(username=username, email=email)  # Atualizado
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Registro bem-sucedido!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

