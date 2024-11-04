import psycopg2

# Conexão com o banco de dados transacional
def get_db_connection_transacional():
    return psycopg2.connect(
        host="localhost",
        database="projetoilhaprimeira",
        user="postgres",
        password="admin"
    )

# Conexão com o banco de dados de stage (espelho)
def get_db_connection_stage():
    return psycopg2.connect(
        host="localhost",
        database="stage_projetoilhaprimeira",
        user="postgres",
        password="admin"
    )

# Função para criar as tabelas na área de stage
def criar_tabelas_stage():
    conn_stage = get_db_connection_stage()
    cur_stage = conn_stage.cursor()

    # Criação das tabelas na área de stage
    comandos = [
        """
        CREATE TABLE IF NOT EXISTS pesquisa (
            pesquisa_id SERIAL PRIMARY KEY,
            pesquisa_nome VARCHAR(128) NOT NULL,
            data_inicio TIMESTAMP NOT NULL,
            data_fim TIMESTAMP NOT NULL,
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN NOT NULL DEFAULT TRUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pesquisa_pergunta_tipo (
            pesquisa_pergunta_tipo_id SERIAL PRIMARY KEY, 
            pesquisa_pergunta_tipo VARCHAR(32) NOT NULL,
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN NOT NULL DEFAULT TRUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pesquisa_pergunta (
            pesquisa_pergunta_id SERIAL PRIMARY KEY,
            pesquisa_id INT NOT NULL,
            pesquisa_pergunta_tipo_id INT NOT NULL,
            pergunta_texto VARCHAR(512) NOT NULL,
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            CONSTRAINT fk_pesquisa_x_pergunta_pesquisa FOREIGN KEY (pesquisa_id) REFERENCES pesquisa(pesquisa_id),
            CONSTRAINT fk_pesquisa_pergunta_x_pesquisa_pergunta_tipo FOREIGN KEY (pesquisa_pergunta_tipo_id) REFERENCES pesquisa_pergunta_tipo(pesquisa_pergunta_tipo_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS genero (
            genero_id SERIAL PRIMARY KEY,
            genero VARCHAR(128)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS entrevistado (
            entrevistado_id SERIAL PRIMARY KEY,
            entrevistado_nome VARCHAR(256) NOT NULL,
            entrevistado_email VARCHAR(128),
            entrevistado_nome_social VARCHAR(32),
            entrevistado_data_nascimento DATE NOT NULL,
            sexo CHAR(1) NOT NULL, 
            genero_id INT NOT NULL,
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_entrevistado_x_genero FOREIGN KEY (genero_id) REFERENCES genero(genero_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS telefone_tipo (
            telefone_tipo_id SERIAL PRIMARY KEY,
            telefone_tipo VARCHAR(32),
            ativo BOOLEAN NOT NULL DEFAULT TRUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS entrevistado_telefone (
            entrevistado_telefone_id SERIAL PRIMARY KEY,
            entrevistado_id INT,
            ddi INT NOT NULL DEFAULT 55,
            ddd INT NOT NULL,
            telefone INT NOT NULL,
            telefone_tipo_id INT NOT NULL,
            eh_telefone_principal BOOLEAN NOT NULL DEFAULT TRUE,
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,  
            CONSTRAINT fk_entrevistado_telefone_x_entrevistado FOREIGN KEY (entrevistado_id) REFERENCES entrevistado(entrevistado_id),
            CONSTRAINT fk_entrevistado_telefone_x_telefone_tipo FOREIGN KEY (telefone_tipo_id) REFERENCES telefone_tipo(telefone_tipo_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pergunta_resposta (
            pergunta_resposta_id SERIAL PRIMARY KEY,
            pesquisa_pergunta_id INT NOT NULL,
            entrevistado_id INT NOT NULL,
            resposta VARCHAR(2048),
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_pergunta_resposta_x_pesquisa_pergunta FOREIGN KEY (pesquisa_pergunta_id) REFERENCES pesquisa_pergunta(pesquisa_pergunta_id),
            CONSTRAINT fk_pergunta_resposta_x_entrevistado FOREIGN KEY (entrevistado_id) REFERENCES entrevistado(entrevistado_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pesquisa_pergunta_opcao (
            pesquisa_pergunta_opcao_id SERIAL PRIMARY KEY,
            pesquisa_pergunta_id INT,
            indice INT NOT NULL DEFAULT 1,
            opcao VARCHAR(128),
            data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,  
            CONSTRAINT fk_pesquisa_pergunta_opcao_x_pesquisa_pergunta FOREIGN KEY (pesquisa_pergunta_id) REFERENCES pesquisa_pergunta(pesquisa_pergunta_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS entrevistado_endereco ( 
            entrevistado_endereco_id SERIAL PRIMARY KEY,
            entrevistado_id INT NOT NULL,
            logradouro VARCHAR(256) NOT NULL,
            numero VARCHAR(64) NOT NULL,
            complemento VARCHAR(256),
            bairro VARCHAR(256) NOT NULL,
            cidade VARCHAR(256) NOT NULL,
            uf VARCHAR(2) NOT NULL,
            cep VARCHAR(8) NOT NULL,
            descricao VARCHAR(32),
            CONSTRAINT fk_entrevistado_endereco_x_entrevistado FOREIGN KEY (entrevistado_id) REFERENCES entrevistado(entrevistado_id)
        );
        """
    ]

    for comando in comandos:
        cur_stage.execute(comando)

    conn_stage.commit()
    cur_stage.close()
    conn_stage.close()

# Função para copiar os dados da transacional para a stage
def atualizar_stage():
    conn_transacional = get_db_connection_transacional()
    cur_transacional = conn_transacional.cursor()

    conn_stage = get_db_connection_stage()
    cur_stage = conn_stage.cursor()

    # Mapeamento de tabelas e suas chaves primárias
    tabelas_chaves_primarias = {
        'pesquisa': 'pesquisa_id',
        'pesquisa_pergunta_tipo': 'pesquisa_pergunta_tipo_id',
        'pesquisa_pergunta': 'pesquisa_pergunta_id',
        'genero': 'genero_id',
        'entrevistado': 'entrevistado_id',
        'telefone_tipo': 'telefone_tipo_id',
        'entrevistado_telefone': 'entrevistado_telefone_id',
        'pergunta_resposta': 'pergunta_resposta_id',
        'pesquisa_pergunta_opcao': 'pesquisa_pergunta_opcao_id',
        'entrevistado_endereco': 'entrevistado_endereco_id'
    }

    for tabela, chave_primaria in tabelas_chaves_primarias.items():
        # Selecionar dados da transacional
        cur_transacional.execute(f"SELECT * FROM {tabela}")
        dados = cur_transacional.fetchall()

        colunas = [desc[0] for desc in cur_transacional.description]
        colunas_str = ", ".join(colunas)

        # Preparar as instruções de UPSERT para atualizar ou inserir novos dados
        for linha in dados:
            valores = tuple(linha)
            placeholders = ', '.join(['%s'] * len(valores))
            
            update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in colunas])

            cur_stage.execute(f"""
                INSERT INTO {tabela} ({colunas_str}) 
                VALUES ({placeholders}) 
                ON CONFLICT ({chave_primaria}) 
                DO UPDATE SET {update_clause}
            """, valores)

    conn_stage.commit()

    cur_transacional.close()
    conn_transacional.close()
    cur_stage.close()
    conn_stage.close()

if __name__ == "__main__":
    atualizar_stage()   # Atualizar os dados da transacional para a área de stage