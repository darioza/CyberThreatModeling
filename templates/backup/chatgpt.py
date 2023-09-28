from key import API_KEY
import requests
import json
import os
import urllib3


systems = []

headers = {"Authorization": f"Bearer {API_KEY}", 
           "Content-Type":"application/json"
           }
link = "https://api.openai.com/v1/chat/completions"

response = {
  "model": "gpt-3.5-turbo-16k",
  "messages": [
    {
      "role": "system",
      "content": "You will be provided with unstructured data, and your task is to parse it into JSON format."
    },
    {
      "role": "user",
      "content": f"Você é um especialista em datas de End Of Life (EOL) de sistemas. Dada a lista de sistemas e aplicações abaixo, forneça as datas REAIS de término do Suporte Estendido (EOL) no formato \"dd/mm/aaaa\". Retorne as informações no formato JSON:\n\nLista\n\n{systems}"
    },
    {
      "role": "assistant",
      "content": "{\n  \"systems\": [\n    {\n      \"name\": \"Windows 2012R2\",\n      \"eol_date\": \"14/10/2023\"\n    },\n    {\n      \"name\": \"RedHat Enterprise 8.6\",\n      \"eol_date\": \"31/05/2029\"\n    }\n  ]\n}"
    }
  ],
  "temperature": 0,
  "max_tokens": 256,
  "top_p": 0.5,
  "frequency_penalty": 0,
  "presence_penalty": 0
}

body_mensagem = json.dumps(response)
requisicao = requests.post(link, headers=headers, data=body_mensagem)

# Converta a resposta em JSON:
response_data = requisicao.json()

# Imprimindo a resposta
print(response_data['choices'][0]['message']['content'])

    
    
