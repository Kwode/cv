--
-- PostgreSQL database dump
--

\restrict Xuaijg0SGXRWxXTuUuui4GLxpDdbeYaJBGpe2euo5hki9pZxliTOasJAe3N0Z7d

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company (
    cac character varying NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    location character varying NOT NULL,
    industry character varying,
    password character varying NOT NULL,
    description text
);


ALTER TABLE public.company OWNER TO postgres;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs (
    id character varying NOT NULL,
    company_id character varying NOT NULL,
    role character varying NOT NULL,
    required_skills character varying[] NOT NULL,
    preferred_skills character varying[],
    responsibilities character varying[] NOT NULL,
    experience_level character varying NOT NULL
);


ALTER TABLE public.jobs OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    id character varying NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    location character varying NOT NULL,
    institution character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company (cac, name, email, location, industry, password, description) FROM stdin;
RC-12345678	Acme Global	acme@gmail.com	Lagos	FinTech	$2b$12$YOX36.Jwu2FwixPXUyhuGOSbcG314mkynnNCDoDqEVKHu7n8dqmKG	Recruit
RC-12345679	Scols	scols@gmail.com	Abuja	EdTech	$2b$12$1STXezsn7HeOzxrLOLT9hOTBQ2myQR6m5MObFu9IfcqyJtHyqnECm	EdTech
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.jobs (id, company_id, role, required_skills, preferred_skills, responsibilities, experience_level) FROM stdin;
fae3d22b-6334-4374-ae8f-850c68340e1e	RC-12345678	Ai Engineer	{Python,"Machine Learning","Deep Learning",PyTorch,TensorFlow,Scikit-learn,NLP,"Data Structures and Algorithms",SQL,"REST APIs",FastAPI,Docker,Git,Linux,"Model Training and Evaluation","Feature Engineering","Data Preprocessing","Vector Databases",LLMs,"Prompt Engineering"}	{AWS,Kubernetes,MLOps,CI/CD,LangChain,"Hugging Face Transformers",Redis,Spark,Airflow,"Cloud Deployment","Monitoring ML Models"}	{}	Junior
a7359b8f-a80f-4e48-bc12-30559decc43e	RC-12345679	Machine Learning Engineer	{Python,"Machine Learning","Deep Learning",PyTorch,TensorFlow,Scikit-learn,"Data Structures and Algorithms",SQL,"Feature Engineering","Data Preprocessing","Model Training","Model Evaluation","REST APIs",FastAPI,Docker,Git,Linux}	{AWS,Kubernetes,MLOps,CI/CD,Airflow,Spark,Redis,"Vector Databases",LangChain,"Hugging Face Transformers","Monitoring ML Models","Model Deployment"}	{"Design and develop machine learning models for production systems",Train,evaluate,"and optimize deep learning and NLP models","Build scalable data pipelines for preprocessing and feature engineering","Deploy ML models using APIs and containerized environments","Collaborate with backend engineers and data scientists","Monitor model performance and retrain when necessary","Conduct experiments and document results"}	Junior
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (id, name, email, location, institution, password) FROM stdin;
211103051	John Doe	obruchekwode@gmail.com	Abuja	Nile	$2b$12$/tFqbtYkIAIYUqojX9mquO0NlgOjpVHp0Sst2g9ZpO94HgC0nl4Z2
\.


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (cac);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id);


--
-- Name: ix_company_cac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_company_cac ON public.company USING btree (cac);


--
-- Name: ix_company_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_company_email ON public.company USING btree (email);


--
-- Name: ix_company_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_company_name ON public.company USING btree (name);


--
-- Name: ix_jobs_company_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_jobs_company_id ON public.jobs USING btree (company_id);


--
-- Name: ix_student_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_student_email ON public.student USING btree (email);


--
-- Name: ix_student_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_student_id ON public.student USING btree (id);


--
-- Name: jobs jobs_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(cac);


--
-- PostgreSQL database dump complete
--

\unrestrict Xuaijg0SGXRWxXTuUuui4GLxpDdbeYaJBGpe2euo5hki9pZxliTOasJAe3N0Z7d

