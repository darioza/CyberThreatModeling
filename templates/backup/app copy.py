from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap5
from flask import Flask, jsonify
from sqlalchemy import inspect  # Importe a função inspect
import json
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import ARRAY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)
app.static_folder = 'static'

# Modelo de dados para Projetos
class Projeto(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    arquiteto = db.Column(db.String(100), nullable=False)  # Adequação para incluir arquiteto

    # Adequação para incluir todos os campos correspondentes à tabela de projetos
    compliance_projeto = db.Column(db.Boolean)
    debitos_tecnicos = db.Column(db.String(100), nullable=False)
    status_projeto = db.Column(db.Text, default=False)
    componentes_multi = db.Column('componentes_multi', db.Text, default='[]')
    tecnologias_multi = db.Column('tecnologias_multi', db.Text, default='[]')
    arquitetura_cloud_multi = db.Column('arquitetura_cloud_multi', db.Text, default='[]')


    
    requisitocybersecurity_autenticacaomultifatorial = db.Column(db.Boolean, default=True)
    requisitocybersecurity_gestaodequestionidentquestionidades = db.Column(db.Boolean, default=True)
    requisitocybersecurity_controledeacessoroles = db.Column(db.Boolean, default=True)
    requisitocybersecurity_criptografiadedados = db.Column(db.Boolean, default=True)
    requisitocybersecurity_classificacaodedados = db.Column(db.Boolean, default=True)
    requisitocybersecurity_politicasderetencaodedados = db.Column(db.Boolean, default=True)
    requisitocybersecurity_firewalls_ips = db.Column(db.Boolean, default=True)
    requisitocybersecurity_segmentacaoderedes = db.Column(db.Boolean, default=True)
    requisitocybersecurity_protecaocontrados = db.Column(db.Boolean, default=True)
    requisitocybersecurity_monitoramentodelogs = db.Column(db.Boolean, default=True)
    requisitocybersecurity_sistemas_questionids_edr = db.Column(db.Boolean, default=True)
    requisitocybersecurity_planoderesposta = db.Column(db.Boolean, default=True)
    requisitocybersecurity_scannersdevulnerabilquestionidades = db.Column(db.Boolean, default=True)
    requisitocybersecurity_patchmanagement = db.Column(db.Boolean, default=True)
    requisitocybersecurity_testesdepenetracao = db.Column(db.Boolean, default=True)
    requisitocybersecurity_desenvolvimentoseguro = db.Column(db.Boolean, default=True)
    requisitocybersecurity_waf = db.Column(db.Boolean, default=True)
    requisitocybersecurity_protecaocontraataquescomuns = db.Column(db.Boolean, default=True)
    requisitocybersecurity_controlesdeacessofisico = db.Column(db.Boolean, default=True)
    requisitocybersecurity_protecaocontradesastres = db.Column(db.Boolean, default=True)
    requisitocybersecurity_monitoramentofisico = db.Column(db.Boolean, default=True)
    requisitocybersecurity_programasdeconscientizacao = db.Column(db.Boolean, default=True)
    requisitocybersecurity_treinamentoregular = db.Column(db.Boolean, default=True)
    requisitocybersecurity_politicasdeseguranca = db.Column(db.Boolean, default=True)
    requisitocybersecurity_avaliacoesderisco = db.Column(db.Boolean, default=True)
    requisitocybersecurity_auditoriasconformquestionidade = db.Column(db.Boolean, default=True)
    requisitocybersecurity_backups = db.Column(db.Boolean, default=True)
    requisitocybersecurity_planosderecuperacao = db.Column(db.Boolean, default=True)

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

@app.route('/')
def index():
    projetos = Projeto.query.all()
    
    # Obter dados do banco
    response = obter_dados_do_banco()
    
    # Supondo que a função obter_dados_do_banco retorne um objeto JSON, converta-o em um dicionário Python
    dados_do_banco = json.loads(response.data)
    
    return render_template('index.html', projetos=projetos, dados=dados_do_banco["dados"], requisitos_sum=dados_do_banco["requisitos_sum"])

@app.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')


@app.route('/adicionar_projeto', methods=['GET', 'POST'])
def adicionar_projeto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        arquiteto = request.form['arquiteto']
        compliance_projeto = 'compliance_projeto' in request.form
        status_projeto = 'status_projeto' in request.form
        debitos_tecnicos = request.form['debitos_tecnicos']
        
        componentes_multi = request.form.getlist('componentes_multi')
        tecnologias_multi = request.form.getlist('tecnologias_multi')
        arquitetura_cloud_multi = request.form.getlist('arquitetura_cloud_multi')

        requisitocybersecurity_autenticacaomultifatorial = 'requisitocybersecurity_autenticacaomultifatorial' in request.form
        requisitocybersecurity_gestaodequestionidentquestionidades = 'requisitocybersecurity_gestaodequestionidentquestionidades' in request.form
        requisitocybersecurity_controledeacessoroles = 'requisitocybersecurity_controledeacessoroles' in request.form
        requisitocybersecurity_criptografiadedados = 'requisitocybersecurity_criptografiadedados' in request.form
        requisitocybersecurity_classificacaodedados = 'requisitocybersecurity_classificacaodedados' in request.form
        requisitocybersecurity_politicasderetencaodedados = 'requisitocybersecurity_politicasderetencaodedados' in request.form
        requisitocybersecurity_firewalls_ips = 'requisitocybersecurity_firewalls_ips' in request.form
        requisitocybersecurity_segmentacaoderedes = 'requisitocybersecurity_segmentacaoderedes' in request.form
        requisitocybersecurity_protecaocontrados = 'requisitocybersecurity_protecaocontrados' in request.form
        requisitocybersecurity_monitoramentodelogs = 'requisitocybersecurity_monitoramentodelogs' in request.form
        requisitocybersecurity_sistemas_questionids_edr = 'requisitocybersecurity_sistemas_questionids_edr' in request.form
        requisitocybersecurity_planoderesposta = 'requisitocybersecurity_planoderesposta' in request.form
        requisitocybersecurity_scannersdevulnerabilquestionidades = 'requisitocybersecurity_scannersdevulnerabilquestionidades' in request.form
        requisitocybersecurity_patchmanagement = 'requisitocybersecurity_patchmanagement' in request.form
        requisitocybersecurity_testesdepenetracao = 'requisitocybersecurity_testesdepenetracao' in request.form
        requisitocybersecurity_desenvolvimentoseguro = 'requisitocybersecurity_desenvolvimentoseguro' in request.form
        requisitocybersecurity_waf = 'requisitocybersecurity_waf' in request.form
        requisitocybersecurity_protecaocontraataquescomuns = 'requisitocybersecurity_protecaocontraataquescomuns' in request.form
        requisitocybersecurity_controlesdeacessofisico = 'requisitocybersecurity_controlesdeacessofisico' in request.form
        requisitocybersecurity_protecaocontradesastres = 'requisitocybersecurity_protecaocontradesastres' in request.form
        requisitocybersecurity_monitoramentofisico = 'requisitocybersecurity_monitoramentofisico' in request.form
        requisitocybersecurity_programasdeconscientizacao = 'requisitocybersecurity_programasdeconscientizacao' in request.form
        requisitocybersecurity_treinamentoregular = 'requisitocybersecurity_treinamentoregular' in request.form
        requisitocybersecurity_politicasdeseguranca = 'requisitocybersecurity_politicasdeseguranca' in request.form
        requisitocybersecurity_avaliacoesderisco = 'requisitocybersecurity_avaliacoesderisco' in request.form
        requisitocybersecurity_auditoriasconformquestionidade = 'requisitocybersecurity_auditoriasconformquestionidade' in request.form
        requisitocybersecurity_backups = 'requisitocybersecurity_backups' in request.form
        requisitocybersecurity_planosderecuperacao = 'requisitocybersecurity_planosderecuperacao' in request.form

        projeto = Projeto(
            nome=nome,
            descricao=descricao,
            arquiteto=arquiteto,
            compliance_projeto=compliance_projeto,
            debitos_tecnicos=debitos_tecnicos,
            status_projeto=status_projeto,

            componentes_multi=componentes_multi,
            tecnologias_multi=tecnologias_multi,
            arquitetura_cloud_multi=arquitetura_cloud_multi,

            requisitocybersecurity_autenticacaomultifatorial=requisitocybersecurity_autenticacaomultifatorial,
            requisitocybersecurity_gestaodequestionidentquestionidades=requisitocybersecurity_gestaodequestionidentquestionidades,
            requisitocybersecurity_controledeacessoroles=requisitocybersecurity_controledeacessoroles,
            requisitocybersecurity_criptografiadedados=requisitocybersecurity_criptografiadedados,
            requisitocybersecurity_classificacaodedados=requisitocybersecurity_classificacaodedados,
            requisitocybersecurity_politicasderetencaodedados=requisitocybersecurity_politicasderetencaodedados,
            requisitocybersecurity_firewalls_ips=requisitocybersecurity_firewalls_ips,
            requisitocybersecurity_segmentacaoderedes=requisitocybersecurity_segmentacaoderedes,
            requisitocybersecurity_protecaocontrados=requisitocybersecurity_protecaocontrados,
            requisitocybersecurity_monitoramentodelogs=requisitocybersecurity_monitoramentodelogs,
            requisitocybersecurity_sistemas_questionids_edr=requisitocybersecurity_sistemas_questionids_edr,
            requisitocybersecurity_planoderesposta=requisitocybersecurity_planoderesposta,
            requisitocybersecurity_scannersdevulnerabilquestionidades=requisitocybersecurity_scannersdevulnerabilquestionidades,
            requisitocybersecurity_patchmanagement=requisitocybersecurity_patchmanagement,
            requisitocybersecurity_testesdepenetracao=requisitocybersecurity_testesdepenetracao,
            requisitocybersecurity_desenvolvimentoseguro=requisitocybersecurity_desenvolvimentoseguro,
            requisitocybersecurity_waf=requisitocybersecurity_waf,
            requisitocybersecurity_protecaocontraataquescomuns=requisitocybersecurity_protecaocontraataquescomuns,
            requisitocybersecurity_controlesdeacessofisico=requisitocybersecurity_controlesdeacessofisico,
            requisitocybersecurity_protecaocontradesastres=requisitocybersecurity_protecaocontradesastres,
            requisitocybersecurity_monitoramentofisico=requisitocybersecurity_monitoramentofisico,
            requisitocybersecurity_programasdeconscientizacao=requisitocybersecurity_programasdeconscientizacao,
            requisitocybersecurity_treinamentoregular=requisitocybersecurity_treinamentoregular,
            requisitocybersecurity_politicasdeseguranca=requisitocybersecurity_politicasdeseguranca,
            requisitocybersecurity_avaliacoesderisco=requisitocybersecurity_avaliacoesderisco,
            requisitocybersecurity_auditoriasconformquestionidade=requisitocybersecurity_auditoriasconformquestionidade,
            requisitocybersecurity_backups=requisitocybersecurity_backups,
            requisitocybersecurity_planosderecuperacao=requisitocybersecurity_planosderecuperacao,
        )
        
        db.session.add(projeto)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adicionar_projeto.html')

@app.route('/dados-do-banco', methods=['GET'])
def obter_dados_do_banco():
    # Consulte o banco de dados para obter todos os projetos
    projetos = Projeto.query.all()
    
    # Crie um dicionário para armazenar a contagem de requisitos de segurança cibernética não verificados
    requisitos_nao_verificados = {
        'Autenticação Multifatorial': 0,
        'Gestão de Identidades': 0,
        'Controle de Acesso': 0,
        'Criptografia de Dados': 0,
        'Classificação de Dados': 0,
        'Políticas de Retenção de Dados': 0,
        'Firewalls/IPS': 0,
        'Segmentação de Redes': 0,
        'Proteção contra DDoS': 0,
        'Monitoramento de Logs': 0,
        'Sistemas IDS/EDR': 0,
        'Plano de Resposta': 0,
        'Scanners de Vulnerabilidades': 0,
        'Patch Management': 0,
        'Testes de Penetração': 0,
        'Desenvolvimento Seguro': 0,
        'WAF': 0,
        'Proteção contra Ataques Comuns': 0,
        'Controles de Acesso Físico': 0,
        'Proteção contra Desastres': 0,
        'Monitoramento Físico': 0,
        'Programas de Conscientização': 0,
        'Treinamento Regular': 0,
        'Políticas de Segurança': 0,
        'Avaliações de Risco': 0,
        'Auditorias de Conformidade': 0,
        'Backups': 0,
        'Planos de Recuperação': 0
    }
    
    mapeamento={
                'Autenticação Multifatorial': 'requisitocybersecurity_autenticacaomultifatorial',
                'Gestão de Identidades': 'requisitocybersecurity_gestaodequestionidentquestionidades',
                'Controle de Acesso': 'requisitocybersecurity_controledeacessoroles',
                'Criptografia de Dados': 'requisitocybersecurity_criptografiadedados',
                'Classificação de Dados': 'requisitocybersecurity_classificacaodedados',
                'Políticas de Retenção de Dados': 'requisitocybersecurity_politicasderetencaodedados',
                'Firewalls/IPS':'requisitocybersecurity_firewalls_ips',
                'Segmentação de Redes':'requisitocybersecurity_segmentacaoderedes',
                'Proteção contra DDoS':'requisitocybersecurity_protecaocontrados',
                'Monitoramento de Logs':'requisitocybersecurity_monitoramentodelogs',
                'Sistemas IDS/EDR':'requisitocybersecurity_sistemas_questionids_edr',
                'Plano de Resposta': 'requisitocybersecurity_planoderesposta',
                'Scanners de Vulnerabilidades':'requisitocybersecurity_scannersdevulnerabilquestionidades',
                'Patch Management': 'requisitocybersecurity_patchmanagement',
                'Testes de Penetração': 'requisitocybersecurity_testesdepenetracao',
                'Desenvolvimento Seguro': 'requisitocybersecurity_desenvolvimentoseguro',
                'WAF': 'requisitocybersecurity_waf',
                'Proteção contra Ataques Comuns': 'requisitocybersecurity_protecaocontraataquescomuns',
                'Controles de Acesso Físico': 'requisitocybersecurity_controlesdeacessofisico',
                'Proteção contra Desastres': 'requisitocybersecurity_protecaocontradesastres',
                'Monitoramento Físico': 'requisitocybersecurity_monitoramentofisico',
                'Programas de Conscientização': 'requisitocybersecurity_programasdeconscientizacao',
                'Treinamento Regular': 'requisitocybersecurity_treinamentoregular',
                'Políticas de Segurança': 'requisitocybersecurity_politicasdeseguranca',
                'Avaliações de Risco': 'requisitocybersecurity_avaliacoesderisco',
                'Auditorias de Conformidade': 'requisitocybersecurity_auditoriasconformquestionidade',
                'Backups': 'requisitocybersecurity_backups',
                'Planos de Recuperação': 'requisitocybersecurity_planosderecuperacao'
    }

      # Percorra todos os projetos
    for projeto in projetos:
        # Use o dicionário de mapeamento para verificar e atualizar a contagem de requisitos não verificados
        for key, attribute in mapeamento.items():
            if not getattr(projeto, attribute):
                requisitos_nao_verificados[key] += 1
    
    # Crie listas de rótulos e dados para o gráfico
    labels = list(requisitos_nao_verificados.keys())
    dados = list(requisitos_nao_verificados.values())
    requisitos_sum = sum(dados)
    
    return jsonify({'labels': labels, 'dados': dados, 'requisitos_sum': requisitos_sum})

# Rota para obter os dados de um projeto pelo ID
@app.route('/projeto/<int:projeto_id>', methods=['GET'])
def obter_dados_do_projeto(projeto_id):
    try:
        projeto = Projeto.query.get(projeto_id)
        if projeto is None:
            return jsonify({'error': 'Projeto não encontrado'}), 404

        # Crie um dicionário para armazenar os dados do projeto
        dados_projeto = {
            'dados_basicos': {
                'id': projeto.id,
                'nome': projeto.nome,
                'descricao': projeto.descricao,
                'arquiteto': projeto.arquiteto,
                'compliance_projeto': projeto.compliance_projeto,
                'debitos_tecnicos': projeto.debitos_tecnicos,
            },
            'componentes': {
                'componentes_multi': projeto.componentes_multi,
            },
            'tecnologias': {
                'tecnologias_multi': projeto.tecnologias_multi,
            },
            'arquitetura': {
                'arquitetura_cloud_multi': projeto.arquitetura_cloud_multi,
            },
            'requisitos_cybersecurity': {
                'autenticacao_multifatorial': projeto.requisitocybersecurity_autenticacaomultifatorial,
                'gestao_de_identidades': projeto.requisitocybersecurity_gestaodequestionidentquestionidades,
                'controle_de_acesso': projeto.requisitocybersecurity_controledeacessoroles,
                'criptografia_de_dados': projeto.requisitocybersecurity_criptografiadedados,
                'classificacao_de_dados': projeto.requisitocybersecurity_classificacaodedados,
                'politicas_de_retencao_de_dados': projeto.requisitocybersecurity_politicasderetencaodedados,
                'firewalls_ips': projeto.requisitocybersecurity_firewalls_ips,
                'segmentacao_de_redes': projeto.requisitocybersecurity_segmentacaoderedes,
                'protecao_contra_ddos': projeto.requisitocybersecurity_protecaocontrados,
                'monitoramento_de_logs': projeto.requisitocybersecurity_monitoramentodelogs,
                'sistemas_ids_edr': projeto.requisitocybersecurity_sistemas_questionids_edr,
                'plano_de_resposta': projeto.requisitocybersecurity_planoderesposta,
                'scanners_de_vulnerabilidades': projeto.requisitocybersecurity_scannersdevulnerabilquestionidades,
                'patch_management': projeto.requisitocybersecurity_patchmanagement,
                'testes_de_penetracao': projeto.requisitocybersecurity_testesdepenetracao,
                'desenvolvimento_seguro': projeto.requisitocybersecurity_desenvolvimentoseguro,
                'waf': projeto.requisitocybersecurity_waf,
                'protecao_contra_ataques_comuns': projeto.requisitocybersecurity_protecaocontraataquescomuns,
                'controles_de_acesso_fisico': projeto.requisitocybersecurity_controlesdeacessofisico,
                'protecao_contra_desastres': projeto.requisitocybersecurity_protecaocontradesastres,
                'monitoramento_fisico': projeto.requisitocybersecurity_monitoramentofisico,
                'programas_de_conscientizacao': projeto.requisitocybersecurity_programasdeconscientizacao,
                'treinamento_regular': projeto.requisitocybersecurity_treinamentoregular,
                'politicas_de_seguranca': projeto.requisitocybersecurity_politicasdeseguranca,
                'avaliacoes_de_risco': projeto.requisitocybersecurity_avaliacoesderisco,
                'auditorias_de_conformidade': projeto.requisitocybersecurity_auditoriasconformquestionidade,
                'backups': projeto.requisitocybersecurity_backups,
                'planos_de_recuperacao': projeto.requisitocybersecurity_planosderecuperacao,
            }
        }
        dados_projeto = projeto.to_dict()
        return jsonify(dados_projeto), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

