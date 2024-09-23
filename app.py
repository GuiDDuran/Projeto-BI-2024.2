from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="dw_projetoilhaprimeira",
        user="postgres",
        password="admin",
        options="-c client_encoding=UTF8"
    )
    return conn

# Rota para exibir a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para listar pesquisas
@app.route('/pesquisas')
def pesquisas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pesquisa;')
    pesquisas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('pesquisas.html', pesquisas=pesquisas)

# Rota para adicionar uma nova pesquisa
@app.route('/adicionar_pesquisa', methods=('GET', 'POST'))
def adicionar_pesquisa():
    if request.method == 'POST':
        nome = request.form['nome']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO pesquisa (pesquisa_nome, data_inicio, data_fim) VALUES (%s, %s, %s)',
                    (nome, data_inicio, data_fim))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('pesquisas'))
    
    return render_template('adicionar_pesquisa.html')

# Rota para editar uma pesquisa
@app.route('/editar_pesquisa/<int:id>', methods=('GET', 'POST'))
def editar_pesquisa(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pesquisa WHERE pesquisa_id = %s', (id,))
    pesquisa = cur.fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        
        cur.execute('UPDATE pesquisa SET pesquisa_nome = %s, data_inicio = %s, data_fim = %s WHERE pesquisa_id = %s',
                    (nome, data_inicio, data_fim, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('pesquisas'))

    cur.close()
    conn.close()
    return render_template('editar_pesquisa.html', pesquisa=pesquisa)

# Rota para excluir uma pesquisa
@app.route('/excluir_pesquisa/<int:id>', methods=('POST',))
def excluir_pesquisa(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM pesquisa WHERE pesquisa_id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('pesquisas'))

# Rota para listar perguntas de uma pesquisa
@app.route('/perguntas/<int:pesquisa_id>')
def perguntas(pesquisa_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pesquisa_pergunta WHERE pesquisa_id = %s', (pesquisa_id,))
    perguntas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('perguntas.html', perguntas=perguntas, pesquisa_id=pesquisa_id)

# Rota para adicionar uma nova pergunta
@app.route('/adicionar_pergunta/<int:pesquisa_id>', methods=('GET', 'POST'))
def adicionar_pergunta(pesquisa_id):
    if request.method == 'POST':
        pergunta_texto = request.form['pergunta_texto']
        tipo_id = request.form['tipo_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO pesquisa_pergunta (pesquisa_id, pesquisa_pergunta_tipo_id, pergunta_texto) VALUES (%s, %s, %s)',
                    (pesquisa_id, tipo_id, pergunta_texto))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('perguntas', pesquisa_id=pesquisa_id))
    
    return render_template('adicionar_pergunta.html', pesquisa_id=pesquisa_id)

# Rota para editar uma pergunta
@app.route('/editar_pergunta/<int:id>', methods=('GET', 'POST'))
def editar_pergunta(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pesquisa_pergunta WHERE pesquisa_pergunta_id = %s', (id,))
    pergunta = cur.fetchone()
    
    if request.method == 'POST':
        pergunta_texto = request.form['pergunta_texto']
        tipo_id = request.form['tipo_id']
        
        cur.execute('UPDATE pesquisa_pergunta SET pergunta_texto = %s, pesquisa_pergunta_tipo_id = %s WHERE pesquisa_pergunta_id = %s',
                    (pergunta_texto, tipo_id, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('perguntas', pesquisa_id=pergunta[1]))

    cur.close()
    conn.close()
    return render_template('editar_pergunta.html', pergunta=pergunta)

# Rota para excluir uma pergunta
@app.route('/excluir_pergunta/<int:id>', methods=('POST',))
def excluir_pergunta(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM pesquisa_pergunta WHERE pesquisa_pergunta_id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('pesquisas'))

# Rota para listar entrevistados
@app.route('/entrevistados')
def entrevistados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM entrevistado;')
    entrevistados = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('entrevistados.html', entrevistados=entrevistados)

# Rota para adicionar um novo entrevistado
@app.route('/adicionar_entrevistado', methods=('GET', 'POST'))
def adicionar_entrevistado():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        nome_social = request.form['nome_social']
        data_nascimento = request.form['data_nascimento']
        sexo = request.form['sexo']
        genero_id = request.form['genero_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO entrevistado (entrevistado_nome, entrevistado_email, entrevistado_nome_social, entrevistado_data_nascimento, sexo, genero_id) VALUES (%s, %s, %s, %s, %s, %s)',
                    (nome, email, nome_social, data_nascimento, sexo, genero_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('entrevistados'))
    
    return render_template('adicionar_entrevistado.html')

# Rota para editar um entrevistado
@app.route('/editar_entrevistado/<int:id>', methods=('GET', 'POST'))
def editar_entrevistado(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM entrevistado WHERE entrevistado_id = %s', (id,))
    entrevistado = cur.fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        nome_social = request.form['nome_social']
        data_nascimento = request.form['data_nascimento']
        sexo = request.form['sexo']
        genero_id = request.form['genero_id']
        
        cur.execute('UPDATE entrevistado SET entrevistado_nome = %s, entrevistado_email = %s, entrevistado_nome_social = %s, entrevistado_data_nascimento = %s, sexo = %s, genero_id = %s WHERE entrevistado_id = %s',
                    (nome, email, nome_social, data_nascimento, sexo, genero_id, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('entrevistados'))

    cur.close()
    conn.close()
    return render_template('editar_entrevistado.html', entrevistado=entrevistado)

# Rota para excluir um entrevistado
@app.route('/excluir_entrevistado/<int:id>', methods=('POST',))
def excluir_entrevistado(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM entrevistado WHERE entrevistado_id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('entrevistados'))

# Rota para listar respostas
@app.route('/respostas/<int:pesquisa_id>')
def respostas(pesquisa_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pergunta_resposta WHERE pesquisa_pergunta_id IN (SELECT pesquisa_pergunta_id FROM pesquisa_pergunta WHERE pesquisa_id = %s)', (pesquisa_id,))
    respostas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('respostas.html', respostas=respostas, pesquisa_id=pesquisa_id)

# Rota para adicionar uma nova resposta
@app.route('/adicionar_resposta/<int:pesquisa_pergunta_id>', methods=('GET', 'POST'))
def adicionar_resposta(pesquisa_pergunta_id):
    if request.method == 'POST':
        entrevistado_id = request.form['entrevistado_id']
        resposta = request.form['resposta']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO pergunta_resposta (pesquisa_pergunta_id, entrevistado_id, resposta) VALUES (%s, %s, %s)',
                    (pesquisa_pergunta_id, entrevistado_id, resposta))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('respostas', pesquisa_id=request.form['pesquisa_id']))
    
    return render_template('adicionar_resposta.html', pesquisa_pergunta_id=pesquisa_pergunta_id)

if __name__ == '__main__':
    app.run(debug=True)
