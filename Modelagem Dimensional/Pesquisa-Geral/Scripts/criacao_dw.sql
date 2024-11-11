
CREATE TABLE public.dim_pergunta (
                sk_pergunta INTEGER NOT NULL,
                nk_pergunta INTEGER NOT NULL,
                tp_pergunta VARCHAR(128) NOT NULL,
                is_ativo BOOLEAN NOT NULL,
                etl_dt_inicio TIMESTAMP NOT NULL,
                etl_dt_fim TIMESTAMP NOT NULL,
                etl_versao INTEGER NOT NULL,
                CONSTRAINT sk_pergunta PRIMARY KEY (sk_pergunta)
);


CREATE TABLE public.dim_regiao (
                sk_regiao INTEGER NOT NULL,
                sk_regiao_1 INTEGER NOT NULL,
                bairro VARCHAR(128) NOT NULL,
                cidade VARCHAR(128) NOT NULL,
                uf CHAR(2) NOT NULL,
                etl_dt_inicio TIMESTAMP NOT NULL,
                etl_dt_fim TIMESTAMP NOT NULL,
                etl_versao INTEGER NOT NULL,
                CONSTRAINT sk_regiao PRIMARY KEY (sk_regiao)
);


CREATE TABLE public.dim_entrevistado (
                sk_entrevistado INTEGER NOT NULL,
                nk_entrevistado INTEGER NOT NULL,
                sexo CHAR(1) NOT NULL,
                genero VARCHAR(128) NOT NULL,
                dt_nascimento DATE NOT NULL,
                etl_dt_inicio TIMESTAMP NOT NULL,
                etl_dt_fim TIMESTAMP NOT NULL,
                etl_versao INTEGER NOT NULL,
                CONSTRAINT sk_entrevistado PRIMARY KEY (sk_entrevistado)
);


CREATE TABLE public.ft_pesquisa (
                sk_regiao INTEGER NOT NULL,
                sk_entrevistado INTEGER NOT NULL,
                sk_pergunta INTEGER NOT NULL,
                dt_inicio TIMESTAMP NOT NULL,
                dt_fim TIMESTAMP NOT NULL,
                is_ativo BOOLEAN NOT NULL
);


ALTER TABLE public.ft_pesquisa ADD CONSTRAINT dim_pergunta_ft_pesquisa_fk
FOREIGN KEY (sk_pergunta)
REFERENCES public.dim_pergunta (sk_pergunta)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.ft_pesquisa ADD CONSTRAINT dim_regiao_ft_pesquisa_fk
FOREIGN KEY (sk_regiao)
REFERENCES public.dim_regiao (sk_regiao)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.ft_pesquisa ADD CONSTRAINT dim_entrevistado_ft_pesquisa_fk
FOREIGN KEY (sk_entrevistado)
REFERENCES public.dim_entrevistado (sk_entrevistado)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
