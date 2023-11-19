

# Projeto de Segurança Cibernética - CyberThreat Modeling

<div align="center">
    <img src="https://github.com/darioza/CyberThreatModeling/assets/24236687/92dc5807-6b8c-497b-a44c-a0d628fc616c" alt="CTM" width="100"/>
</div>

![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-2.x-blue.svg)

## Índice
- [Descrição do Projeto](#descrição-do-projeto)
- [Status do Projeto](#status-do-projeto)
- [Funcionalidades e Demonstração](#funcionalidades-e-demonstração)
- [Acesso ao Projeto](#acesso-ao-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Contribuir](#como-contribuir)
- [Desenvolvedores do Projeto](#desenvolvedores-do-projeto)
- [Licença](#licença)

## Descrição do Projeto

O CyberThreat Modeling é uma ferramenta inovadora projetada para arquitetos de segurança cibernética. Este projeto, desenvolvido com Flask e um banco de dados SQLite, oferece uma plataforma robusta para gerenciamento de projetos de segurança cibernética, permitindo aos usuários modelar ameaças, avaliar riscos, gerenciar vulnerabilidades e débitos técnicos, e criar relatórios detalhados.

## Status do Projeto
🚧 Em desenvolvimento 🚧

## Funcionalidades e Demonstração
- **Gestão de Projetos**: Cadastro e gerenciamento de projetos de segurança cibernética.
- **Modelagem de Ameaças**: Ferramentas para modelagem e avaliação de ameaças.
- **Gestão de Requisitos de Segurança**: Interface para gerenciar requisitos de segurança específicos.
- **Avaliação de Riscos**: Auxilia na identificação e avaliação de riscos associados a cada projeto.
- **Gestão de Vulnerabilidades e Débitos Técnicos**: Oferece ferramentas para gerenciar vulnerabilidades e débitos técnicos de forma eficiente.
- **Geração de Relatórios**: Cria relatórios detalhados, apoiados por inteligência artificial, para uma análise aprofundada da segurança.
- **Demonstração**: [Clique aqui](https://www.cyberthreatmodeling.com.br/) para ver a demonstração.



## Como Contribuir

Para contribuir com o projeto, siga estas etapas:

- Faça um fork do repositório.
- Crie uma branch para sua feature (git checkout -b feature/novaFeature).
- Faça suas alterações e commit (git commit -am 'Adicionando uma nova feature').
- Push para a branch (git push origin feature/novaFeature).
- Abra um Pull Request.

## Onde Encontrar Ajuda

Se você tiver dúvidas ou precisar de assistência, pode:

- Abrir uma issue no GitHub para questões específicas.
- Entrar em contato com a equipe de suporte através do email daniel.arioza@gmail.com.

## Desenvolvedores do Projeto
Daniel Arioza - Arquiteto de Cybersecurity e Desenvolvedor Principal (https://www.linkedin.com/in/daniel-arioza/)

## Acesso ao Projeto
Para acessar o projeto, clone o repositório e siga as instruções de instalação:

## Tecnologias Utilizadas

Para executar este projeto, você precisará dos seguintes pré-requisitos:

* Python 3.6 ou superior
* Flask
* SQLAlchemy
* Flask-Login
* Flask-Admin
* Flask-Bootstrap5
* open_ai
* requests

## Instalação

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



