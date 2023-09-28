from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from sqlalchemy import inspect
import json
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import LoginManager, UserMixin,login_user,login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
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
    arquiteto = db.Column(db.String(100), nullable=False)
    compliance_projeto = db.Column(db.Boolean)
    debitos_tecnicos = db.Column(db.String(100), nullable=False)
    status_projeto = db.Column(db.Text, nullable=False)
    componentes_multi = db.Column('componentes_multi', db.JSON, default=[])
    tecnologias_multi = db.Column('tecnologias_multi', db.JSON, default=[])
    arquitetura_cloud_multi = db.Column('arquitetura_cloud_multi', db.JSON, default=[])

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

    # JSON processing for arrays

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


#### Login ####

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Adicionado campo de nome de usuário
    password = db.Column(db.String(120), nullable=False)              # Adicionado campo de senha

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    # lógica da rota
    return render_template('profile.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        # Verifica se o usuário existe e se a senha está correta
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirecionar para o dashboard depois de fazer login
        else:
            # Caso contrário, retorna um erro (você pode personalizar isso conforme necessário)
            return "Usuário ou senha incorretos!", 401
    
    return render_template('login.html')


@app.route('/')
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

@app.route('/adicionar_projeto', methods=['GET', 'POST'])
def adicionar_projeto():
    try:
        if request.method == 'POST':
            # Obtendo dados do formulário
            data = request.form
            print(request.form)

            # Validação básica dos dados de entrada
            required_fields = ['nome', 'descricao', 'arquiteto']
            for field in required_fields:
                if field not in data:
                    return jsonify(success=False, error=f"Campo {field} ausente"), 400

            # Criando o objeto projeto com os dados recebidos
            projeto = Project(
                nome=data['nome'],
                descricao=data['descricao'],
                arquiteto=data['arquiteto'],
                compliance_projeto='compliance_projeto' in data,
                status_projeto=data['status_projeto'],
                debitos_tecnicos=data['debitos_tecnicos'],
                componentes_multi = request.form.getlist('componentes_multi[]'),
                tecnologias_multi=request.form.getlist('tecnologias_multi[]'),
                arquitetura_cloud_multi=request.form.getlist('arquitetura_cloud_multi[]')     
            )

            db.session.add(projeto)
            db.session.flush()
            
            print(request.form.getlist('componentes_multi'))
            print(request.form.getlist('tecnologias_multi'))
            print(request.form.getlist('arquitetura_cloud_multi'))


            # Processando os requirements
            all_requirements_ids = [r.id for r in CybersecurityRequirements.query.all()]
            for req_id in all_requirements_ids:
                req_id = int(req_id)
                requirement_key = 'requirement-' + str(req_id)
                if data.get(requirement_key) == 'on':
                    pr = ProjectCybersecurityRequirements(projeto_id=projeto.id, requirement_id=req_id, attainment=True)
                else:
                    pr = ProjectCybersecurityRequirements(projeto_id=projeto.id, requirement_id=req_id, attainment=False)
                db.session.add(pr)
            db.session.commit()
            return redirect(url_for('index'))
        requirements = CybersecurityRequirements.query.all()
        categories = CybersecurityCategories.query.all()
        return render_template('adicionar_projeto.html', categories=categories, requirements=requirements)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=f"Erro ao adicionar projeto: {str(e)}"), 500


@app.route('/excluir_projeto/<int:projeto_id>', methods=['POST'])
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



@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
def editar_projeto(projeto_id):
    projeto = Project.query.get_or_404(projeto_id)  # Se não encontrar o projeto, retorna 404

    if request.method == 'POST':
        try:
            # Atualizando os dados do projeto com base nos dados do formulário
            data = request.form

            projeto.nome = data['nome']
            projeto.descricao = data['descricao']
            projeto.arquiteto = data['arquiteto']
            projeto.compliance_projeto = 'compliance_projeto' in data
            projeto.status_projeto = data['status_projeto']
            projeto.debitos_tecnicos = data['debitos_tecnicos']
            projeto.componentes_multi = json.dumps(data.getlist('componentes_multi'))
            projeto.tecnologias_multi = json.dumps(data.getlist('tecnologias_multi'))
            projeto.arquitetura_cloud_multi = json.dumps(data.getlist('arquitetura_cloud_multi'))

            # Atualizando os requirements
            all_requirements_ids = [r.id for r in CybersecurityRequirements.query.all()]
            for req_id in all_requirements_ids:
                req_id = int(req_id)
                requirement_key = 'requirement-' + str(req_id)
                requirement_obj = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, requirement_id=req_id).first()

                if data.get(requirement_key) == 'on':
                    requirement_obj.attainment = True
                else:
                    requirement_obj.attainment = False

            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, error=f"Erro ao editar projeto: {str(e)}"), 500

    # Para o método GET:
    categories = CybersecurityCategories.query.all()
    requirements = CybersecurityRequirements.query.all()
    attained_requirements = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, attainment=True).all()
    not_attained_requirements = ProjectCybersecurityRequirements.query.filter_by(projeto_id=projeto_id, attainment=False).all()
    attained_requirement_ids = [req.requirement_id for req in attained_requirements]
    not_attained_requirement_ids = [req.requirement_id for req in not_attained_requirements]
    not_attained_requirement_names = [req.requirement.requirement_name for req in not_attained_requirements]

    return render_template('adicionar_projeto.html'
                           , categories=categories
                           , requirements=requirements
                           , projeto=projeto
                           , attained_requirement_ids=attained_requirement_ids
                           , not_attained_requirement=not_attained_requirements 
                           )

      
@app.route('/dados-do-banco', methods=['GET'])
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
        print(f"Total de projetos: {numero_de_projetos}")

        percentuais_categorias = {}
        for categoria, requirements in categorias.items():
            total_requisitos_por_projeto = len(requirements)
            total_requisitos = total_requisitos_por_projeto * numero_de_projetos

            print(f"\nCategoria: {categoria}")
            print(f"Total de requisitos por projeto: {total_requisitos_por_projeto}")
            print(f"Total de requisitos considerando todos os projetos: {total_requisitos}")

            # Calcular o número de requisitos não atendidos
            nao_atendidos = sum(requisitos_nao_verificados.get(requisito, 0) for requisito in requirements)
            print(f"Total de requisitos não atendidos: {nao_atendidos}")

            # Calcular o número de requisitos atendidos
            atendidos = total_requisitos - nao_atendidos
            print(f"Total de requisitos atendidos: {atendidos}")

            # Calcular a porcentagem de requisitos atendidos
            percentual_atendido = (atendidos / total_requisitos) * 100
            print(f"Porcentagem de requisitos atendidos: {percentual_atendido}%")

            percentuais_categorias[categoria] = round(percentual_atendido, 2)

        print("\nPercentuais finais por categoria:", percentuais_categorias)


           
        labels = list(requisitos_nao_verificados.keys())
        dados = list(requisitos_nao_verificados.values())
        requisitos_sum = sum(dados)
        
        return jsonify({'requisitos': requisitos_nao_verificados, 'labels': labels, 'dados': dados, 'requisitos_sum': requisitos_sum, 'percentuais_categorias':percentuais_categorias})

    except Exception as e:
        return abort(500, description=f"Erro ao buscar dados do banco: {str(e)}")


@app.route('/projeto/<int:projeto_id>', methods=['GET'])
def obter_dados_do_projeto(projeto_id):
    projeto = Project.query.get_or_404(projeto_id)  # Se não encontrar o projeto, retorna 404

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
                    'debitos_tecnicos':projeto.debitos_tecnicos,
                    'status_projeto' : projeto.status_projeto,
                    'fase' : projeto.fase,
                    'componentes_multi':projeto.componentes_multi,
                    'tecnologias_multi':projeto.tecnologias_multi,
                    'arquitetura_cloud_multi':projeto.arquitetura_cloud_multi
                },
                'categorias_avaliadas': [category.category_name for category in categories],
                'requirements': [req.requirement_name for req in requirements],
                'not_attained_requirements':not_attained_requirement_names,
            }
            formatted_json = json.dumps(response_data, indent=4, ensure_ascii=False)
            return Response(formatted_json, content_type='application/json; charset=utf-8')

        return render_template('adicionar_projeto.html'
                            , categories=categories
                            , requirements=requirements
                            , projeto=projeto
                            , attained_requirement_ids=attained_requirement_ids
                            , not_attained_requirement=not_attained_requirements 
                            )
    except Exception as e:
        return jsonify({'error': f"Erro ao buscar os dados: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

