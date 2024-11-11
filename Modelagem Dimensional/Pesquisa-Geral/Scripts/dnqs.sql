insert into dim_entrevistado 
(sk_entrevistado, nk_entrevistado, sexo, genero, dt_nascimento, etl_dt_inicio, etl_dt_fim, etl_versao) 
values
(0, 0, '', 'N/A', '1900-01-01', '1900-01-01', '2199-12-31',0);

insert into dim_pergunta 
(sk_pergunta, nk_pergunta, tp_pergunta, is_ativo, etl_dt_inicio, etl_dt_fim, etl_versao) 
values
(0, 0, 'N/A', false, '1900-01-01', '2199-12-31',0);

insert into dim_regiao 
(sk_regiao , nk_regiao, bairro, cidade, uf, etl_dt_inicio, etl_dt_fim, etl_versao) 
values
(0, 0, 'N/A', 'N/A', 'NA', '1900-01-01', '2199-12-31',0);