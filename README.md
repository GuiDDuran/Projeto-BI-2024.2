# Projeto de Pesquisa e Entrevistas - Banco de Dados

Este projeto foi desenvolvido para gerenciar pesquisas e entrevistas, incluindo o cadastro de entrevistados, suas informações pessoais, perguntas e respostas das pesquisas, além de controle de dados relacionados a telefones e endereços. O banco de dados foi modelado para ser escalável, seguro e de fácil manutenção.

## Estrutura do Projeto

O banco de dados é composto por várias tabelas interrelacionadas que permitem armazenar informações detalhadas sobre pesquisas, entrevistados e suas respectivas respostas. Abaixo estão as tabelas principais e suas descrições:

### 1. **Tabela `pesquisa`**
Armazena os detalhes de cada pesquisa cadastrada, como nome, datas de início e término, e se está ativa.

- `pesquisa_id`: Chave primária.
- `pesquisa_nome`: Nome da pesquisa.
- `data_inicio`: Data de início da pesquisa.
- `data_fim`: Data de término da pesquisa.
- `data_cadastro`: Data de cadastro do registro.
- `ativo`: Indica se a pesquisa está ativa (exclusão lógica).

### 2. **Tabela `pesquisa_pergunta_tipo`**
Define os tipos de perguntas que podem ser associados às pesquisas, como "Múltipla Escolha", "Resposta Aberta", etc.

- `pesquisa_pergunta_tipo_id`: Chave primária.
- `pesquisa_pergunta_tipo`: Descrição do tipo de pergunta.
- `data_cadastro`: Data de cadastro do tipo.
- `ativo`: Indica se o tipo de pergunta está ativo (exclusão lógica).

### 3. **Tabela `pesquisa_pergunta`**
Armazena as perguntas associadas a uma pesquisa específica.

- `pesquisa_pergunta_id`: Chave primária.
- `pesquisa_id`: Chave estrangeira que se refere à tabela `pesquisa`.
- `pesquisa_pergunta_tipo_id`: Chave estrangeira que se refere à tabela `pesquisa_pergunta_tipo`.
- `data_cadastro`: Data de cadastro da pergunta.
- `ativo`: Indica se a pergunta está ativa (exclusão lógica).

### 4. **Tabela `genero`**
Armazena as diferentes opções de gênero disponíveis para os entrevistados.

- `genero_id`: Chave primária.
- `genero`: Descrição do gênero.

### 5. **Tabela `entrevistado`**
Armazena as informações pessoais dos entrevistados, como nome, email, data de nascimento, gênero, entre outros.

- `entrevistado_id`: Chave primária.
- `entrevistado_nome`: Nome completo do entrevistado.
- `entrevistado_email`: Email do entrevistado.
- `entrevistado_nome_social`: Nome social (se aplicável).
- `entrevistado_data_nascimento`: Data de nascimento do entrevistado.
- `sexo`: Sexo do entrevistado (M, F ou O).
- `genero_id`: Chave estrangeira que se refere à tabela `genero`.
- `data_cadastro`: Data de cadastro do entrevistado.

### 6. **Tabela `telefone_tipo`**
Armazena os diferentes tipos de telefones (ex.: Celular, Fixo).

- `telefone_tipo_id`: Chave primária.
- `telefone_tipo`: Descrição do tipo de telefone.
- `ativo`: Indica se o tipo está ativo (exclusão lógica).

### 7. **Tabela `entrevistado_telefone`**
Armazena os números de telefone associados aos entrevistados, permitindo múltiplos números por entrevistado.

- `entrevistado_telefone_id`: Chave primária.
- `entrevistado_id`: Chave estrangeira que se refere à tabela `entrevistado`.
- `ddi`: Código de discagem internacional (padrão 55 para o Brasil).
- `ddd`: Código de discagem da área (ex.: 11 para São Paulo).
- `telefone`: Número de telefone.
- `telefone_tipo_id`: Chave estrangeira que se refere à tabela `telefone_tipo`.
- `eh_telefone_principal`: Indica se o telefone é o principal.
- `data_cadastro`: Data de cadastro do telefone.
- `ativo`: Indica se o telefone está ativo (exclusão lógica).

### 8. **Tabela `pergunta_resposta`**
Armazena as respostas dadas pelos entrevistados às perguntas da pesquisa.

- `pergunta_resposta_id`: Chave primária.
- `pesquisa_pergunta_id`: Chave estrangeira que se refere à tabela `pesquisa_pergunta`.
- `entrevistado_id`: Chave estrangeira que se refere à tabela `entrevistado`.
- `resposta`: Resposta fornecida pelo entrevistado.
- `data_cadastro`: Data de cadastro da resposta.

### 9. **Tabela `pesquisa_pergunta_opcao`**
Armazena as opções de respostas para perguntas do tipo "Múltipla Escolha".

- `pesquisa_pergunta_opcao_id`: Chave primária.
- `pesquisa_pergunta_id`: Chave estrangeira que se refere à tabela `pesquisa_pergunta`.
- `indice`: Ordem da opção de resposta.
- `opcao`: Texto da opção.
- `data_cadastro`: Data de cadastro da opção.
- `ativo`: Indica se a opção está ativa (exclusão lógica).

### 10. **Tabela `entrevistado_endereco`**
Armazena os endereços dos entrevistados.

- `entrevistado_endereco_id`: Chave primária.
- `entrevistado_id`: Chave estrangeira que se refere à tabela `entrevistado`.
- `logradouro`: Logradouro do endereço (ex.: Rua, Avenida).
- `numero`: Número do endereço.
- `complemento`: Complemento (ex.: bloco, apartamento).
- `bairro`: Bairro.
- `cidade`: Cidade.
- `uf`: Unidade Federativa (Estado) representada por sigla.
- `cep`: Código de Endereçamento Postal (CEP).
- `descricao`: Descrição adicional do endereço (ex.: Casa, Trabalho).

### 11. **Etapa de Transferência de Dados Transacional**
Organiza a transferência dos dados transacionais para a stage area, garantindo que a base transacional permaneça intacta e preservada.

- Extração de Dados: Realiza a extração dos dados do banco transacional utilizando um script em Python.
- Transferência Stage: Transfere os dados extraídos para stage area, onde podem ser processados sem afetar o banco transacional.
- Preservação Transacional: Garante que o ambiente transacional fique isolado de operações pesadas, mantendo sua integridade e desempenho.
- Processamento Stage: Realiza o processamento e transformações necessárias na stage, preservando a performance do ambiente original.
- Validação Dados: Executa a validação dos dados após as transformações, assegurando consistência para uso nas próximas análises.

### 12. **Levantamento de Perguntas** 
Para o desenvolvimento do sistema de entrevista, foi realizado um levantamento criterioso das perguntas que seriam incluídas, adaptando-as ao contexto da comunidade local na ilha. O processo seguiu as etapas abaixo:

- Modelagem Inicial das Perguntas: Utilizamos como base o modelo de perguntas fornecido pelo IBGE. Esse modelo serviu de referência inicial, considerando que já contempla uma estrutura sólida e bem estabelecida para entrevistas de levantamento de dados demográficos e socioeconômicos.

- Adequação ao Contexto Local: Para garantir que o questionário estivesse alinhado com a realidade da ilha, realizamos uma entrevista com a representante local. Durante essa reunião, ela nos ajudou a ajustar as perguntas de acordo com a situação específica da comunidade. Por exemplo, eliminamos questões sobre serviços de saúde e segurança, uma vez que esses serviços não estão presentes na ilha.

- Filtragem e Seleção das Perguntas: Após as observações da representante local, procedemos com uma nova filtragem do questionário. Essa etapa teve como objetivo garantir que cada pergunta fosse relevante e estivesse contextualizada com a realidade local.

- Definição dos Tipos de Resposta: Cada pergunta foi então analisada para determinar o tipo de resposta mais adequado. Classificamos as respostas em formatos de resposta única ou múltipla, dependendo da natureza da informação desejada e da complexidade de cada pergunta.
  
### 13. **Modelagem do Data Warehouse - Pesquisa Geral**
A modelagem do Data Warehouse (DW) foi feita com o Power Architect e foi projetada para atender às necessidades de armazenamento, consulta e análise de dados relacionados a pesquisas e entrevistas, garantindo uma estrutura escalável e de fácil manutenção.

- `dim_entrevistado`: Armazena informações dos entrevistados.
- `dim_região`: Armazena informações sobre a região dos entrevistados.
- `dim_data`: Armazena detalhes sobre as datas para facilitar a análise temporal.
- `dim-pergunta`: Armazena informações das perguntas realizadas para os entrevistados.

  ![image](https://github.com/user-attachments/assets/84ac245d-2ed3-4281-a86f-b7150de72f3b)

### 14. **Tratamento do Data Warehouse com Pentaho**
No projeto de criação do sistema de perguntas e entrevista, o Pentaho foi utilizado como ferramenta de ETL (Extração, Transformação e Carga) para o tratamento e integração de dados em um Data Warehouse (DW) dedicado à análise das informações coletadas.

- `Tratamento Entrevistado`: 

 ![Tratamento_Entrevistado](https://github.com/user-attachments/assets/f5ef0907-eacc-4c3f-8d7f-b286eb62e387)


- `Tratamento Pergunta`:

 ![Tratamento_Pergunta](https://github.com/user-attachments/assets/67eb5966-5aad-4153-b522-ce579bb9db19)


- `Tratamento Pesquisa`:

 ![Tratamento_Pesquisa](https://github.com/user-attachments/assets/11003181-edec-4501-9998-e0e371ad29ba)


- `Tratamento Região`:

 ![Tratamento_Região](https://github.com/user-attachments/assets/688777b2-b2b2-40c7-ba1e-bba8311bc6fe)


## Tecnologias Utilizadas

- **PostgreSQL**: Sistema de banco de dados relacional usado para modelar e gerenciar as tabelas e relacionamentos.
- **SQL**: Linguagem utilizada para criação de tabelas, relacionamento de entidades, restrições e exclusão lógica.
- **Python**: Linguagem de programação utilizada para desenvolvimento de scripts e integração com o banco de dados.
-  **Power Architect**: Ferramenta de modelagem de banco de dados que permite realizar engenharia reversa de bancos de dados existentes para criar modelos visuais detalhados.
-  **Pentaho**: Ferramenta de ETL que permite coletar, transformar, monitorar e analisar dados, oferecendo recursos integrados para facilitar todo o processo de manipulação de informações.

## Considerações Finais

Este projeto foi desenvolvido com o objetivo de fornecer uma análise para a Ilha Primeira de fácil crescimento e manutenção de novas pesquisas e entrevistados ao longo do tempo. O banco de dados está preparado para armazenar grandes volumes de dados de forma organizada, garantindo a integridade e segurança das informações.
