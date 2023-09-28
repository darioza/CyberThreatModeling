 # Projeto de Segurança Cibernética - CyberThreat Modeling

Este projeto fornece uma ferramenta para arquitetos de segurança cibernética gerenciarem seus projetos e requisitos de segurança. O projeto consiste em um aplicativo Flask e um banco de dados SQLite.

###Pré-requisitos

Para executar este projeto, você precisará dos seguintes pré-requisitos:

* Python 3.6 ou superior
* Flask
* SQLAlchemy
* Flask-Login
* Flask-Admin
* Flask-Bootstrap5
* open_ai
* requests

###Instalação

Para instalar o projeto, siga estas etapas:

1. Clone o repositório do projeto:

```
git clone https://github.com/seu-nome-de-usuario/Cyber-Threat-Modeling.git
```

2. Instale os requisitos do projeto:

```
pip install -r requirements.txt
```

3. Crie um banco de dados SQLite:

```
sqlite3 projeto.db
```

4. Execute as seguintes instruções SQL para criar as tabelas do banco de dados:

```
CREATE TABLE CybersecurityCategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE CybersecurityRequirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requirement_name VARCHAR(255) NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES CybersecurityCategories(id)
);

CREATE TABLE Project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    arquiteto_id INTEGER NOT NULL,
    compliance_projeto BOOLEAN,
    debitos_tecnicos VARCHAR(100) NOT NULL,
    status_projeto TEXT NOT NULL,
    componentes_multi JSON DEFAULT [],
    tecnologias_multi JSON DEFAULT [],
    arquitetura_cloud_multi JSON DEFAULT [],
    modelagem_ameacas TEXT NOT NULL,
    FOREIGN KEY (arquiteto_id) REFERENCES User(id)
);

CREATE TABLE ProjectCybersecurityRequirements (
    projeto_id INTEGER NOT NULL,
    requirement_id INTEGER NOT NULL,
    attainment BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (projeto_id, requirement_id),
    FOREIGN KEY (projeto_id) REFERENCES Project(id),

