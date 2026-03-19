from openai import OpenAI

client = OpenAI(
    base_url='http://127.0.0.1:1234/v1',
    api_key='lm-studio'
)

resposta_do_llm = client.chat.completions.create(
    model='openai/gpt-oss-20b', 
    messages=[
        {'role':'system', 'content': 'Você é um especialista em Python, possuindo conhecimento desde o inicio da linguagem e acompanhou toda a evolução, com isso hoje você utiliza o python puro para montar os códigos com o máximo de otimização conhecido pelas linguagens que moldaram o Python'},
        {'role':'user', 'content': 'Qual é o seu último modelo de Python que tem de conhecimento?'}
    ], 
    temperature=0.5
)

print(resposta_do_llm.choices[0].message.content)
