from key import API_KEY
import requests
import json
import os
import urllib3
import argparse
import json
import pdfkit  # biblioteca para gerar PDFs

def generate_threat_modeling_report(json_data):
    
    if not json_data:
        raise ValueError("The JSON data is empty.")
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {"Authorization": f"Bearer {API_KEY}", 
           "Content-Type":"application/json"
           }
    
    # Extract not_attained_requirements, components, technologies, and cloud_architecture from json_data
    nome_do_projeto = json_data['projeto']['nome']    
    descricao = json_data['projeto']['descricao']
    not_attained_requirements = json_data['not_attained_requirements']
    components = json_data['projeto']['componentes_multi']
    technologies = json_data['projeto']['tecnologias_multi']
    cloud_architecture = json_data['projeto']['arquitetura_cloud_multi']
    

    # Prepare the prompt for OpenAI
    
    response = {
        "model":"gpt-3.5-turbo",
        "messages":[ 
            {
            "role": "system",
            "content": "Identifique ameaças, vulnerabilidades, avaliação de riscos e estratégias de mitigação com base nos dados do projeto. A resposta deve estar estruturada como um relatório."
            },
            {
            "role": "user",
            "content": f"Nome do Projeto:{nome_do_projeto}, Descrição:{descricao} ,Componentes:{components},Tecnologias:{technologies},Arquitetura:{cloud_architecture},Requisitos Não Atendidos:{not_attained_requirements}"
            },
            {
            "role": "assistant",
            "content": "Ameaças Identificadas:\n- Falta de Criptografia de Dados, Classificação de Dados, Políticas de Retenção de Dados, Firewalls/IPS, e Segmentação de Redes.\n\nVulnerabilidades:\n- Acesso não autorizado, retenção inadequada ou eliminação prematura de dados, exposição a ataques de rede.\n\nAvaliação de Riscos:\n- Alto risco de exposição de informações sensíveis, comprometimento da infraestrutura de rede, acesso não autorizado a áreas restritas.\n\nEstratégia de Mitigação e Controles:\n- Implementar Criptografia, Classificação de Dados, Políticas de Retenção, Firewalls/IPS, e Segmentação de Redes."
            }
        ],
        "temperature":1,
        "max_tokens":3000,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
    }

    # Send the request to the OpenAI API
    body_mensagem = json.dumps(response)
    response = requests.post(url, headers=headers, data= body_mensagem)
    response_json = response.json()
    print
    
    # Extract and format the threat modeling report from the response
    report = "### Threat Modeling Report ###\n\n"
    report_content = response_json['choices'][0]['message']['content']
    report += report_content.encode('utf-8').decode('utf-8')
    return report

