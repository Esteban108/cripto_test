--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1 (Debian 12.1-1.pgdg100+1)
-- Dumped by pg_dump version 12rc1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: cripto_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE cripto_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE cripto_db OWNER TO postgres;

connect cripto_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: c_coins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.c_coins (
    description character varying(200) NOT NULL,
    id character varying(3) NOT NULL,
    created_at date NOT NULL,
    status integer NOT NULL
);


ALTER TABLE public.c_coins OWNER TO postgres;

--
-- Name: c_transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.c_transaction (
    send_value money NOT NULL,
    date timestamp with time zone NOT NULL,
    id integer NOT NULL,
    coin_id character varying(3) NOT NULL,
    user_sender_username character varying(2044),
    user_receiver_username character varying(2044),
    type_id integer NOT NULL
);


ALTER TABLE public.c_transaction OWNER TO postgres;

--
-- Name: c_transaction_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.c_transaction_type (
    id integer NOT NULL,
    description character varying(2044) NOT NULL
);


ALTER TABLE public.c_transaction_type OWNER TO postgres;

--
-- Name: c_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.c_user (
    username character varying(2044) NOT NULL,
    email character varying(2044) NOT NULL,
    password text NOT NULL,
    status integer NOT NULL,
    type_id integer NOT NULL
);


ALTER TABLE public.c_user OWNER TO postgres;

--
-- Name: c_user_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.c_user_type (
    id integer NOT NULL,
    description character varying(2044) NOT NULL
);


ALTER TABLE public.c_user_type OWNER TO postgres;

--
-- Name: seq_transaction; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_transaction
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_transaction OWNER TO postgres;

--
-- Name: seq_transaction_type; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_transaction_type
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_transaction_type OWNER TO postgres;

--
-- Name: seq_user_type; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_user_type
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_user_type OWNER TO postgres;

--
-- Data for Name: c_coins; Type: TABLE DATA; Schema: public; Owner: postgres
--

--INSERT INTO public.c_coins VALUES ('Dolares', 'USD', '2020-02-02', 1);


--
-- Data for Name: c_transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: c_transaction_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

--INSERT INTO public.c_transaction_type VALUES (1, 'DEBITO');
--INSERT INTO public.c_transaction_type VALUES (2, 'CARGA');
--INSERT INTO public.c_transaction_type VALUES (3, 'TRANSFERENCIA');


--
-- Data for Name: c_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

--INSERT INTO public.c_user VALUES ('string', 'user@example.com', '$2b$12$KXc8cTnL9HALxj/aKUNkvOTyF3eZE7s6QyOXb.cXmBaU.ZTXwj7Ua', 1, 1);


--
-- Data for Name: c_user_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

--INSERT INTO public.c_user_type VALUES (2, 'NORMAL');
--INSERT INTO public.c_user_type VALUES (1, 'ADMIN');


--
-- Name: seq_transaction; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seq_transaction', 22, true);


--
-- Name: seq_transaction_type; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seq_transaction_type', 1, false);


--
-- Name: seq_user_type; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seq_user_type', 1, false);


--
-- Name: c_user UK_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_user
    ADD CONSTRAINT "UK_email" UNIQUE (email);


--
-- Name: c_transaction UK_user_transaction; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction
    ADD CONSTRAINT "UK_user_transaction" UNIQUE (date, user_sender_username, user_receiver_username, type_id, coin_id);


--
-- Name: c_coins c_coins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_coins
    ADD CONSTRAINT c_coins_pkey PRIMARY KEY (id);


--
-- Name: c_transaction c_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction
    ADD CONSTRAINT c_transaction_pkey PRIMARY KEY (id);


--
-- Name: c_transaction_type c_transaction_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction_type
    ADD CONSTRAINT c_transaction_type_pkey PRIMARY KEY (id);


--
-- Name: c_user c_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_user
    ADD CONSTRAINT c_user_pkey PRIMARY KEY (username);


--
-- Name: c_user_type c_user_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_user_type
    ADD CONSTRAINT c_user_type_pkey PRIMARY KEY (id);


--
-- Name: index_coin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_coin ON public.c_transaction USING btree (coin_id);


--
-- Name: index_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_created_at ON public.c_coins USING btree (created_at);


--
-- Name: index_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_date ON public.c_transaction USING btree (date);


--
-- Name: index_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_status ON public.c_coins USING btree (status);


--
-- Name: index_status1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_status1 ON public.c_user USING btree (status);


--
-- Name: index_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_type ON public.c_transaction USING btree (type_id);


--
-- Name: index_user_receiver; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_user_receiver ON public.c_transaction USING btree (user_receiver_username);


--
-- Name: index_user_sender; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX index_user_sender ON public.c_transaction USING btree (user_sender_username);


--
-- Name: c_transaction lnk_c_coins_c_transaction; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction
    ADD CONSTRAINT lnk_c_coins_c_transaction FOREIGN KEY (coin_id) REFERENCES public.c_coins(id) MATCH FULL ON UPDATE CASCADE;


--
-- Name: c_transaction lnk_c_transaction_type_c_transaction; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction
    ADD CONSTRAINT lnk_c_transaction_type_c_transaction FOREIGN KEY (type_id) REFERENCES public.c_transaction_type(id) MATCH FULL ON UPDATE CASCADE;


--
-- Name: c_transaction lnk_c_user_c_transaction; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction
    ADD CONSTRAINT lnk_c_user_c_transaction FOREIGN KEY (user_sender_username) REFERENCES public.c_user(username) MATCH FULL ON UPDATE CASCADE;


--
-- Name: c_transaction lnk_c_user_c_transaction_2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_transaction
    ADD CONSTRAINT lnk_c_user_c_transaction_2 FOREIGN KEY (user_receiver_username) REFERENCES public.c_user(username) MATCH FULL ON UPDATE CASCADE;


--
-- Name: c_user lnk_c_user_type_c_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.c_user
    ADD CONSTRAINT lnk_c_user_type_c_user FOREIGN KEY (type_id) REFERENCES public.c_user_type(id) MATCH FULL ON UPDATE CASCADE;


--
-- PostgreSQL database dump complete
--

