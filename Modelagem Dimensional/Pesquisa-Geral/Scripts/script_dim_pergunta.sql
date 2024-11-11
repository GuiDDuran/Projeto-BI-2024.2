SELECT 
pp.pesquisa_pergunta_id, ppt.pesquisa_pergunta_tipo, pp.ativo
FROM pesquisa_pergunta pp
JOIN pesquisa_pergunta_tipo ppt on ppt.pesquisa_pergunta_tipo_id = pp.pesquisa_pergunta_tipo_id