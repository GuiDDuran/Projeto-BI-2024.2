@app.route('/cadastrar_entrevista', methods=['GET'])
def cadastrar_entrevista():
    pesquisa_id = request.args.get('pesquisa_id')
    entrevistado_id = request.args.get('entrevistado_id')
    print(f"pesquisa_id: {pesquisa_id}, entrevistado_id: {entrevistado_id}")



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
    return render_template('cadastrar_entrevista.html', pesquisa_nome=pesquisa_nome, entrevistado_nome=entrevistado_nome)