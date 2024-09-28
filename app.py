from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import time

app = Flask(__name__)

# Função para conectar ao banco de dados PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname='dw_projetoilhaprimeira',
        user='postgres',
        password='admin',
        host='localhost',
        port='5432'
    )
    return conn

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página do administrador
@app.route('/administrador')
def administrador():
    return render_template('administrador.html')

# Rota para gerenciar entrevistados
@app.route('/gerenciar_entrevistado', methods=['GET', 'POST'])
def gerenciar_entrevistado():
    conn = get_db_connection()
    if request.method == 'POST':
        search_name = request.form['search_name']
        cur = conn.cursor()
        cur.execute("SELECT entrevistado_id, entrevistado_nome FROM entrevistado WHERE entrevistado_nome ILIKE %s", (f'%{search_name}%',))
        entrevistados = cur.fetchall()
        cur.close()
    else:
        cur = conn.cursor()
        cur.execute("SELECT entrevistado_id, entrevistado_nome FROM entrevistado;")
        entrevistados = cur.fetchall()
        cur.close()

    conn.close()
    return render_template('gerenciar_entrevistado.html', entrevistados=entrevistados)

# Rota para exibir informações de um entrevistado
@app.route('/informacao_entrevistado/<int:entrevistado_id>')
def informacao_entrevistado(entrevistado_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Seleciona as informações do entrevistado com base no ID
    cur.execute("""
        SELECT
            entrevistado_nome,
            entrevistado_email,
            sexo,
            entrevistado_data_nascimento,
            genero.genero
        FROM
            entrevistado
        JOIN
            genero ON entrevistado.genero_id = genero.genero_id
        WHERE
            entrevistado_id = %s
    """, (entrevistado_id,))

    entrevistado_info = cur.fetchone()

    cur.close()
    conn.close()

    # Verifica se o entrevistado foi encontrado
    if entrevistado_info is None:
        return "Entrevistado não encontrado.", 404

    return render_template(
        'informacao_entrevistado.html',
        entrevistado=entrevistado_info,
        entrevistado_id=entrevistado_id
    )

# Rota para exibir as respostas de um entrevistado
@app.route('/respostas_entrevistado/<int:entrevistado_id>')
def respostas_entrevistado(entrevistado_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Obter informações do entrevistado
    cur.execute("SELECT entrevistado_nome FROM entrevistado WHERE entrevistado_id = %s", (entrevistado_id,))
    entrevistado_info = cur.fetchone()

    # Obter informações da pesquisa e perguntas/respostas
    cur.execute("""
        SELECT
            pesquisa.pesquisa_nome,
            pesquisa_pergunta.pesquisa_pergunta_id,
            pesquisa_pergunta.pergunta_texto,
            pergunta_resposta.resposta
        FROM
            pesquisa
        JOIN
            pesquisa_pergunta ON pesquisa.pesquisa_id = pesquisa_pergunta.pesquisa_id
        JOIN
            pergunta_resposta ON pesquisa_pergunta.pesquisa_pergunta_id = pergunta_resposta.pesquisa_pergunta_id
        WHERE
            pergunta_resposta.entrevistado_id = %s
    """, (entrevistado_id,))

    perguntas_respostas = cur.fetchall()

    cur.close()
    conn.close()

    # Verifica se o entrevistado foi encontrado
    if entrevistado_info is None:
        return "Entrevistado não encontrado.", 404

    # Verifica se há perguntas e respostas
    if not perguntas_respostas:
        return "Nenhuma resposta encontrada para este entrevistado.", 404

    # Coleta o nome da pesquisa
    pesquisa_nome = perguntas_respostas[0][0] if perguntas_respostas else None

    return render_template(
        'respostas_entrevistado.html',
        entrevistado_nome=entrevistado_info[0],
        pesquisa_nome=pesquisa_nome,
        perguntas_respostas=perguntas_respostas
    )

# Rota para editar um entrevistado
@app.route('/editar_entrevistado/<int:entrevistado_id>', methods=['GET', 'POST'])
def editar_entrevistado(entrevistado_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.form['entrevistado_nome']
        email = request.form['entrevistado_email']
        nome_social = request.form['entrevistado_nome_social']
        data_nascimento = request.form['entrevistado_data_nascimento']
        sexo = request.form['sexo']

        # Atualiza o entrevistado no banco de dados
        cur.execute("""
            UPDATE entrevistado
            SET entrevistado_nome = %s,
                entrevistado_email = %s,
                entrevistado_nome_social = %s,
                entrevistado_data_nascimento = %s,
                sexo = %s
            WHERE entrevistado_id = %s
        """, (nome, email, nome_social, data_nascimento, sexo, entrevistado_id))

        conn.commit()  # Certifique-se de que as mudanças estão sendo salvas
        cur.close()
        conn.close()

        # Redireciona para a página de gerenciamento
        return redirect(url_for('gerenciar_entrevistado'))

    # Seleciona as informações do entrevistado
    cur.execute("SELECT * FROM entrevistado WHERE entrevistado_id = %s", (entrevistado_id,))
    entrevistado_info = cur.fetchone()

    cur.close()
    conn.close()

    if entrevistado_info is None:
        return "Entrevistado não encontrado.", 404

    return render_template('editar_entrevistado.html', entrevistado=entrevistado_info)

# Rota para listar as pesquisas
@app.route('/listar_pesquisa')
def listar_pesquisa():
    conn = get_db_connection()
    cur = conn.cursor()

    # Seleciona as pesquisas ativas
    cur.execute("SELECT pesquisa_id, pesquisa_nome FROM pesquisa WHERE ativo = TRUE")
    pesquisas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('listar_pesquisa.html', pesquisas=pesquisas)

# Rota para cadastrar um entrevistado
@app.route('/cadastrar_entrevistado', methods=['GET', 'POST'])
def cadastrar_entrevistado():
    if request.method == 'POST':
        pesquisa_id = request.form.get('pesquisa_id')
        print(f"pesquisa_id: {pesquisa_id}") #recebido com sucesso id=1


        conn = get_db_connection()
        cur = conn.cursor()

        # Buscar o nome da pesquisa
        cur.execute("SELECT pesquisa_nome FROM pesquisa WHERE pesquisa_id = %s", (pesquisa_id,))
        pesquisa_info = cur.fetchone()

        # Verificar se a pesquisa foi encontrada
        if pesquisa_info is None:
            return "Pesquisa não encontrada.", 404

        pesquisa_nome = pesquisa_info[0]

        # Buscar os gêneros disponíveis
        cur.execute("SELECT genero_id, genero FROM genero")
        generos = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('cadastrar_entrevistado.html', pesquisa_nome=pesquisa_nome, pesquisa_id=pesquisa_id, generos=generos)

    return redirect(url_for('listar_pesquisa'))

# Rota para salvar um entrevistado
@app.route('/salvar_entrevistado', methods=['POST'])
def salvar_entrevistado():
    nome = request.form.get('nome')
    nome_social = request.form.get('nome_social')
    email = request.form.get('email')
    sexo = request.form.get('sexo')
    genero_id = request.form.get('genero_id')
    data_nascimento = request.form.get('data_nascimento')
    pesquisa_id = request.form.get('pesquisa_id')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Inserir o entrevistado no banco de dados e retornar o entrevistado_id
        cur.execute("""
            INSERT INTO entrevistado (entrevistado_nome, entrevistado_nome_social, entrevistado_email, sexo, genero_id, entrevistado_data_nascimento)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING entrevistado_id
            """, (nome, nome_social, email, sexo, genero_id, data_nascimento))

        entrevistado_id = cur.fetchone()[0]  # Recuperar o entrevistado_id retornado

        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Em caso de erro, reverter a transação
        return f"Ocorreu um erro ao salvar o entrevistado: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

    # Redirecionar para a rota de cadastrar_endereco com pesquisa_id e entrevistado_id
    return redirect(url_for('cadastrar_endereco', pesquisa_id=pesquisa_id, entrevistado_id=entrevistado_id))

# Rota para cadastrar um endereço
@app.route('/cadastrar_endereco', methods=['GET'])
def cadastrar_endereco():
    pesquisa_id = request.args.get('pesquisa_id')
    print(f"pesquisa_id: {pesquisa_id} oi") # id com valor 1 recebido com sucesso
    entrevistado_id = request.args.get('entrevistado_id')

    conn = get_db_connection()
    cur = conn.cursor()

    # Buscar o nome da pesquisa
    cur.execute("SELECT pesquisa_nome FROM pesquisa WHERE pesquisa_id = %s", (pesquisa_id,))
    pesquisa_info = cur.fetchone()

    # Buscar o nome do entrevistado
    cur.execute("SELECT entrevistado_nome FROM entrevistado WHERE entrevistado_id = %s", (entrevistado_id,))
    entrevistado_info = cur.fetchone()

    cur.close()
    conn.close()

    # Verificar se a pesquisa ou o entrevistado foram encontrados
    if pesquisa_info is None or entrevistado_info is None:
        return "Pesquisa ou entrevistado não encontrados.", 404

    pesquisa_nome = pesquisa_info[0]
    entrevistado_nome = entrevistado_info[0]

    # Passar as variáveis `pesquisa_nome` e `entrevistado_nome` para o template
    return render_template('cadastrar_endereco.html', pesquisa_nome=pesquisa_nome, entrevistado_nome=entrevistado_nome, pesquisa_id=pesquisa_id, entrevistado_id=entrevistado_id) #ERRO TAVA AQUI NÃO PASAVA PESQUISA_ID NO RENDER PARA O HTMLHTML RECEBIA NULL

# Rota para salvar um endereço
@app.route('/salvar_endereco', methods=['POST'])
def salvar_endereco():
    entrevistado_id = request.form.get('entrevistado_id')
    cep = request.form.get('cep')
    logradouro = request.form.get('logradouro')
    numero = request.form.get('numero')
    complemento = request.form.get('complemento')
    bairro = request.form.get('bairro')
    cidade = request.form.get('cidade')
    uf = request.form.get('uf')
    descricao = request.form.get('descricao')
    pesquisa_id = request.form.get('pesquisa_id')  # Certifique-se de obter o ID da pesquisa aqui
    print(f"Pesquisa ID: {pesquisa_id} tá vindo??") # O ID NÃO ESTÁ CHEGANDO AQUI!!

    conn = get_db_connection()
    cur = conn.cursor()

    # Inserir o endereço no banco de dados
    cur.execute("""INSERT INTO entrevistado_endereco (entrevistado_id, cep, logradouro, numero, complemento, bairro, cidade, uf, descricao)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                   (entrevistado_id, cep, logradouro, numero, complemento, bairro, cidade, uf, descricao))

    conn.commit()

    cur.close()
    conn.close()

    # Redirecionar para a nova rota cadastrar_entrevista

    return redirect(url_for('cadastrar_entrevista', pesquisa_id=pesquisa_id, entrevistado_id=entrevistado_id))

# Rota para cadastrar uma entrevista
@app.route('/cadastrar_entrevista', methods=['GET'])
def cadastrar_entrevista():
    pesquisa_id = request.args.get('pesquisa_id')
    entrevistado_id = request.args.get('entrevistado_id')
    indice_pergunta = int(request.args.get('indice_pergunta', 0))

    conn = get_db_connection()
    cur = conn.cursor()

    # Buscar o nome da pesquisa
    cur.execute("SELECT pesquisa_nome FROM pesquisa WHERE pesquisa_id = %s", (pesquisa_id,))
    pesquisa_info = cur.fetchone()

    # Buscar o nome do entrevistado
    cur.execute("SELECT entrevistado_nome FROM entrevistado WHERE entrevistado_id = %s", (entrevistado_id,))
    entrevistado_info = cur.fetchone()

    if pesquisa_info is None or entrevistado_info is None:
        return "Pesquisa ou entrevistado não encontrados.", 404

    pesquisa_nome = pesquisa_info[0]
    entrevistado_nome = entrevistado_info[0]

    # Buscar o número total de perguntas da pesquisa
    cur.execute("SELECT COUNT(*) FROM pesquisa_pergunta WHERE pesquisa_id = %s", (pesquisa_id,))
    total_perguntas = cur.fetchone()[0]

    # Buscar a pergunta atual com base no índice, incluindo o tipo da pergunta
    cur.execute("""
        SELECT pp.pesquisa_pergunta_id, pp.pergunta_texto, ppt.pesquisa_pergunta_tipo_id
        FROM pesquisa_pergunta pp
        JOIN pesquisa_pergunta_tipo ppt ON pp.pesquisa_pergunta_tipo_id = ppt.pesquisa_pergunta_tipo_id
        WHERE pp.pesquisa_id = %s
        ORDER BY pp.pesquisa_pergunta_id
        LIMIT 1 OFFSET %s
    """, (pesquisa_id, indice_pergunta))
    pergunta_info = cur.fetchone()

    if pergunta_info is None:
        return render_template('finalizar_entrevista.html'), 200

    pergunta_id, pergunta_texto, pesquisa_pergunta_tipo_id = pergunta_info

    # Buscar as opções de resposta, caso a pergunta tenha (para escolha única e múltipla escolha)
    cur.execute("SELECT pesquisa_pergunta_opcao_id, opcao FROM pesquisa_pergunta_opcao WHERE pesquisa_pergunta_id = %s", (pergunta_id,))
    opcoes_resposta = cur.fetchall()

    cur.close()
    conn.close()
    print(f"pergunta_id: {pergunta_id} veio??") # veio mas n passa como parametro
    return render_template('cadastrar_entrevista.html',
                           pesquisa_nome=pesquisa_nome,
                           entrevistado_nome=entrevistado_nome,
                           pergunta_texto=pergunta_texto,
                           pesquisa_pergunta_tipo_id=pesquisa_pergunta_tipo_id,
                           opcoes_resposta=opcoes_resposta,
                           indice_pergunta=indice_pergunta,
                           total_perguntas=total_perguntas,
                           pergunta_id=pergunta_id,
                           pesquisa_id=pesquisa_id,
                           entrevistado_id=entrevistado_id)

# Rota para salvar uma entrevista
@app.route('/salvar_respostas', methods=['POST'])
def salvar_respostas():
    pesquisa_id = request.form.get('pesquisa_id')
    entrevistado_id = request.form.get('entrevistado_id')
    pergunta_id = request.form.get('pergunta_id')
    print(f"pergunta_id: {pergunta_id} aqui") #não chega
    resposta = request.form.get('resposta')  # Para respostas únicas
    respostas_multipla = request.form.getlist('respostas')  # Para múltipla escolha
    indice_pergunta = request.form.get('indice_pergunta')

    conn = get_db_connection()
    cur = conn.cursor()

    # Se a resposta for nula ou múltipla escolha for vazia, insira uma resposta vazia
    if not resposta and not respostas_multipla:
        cur.execute("""
            INSERT INTO pergunta_resposta (entrevistado_id, pesquisa_pergunta_id, resposta)
            VALUES (%s, %s, '')
        """, (entrevistado_id, pergunta_id))

    # Salve a resposta no banco de dados
    if resposta:
        cur.execute("""
            INSERT INTO pergunta_resposta (entrevistado_id, pesquisa_pergunta_id, resposta)
            VALUES (%s, %s, %s)
        """, (entrevistado_id, pergunta_id, resposta))
    elif respostas_multipla:
        for resp in respostas_multipla:
            cur.execute("""
                INSERT INTO pergunta_resposta (entrevistado_id, pesquisa_pergunta_id, resposta)
                VALUES (%s, %s, %s)
            """, (entrevistado_id, pergunta_id, resp))

    conn.commit()
    cur.close()
    conn.close()

    # Redirecionar para a próxima pergunta
    return redirect(url_for('cadastrar_entrevista', pesquisa_id=pesquisa_id, entrevistado_id=entrevistado_id, indice_pergunta=int(indice_pergunta) + 1))

@app.route('/gerenciar_pesquisa', methods=['GET'])
def gerenciar_pesquisas():
    conn = get_db_connection()
    cur = conn.cursor()

    # Seleciona todas as pesquisas do banco
    cur.execute("SELECT pesquisa_id, pesquisa_nome FROM pesquisa")
    pesquisas = cur.fetchall()

    cur.close()
    conn.close()

    # Renderiza o template com as pesquisas
    return render_template('gerenciar_pesquisa.html', pesquisas=pesquisas)

# Rota para cadastrar uma nova pesquisa
@app.route('/cadastrar_pesquisa', methods=['GET', 'POST'])
def cadastrar_pesquisa():
    if request.method == 'POST':
        # Processa os dados enviados pelo formulário
        nome_pesquisa = request.form.get('nome_pesquisa')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        conn = get_db_connection()
        cur = conn.cursor()

        # Inserir a nova pesquisa no banco de dados
        cur.execute("""
            INSERT INTO pesquisa (pesquisa_nome, data_inicio, data_fim)
            VALUES (%s, %s, %s)
            RETURNING pesquisa_id
        """, (nome_pesquisa, data_inicio, data_fim))

        pesquisa_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        # Redirecionar para a página de listar perguntas
        return redirect(url_for('listar_perguntas', pesquisa_id=pesquisa_id))

    # Exibir o formulário de cadastro se for uma requisição GET
    return render_template('cadastrar_pesquisa.html')

# Rota para listar as perguntas de uma pesquisa
@app.route('/listar_perguntas/<int:pesquisa_id>', methods=['GET'])
def listar_perguntas(pesquisa_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Buscar perguntas associadas a essa pesquisa
    cur.execute("""
        SELECT pesquisa_pergunta_id, pergunta_texto 
        FROM pesquisa_pergunta 
        WHERE pesquisa_id = %s
    """, (pesquisa_id,))
    perguntas = cur.fetchall()

    # Buscar o nome da pesquisa
    cur.execute("""
        SELECT pesquisa_nome 
        FROM pesquisa 
        WHERE pesquisa_id = %s
    """, (pesquisa_id,))
    nome_pesquisa = cur.fetchone()

    cur.close()
    conn.close()

    # Renderizar o template com as perguntas e o pesquisa_id
    return render_template('listar_perguntas.html', perguntas=perguntas, pesquisa_id=pesquisa_id, nome_pesquisa=nome_pesquisa[0])

# Rota para cadastrar uma nova pergunta
@app.route('/cadastrar_pergunta', methods=['GET', 'POST'])
def cadastrar_pergunta():
    if request.method == 'POST':
        # Pegue os dados enviados pelo formulário
        pesquisa_id = request.form.get('pesquisa_id')  # ID da pesquisa
        print(f"pesquisa_id: {pesquisa_id} aqui") # Não está recebendo
        pergunta_texto = request.form.get('pergunta_texto')  # Texto da pergunta
        pesquisa_pergunta_tipo_id = request.form.get('pesquisa_pergunta_tipo')  # Tipo da pergunta
        opcoes_resposta = request.form.getlist('opcao_resposta[]')  # Lista de opções de resposta

        # Verificações para garantir que nenhum valor necessário está "None" ou vazio
        if not pesquisa_id or pesquisa_id == 'None':
            return "Erro: pesquisa_id não foi fornecido corretamente", 400  # Retorna erro
        if not pergunta_texto:
            return "Erro: pergunta_texto não foi fornecido", 400  # Retorna erro
        if not pesquisa_pergunta_tipo_id or pesquisa_pergunta_tipo_id == 'None':
            return "Erro: pesquisa_pergunta_tipo_id não foi fornecido", 400  # Retorna erro

        conn = get_db_connection()
        cur = conn.cursor()

        # Insere a pergunta na tabela `pesquisa_pergunta`
        cur.execute("""
            INSERT INTO pesquisa_pergunta (pergunta_texto, pesquisa_id, pesquisa_pergunta_tipo_id)
            VALUES (%s, %s, %s) RETURNING pesquisa_pergunta_id
        """, (pergunta_texto, int(pesquisa_id), int(pesquisa_pergunta_tipo_id)))
        
        pergunta_id = cur.fetchone()[0]  # Pega o ID da pergunta recém-criada

        # Se o tipo da pergunta for "escolha única" ou "múltipla escolha", insere as opções
        if pesquisa_pergunta_tipo_id in ['1', '2']:  # 1 para "Escolha única" e 2 para "Múltipla escolha"
            for opcao in opcoes_resposta:
                if opcao:  # Verifica se a opção não está vazia
                    cur.execute("""
                        INSERT INTO pesquisa_pergunta_opcao (pergunta_id, opcao_texto)
                        VALUES (%s, %s)
                    """, (pergunta_id, opcao))

        # Salva as alterações no banco de dados
        conn.commit()
        cur.close()
        conn.close()

        # Redireciona para a página de listar perguntas após salvar
        return redirect(url_for('listar_perguntas', pesquisa_id=pesquisa_id))

    # Se for um GET, exibe o formulário de cadastro de pergunta
    pesquisa_id = request.args.get('pesquisa_id')  # Obtém o ID da pesquisa
    pesquisa_nome = ...  # Pega o nome da pesquisa a partir do banco (você deve implementar isso)

    # Busca os tipos de pergunta disponíveis
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT pesquisa_pergunta_tipo_id, pesquisa_pergunta_tipo FROM pesquisa_pergunta_tipo")
    tipos_pergunta = cur.fetchall()

    cur.close()
    conn.close()

    # Renderiza o template para cadastrar pergunta
    return render_template('cadastrar_pergunta.html', pesquisa_nome=pesquisa_nome, pesquisa_id=pesquisa_id, tipos_pergunta=tipos_pergunta)

if __name__ == '__main__':
    app.run(debug=True)
