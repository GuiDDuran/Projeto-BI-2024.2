SELECT 
e.entrevistado_id, sexo, genero.genero, entrevistado_data_nascimento
FROM entrevistado e
JOIN genero on e.genero_id = genero.genero_id