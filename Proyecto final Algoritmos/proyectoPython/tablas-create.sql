-- Table: public.clientes

-- DROP TABLE IF EXISTS public.clientes;

CREATE TABLE IF NOT EXISTS public.clientes
(
    id integer NOT NULL DEFAULT nextval('clientes_id_seq'::regclass),
    codigo character varying(30) COLLATE pg_catalog."default" NOT NULL,
    nombre character varying(100) COLLATE pg_catalog."default" NOT NULL,
    direccion character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT clientes_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.clientes
    OWNER to postgres;


-- Table: public.ventas

-- DROP TABLE IF EXISTS public.ventas;

CREATE TABLE IF NOT EXISTS public.ventas
(
    id integer NOT NULL DEFAULT nextval('ventas_id_seq'::regclass),
    codigo_producto character varying(30) COLLATE pg_catalog."default" NOT NULL,
    codigo_cliente character varying(30) COLLATE pg_catalog."default" NOT NULL,
    cantidad integer NOT NULL,
    total_venta numeric(10,2) NOT NULL,
    CONSTRAINT ventas_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ventas
    OWNER to postgres;    