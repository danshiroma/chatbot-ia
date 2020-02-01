# Integrantes
Danilo Shiroma 201719070806
Dawson Paiva Lima 201719070016

# Estrutura de arquivos enviada
    - chatbot-standalone.py: Para testes locais sem nenhuma integração, apenas executar e interagir com o BOT
    - chatbot-telegram.py: Integrado com o Telegram. Para testar procure pelo usuário "EspacoShiromaBot" no telegram, execute
        o arquivo para realizar o teste
    - dataset_intencao_frase.txt: contém as frases e suas respectivas intenções usados no treinamento
    - etiquetadores.txt: etiquetas de entidades identificadas para o tema escolhido no trabalho

# Exemplo de um diálogo
    Ola tudo bem - (retorna intenção saudacao)
    Como é o espaço de vcs? - (retorna intenção sobre_espaco)
    Qual o valor cobrado pelo local? - (retorna intenção forma_pagamento)
    Quais as formas de pagamento? - (retorna intenção forma_pagamento)
    Podemos agendar uma visita para conhecer o local? - (retorna intenção visita)

# Por padrão o Whatsapp envia os logs das conversas com o nome ou então o número do cliente. Alteramos em todos os logs para que tais informações não fossem mostradas. Assim os clientes são referenciados como "Cliente".