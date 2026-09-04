--
-- PostgreSQL database dump
--

\restrict gMwuxasHde7Z8LcMDCcINZhXhrckfsQyeM9NhwW1bdrszdbQDkS8WClGbMyYkix

-- Dumped from database version 16.15 (Ubuntu 16.15-1.pgdg24.04+2)
-- Dumped by pg_dump version 16.15 (Ubuntu 16.15-1.pgdg24.04+2)

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
-- Name: customer_address; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.customer_address (
    customer_address_id bigint NOT NULL,
    customer_id bigint NOT NULL,
    address_type character varying(20) NOT NULL,
    address_line1 character varying(255) NOT NULL,
    address_line2 character varying(255),
    city character varying(100),
    state character varying(100),
    postal_code character varying(20),
    country character varying(100),
    is_default boolean DEFAULT false NOT NULL,
    CONSTRAINT customer_address_address_type_check CHECK (((address_type)::text = ANY ((ARRAY['billing'::character varying, 'shipping'::character varying])::text[])))
);


ALTER TABLE public.customer_address OWNER TO shahir;

--
-- Name: customer_address_customer_address_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.customer_address_customer_address_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customer_address_customer_address_id_seq OWNER TO shahir;

--
-- Name: customer_address_customer_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.customer_address_customer_address_id_seq OWNED BY public.customer_address.customer_address_id;


--
-- Name: customer_group; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.customer_group (
    customer_group_id bigint NOT NULL,
    name character varying(100) NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    CONSTRAINT customer_group_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.customer_group OWNER TO shahir;

--
-- Name: customer_group_customer_group_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.customer_group_customer_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customer_group_customer_group_id_seq OWNER TO shahir;

--
-- Name: customer_group_customer_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.customer_group_customer_group_id_seq OWNED BY public.customer_group.customer_group_id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.customers (
    customer_id bigint NOT NULL,
    name character varying(150) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(30),
    password text NOT NULL,
    gender character varying(20),
    age integer,
    customer_group_id bigint,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT customers_age_check CHECK ((age >= 0)),
    CONSTRAINT customers_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.customers OWNER TO shahir;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.customers_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_customer_id_seq OWNER TO shahir;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;


--
-- Name: discounts; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.discounts (
    discount_id bigint NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    prod_ids jsonb,
    discount_type character varying(30) NOT NULL,
    percentage numeric(5,2),
    coupon_code character varying(100),
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_discount_dates CHECK ((end_date >= start_date)),
    CONSTRAINT discounts_discount_type_check CHECK (((discount_type)::text = ANY ((ARRAY['percentage'::character varying, 'fixed'::character varying, 'coupon'::character varying])::text[]))),
    CONSTRAINT discounts_percentage_check CHECK (((percentage >= (0)::numeric) AND (percentage <= (100)::numeric))),
    CONSTRAINT discounts_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.discounts OWNER TO shahir;

--
-- Name: discounts_discount_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.discounts_discount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.discounts_discount_id_seq OWNER TO shahir;

--
-- Name: discounts_discount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.discounts_discount_id_seq OWNED BY public.discounts.discount_id;


--
-- Name: order_billing; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.order_billing (
    order_billing_id bigint NOT NULL,
    order_id bigint NOT NULL,
    name character varying(150),
    phone character varying(30),
    address_line1 character varying(255) NOT NULL,
    address_line2 character varying(255),
    city character varying(100),
    state character varying(100),
    postal_code character varying(20),
    country character varying(100)
);


ALTER TABLE public.order_billing OWNER TO shahir;

--
-- Name: order_billing_order_billing_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.order_billing_order_billing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_billing_order_billing_id_seq OWNER TO shahir;

--
-- Name: order_billing_order_billing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.order_billing_order_billing_id_seq OWNED BY public.order_billing.order_billing_id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.order_items (
    order_item_id bigint NOT NULL,
    order_id bigint NOT NULL,
    prod_id bigint NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    sub_total numeric(12,2) NOT NULL,
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0)),
    CONSTRAINT order_items_sub_total_check CHECK ((sub_total >= (0)::numeric)),
    CONSTRAINT order_items_unit_price_check CHECK ((unit_price >= (0)::numeric))
);


ALTER TABLE public.order_items OWNER TO shahir;

--
-- Name: order_items_order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.order_items_order_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_order_item_id_seq OWNER TO shahir;

--
-- Name: order_items_order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.order_items_order_item_id_seq OWNED BY public.order_items.order_item_id;


--
-- Name: order_shipping; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.order_shipping (
    order_shipping_id bigint NOT NULL,
    order_id bigint NOT NULL,
    name character varying(150),
    phone character varying(30),
    address_line1 character varying(255) NOT NULL,
    address_line2 character varying(255),
    city character varying(100),
    state character varying(100),
    postal_code character varying(20),
    country character varying(100),
    shipping_method character varying(100),
    shipping_cost numeric(12,2) DEFAULT 0 NOT NULL,
    tracking_number character varying(150),
    status character varying(30)
);


ALTER TABLE public.order_shipping OWNER TO shahir;

--
-- Name: order_shipping_order_shipping_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.order_shipping_order_shipping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_shipping_order_shipping_id_seq OWNER TO shahir;

--
-- Name: order_shipping_order_shipping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.order_shipping_order_shipping_id_seq OWNED BY public.order_shipping.order_shipping_id;


--
-- Name: order_transactions; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.order_transactions (
    order_transaction_id bigint NOT NULL,
    order_id bigint NOT NULL,
    transaction_id character varying(150) NOT NULL,
    amount numeric(12,2) NOT NULL,
    status character varying(30) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT order_transactions_amount_check CHECK ((amount >= (0)::numeric))
);


ALTER TABLE public.order_transactions OWNER TO shahir;

--
-- Name: order_transactions_order_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.order_transactions_order_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_transactions_order_transaction_id_seq OWNER TO shahir;

--
-- Name: order_transactions_order_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.order_transactions_order_transaction_id_seq OWNED BY public.order_transactions.order_transaction_id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.orders (
    order_id bigint NOT NULL,
    customer_id bigint NOT NULL,
    store_id bigint,
    base_price numeric(12,2) DEFAULT 0 NOT NULL,
    sub_total numeric(12,2) DEFAULT 0 NOT NULL,
    tax numeric(12,2) DEFAULT 0 NOT NULL,
    grand_total numeric(12,2) DEFAULT 0 NOT NULL,
    discount numeric(12,2) DEFAULT 0 NOT NULL,
    payment_type character varying(50),
    status character varying(30) DEFAULT 'pending'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_order_amounts CHECK (((base_price >= (0)::numeric) AND (sub_total >= (0)::numeric) AND (tax >= (0)::numeric) AND (grand_total >= (0)::numeric) AND (discount >= (0)::numeric)))
);


ALTER TABLE public.orders OWNER TO shahir;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_order_id_seq OWNER TO shahir;

--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- Name: product_inventory; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.product_inventory (
    prod_inv_id bigint NOT NULL,
    prod_id bigint NOT NULL,
    quantity integer DEFAULT 0 NOT NULL,
    store_id bigint NOT NULL,
    CONSTRAINT product_inventory_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.product_inventory OWNER TO shahir;

--
-- Name: product_inventory_prod_inv_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.product_inventory_prod_inv_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_inventory_prod_inv_id_seq OWNER TO shahir;

--
-- Name: product_inventory_prod_inv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.product_inventory_prod_inv_id_seq OWNED BY public.product_inventory.prod_inv_id;


--
-- Name: product_price; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.product_price (
    prod_price_id bigint NOT NULL,
    prod_id bigint NOT NULL,
    price numeric(12,2) NOT NULL,
    store_id bigint NOT NULL,
    CONSTRAINT product_price_price_check CHECK ((price >= (0)::numeric))
);


ALTER TABLE public.product_price OWNER TO shahir;

--
-- Name: product_price_prod_price_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.product_price_prod_price_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_price_prod_price_id_seq OWNER TO shahir;

--
-- Name: product_price_prod_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.product_price_prod_price_id_seq OWNED BY public.product_price.prod_price_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.products (
    prod_id bigint NOT NULL,
    name character varying(200) NOT NULL,
    short_desc text,
    description text,
    specifications jsonb,
    additional_data jsonb,
    image_title character varying(255),
    image_url text,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT products_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.products OWNER TO shahir;

--
-- Name: products_prod_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.products_prod_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_prod_id_seq OWNER TO shahir;

--
-- Name: products_prod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.products_prod_id_seq OWNED BY public.products.prod_id;


--
-- Name: stores; Type: TABLE; Schema: public; Owner: shahir
--

CREATE TABLE public.stores (
    store_id bigint NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    location character varying(255),
    email character varying(255),
    phone character varying(30),
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT stores_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.stores OWNER TO shahir;

--
-- Name: stores_store_id_seq; Type: SEQUENCE; Schema: public; Owner: shahir
--

CREATE SEQUENCE public.stores_store_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stores_store_id_seq OWNER TO shahir;

--
-- Name: stores_store_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shahir
--

ALTER SEQUENCE public.stores_store_id_seq OWNED BY public.stores.store_id;


--
-- Name: customer_address customer_address_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customer_address ALTER COLUMN customer_address_id SET DEFAULT nextval('public.customer_address_customer_address_id_seq'::regclass);


--
-- Name: customer_group customer_group_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customer_group ALTER COLUMN customer_group_id SET DEFAULT nextval('public.customer_group_customer_group_id_seq'::regclass);


--
-- Name: customers customer_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);


--
-- Name: discounts discount_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.discounts ALTER COLUMN discount_id SET DEFAULT nextval('public.discounts_discount_id_seq'::regclass);


--
-- Name: order_billing order_billing_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_billing ALTER COLUMN order_billing_id SET DEFAULT nextval('public.order_billing_order_billing_id_seq'::regclass);


--
-- Name: order_items order_item_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_items ALTER COLUMN order_item_id SET DEFAULT nextval('public.order_items_order_item_id_seq'::regclass);


--
-- Name: order_shipping order_shipping_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_shipping ALTER COLUMN order_shipping_id SET DEFAULT nextval('public.order_shipping_order_shipping_id_seq'::regclass);


--
-- Name: order_transactions order_transaction_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_transactions ALTER COLUMN order_transaction_id SET DEFAULT nextval('public.order_transactions_order_transaction_id_seq'::regclass);


--
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Name: product_inventory prod_inv_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_inventory ALTER COLUMN prod_inv_id SET DEFAULT nextval('public.product_inventory_prod_inv_id_seq'::regclass);


--
-- Name: product_price prod_price_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_price ALTER COLUMN prod_price_id SET DEFAULT nextval('public.product_price_prod_price_id_seq'::regclass);


--
-- Name: products prod_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.products ALTER COLUMN prod_id SET DEFAULT nextval('public.products_prod_id_seq'::regclass);


--
-- Name: stores store_id; Type: DEFAULT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.stores ALTER COLUMN store_id SET DEFAULT nextval('public.stores_store_id_seq'::regclass);


--
-- Data for Name: customer_address; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.customer_address (customer_address_id, customer_id, address_type, address_line1, address_line2, city, state, postal_code, country, is_default) FROM stdin;
\.


--
-- Data for Name: customer_group; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.customer_group (customer_group_id, name, status) FROM stdin;
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.customers (customer_id, name, email, phone, password, gender, age, customer_group_id, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: discounts; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.discounts (discount_id, name, description, prod_ids, discount_type, percentage, coupon_code, start_date, end_date, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: order_billing; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.order_billing (order_billing_id, order_id, name, phone, address_line1, address_line2, city, state, postal_code, country) FROM stdin;
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.order_items (order_item_id, order_id, prod_id, quantity, unit_price, sub_total) FROM stdin;
\.


--
-- Data for Name: order_shipping; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.order_shipping (order_shipping_id, order_id, name, phone, address_line1, address_line2, city, state, postal_code, country, shipping_method, shipping_cost, tracking_number, status) FROM stdin;
\.


--
-- Data for Name: order_transactions; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.order_transactions (order_transaction_id, order_id, transaction_id, amount, status, created_at) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.orders (order_id, customer_id, store_id, base_price, sub_total, tax, grand_total, discount, payment_type, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: product_inventory; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.product_inventory (prod_inv_id, prod_id, quantity, store_id) FROM stdin;
\.


--
-- Data for Name: product_price; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.product_price (prod_price_id, prod_id, price, store_id) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.products (prod_id, name, short_desc, description, specifications, additional_data, image_title, image_url, status, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: stores; Type: TABLE DATA; Schema: public; Owner: shahir
--

COPY public.stores (store_id, name, description, location, email, phone, status, created_at, updated_at) FROM stdin;
\.


--
-- Name: customer_address_customer_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.customer_address_customer_address_id_seq', 1, false);


--
-- Name: customer_group_customer_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.customer_group_customer_group_id_seq', 1, false);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.customers_customer_id_seq', 1, false);


--
-- Name: discounts_discount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.discounts_discount_id_seq', 1, false);


--
-- Name: order_billing_order_billing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.order_billing_order_billing_id_seq', 1, false);


--
-- Name: order_items_order_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.order_items_order_item_id_seq', 1, false);


--
-- Name: order_shipping_order_shipping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.order_shipping_order_shipping_id_seq', 1, false);


--
-- Name: order_transactions_order_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.order_transactions_order_transaction_id_seq', 1, false);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 1, false);


--
-- Name: product_inventory_prod_inv_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.product_inventory_prod_inv_id_seq', 1, false);


--
-- Name: product_price_prod_price_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.product_price_prod_price_id_seq', 1, false);


--
-- Name: products_prod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.products_prod_id_seq', 1, false);


--
-- Name: stores_store_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shahir
--

SELECT pg_catalog.setval('public.stores_store_id_seq', 1, false);


--
-- Name: customer_address customer_address_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customer_address
    ADD CONSTRAINT customer_address_pkey PRIMARY KEY (customer_address_id);


--
-- Name: customer_group customer_group_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customer_group
    ADD CONSTRAINT customer_group_pkey PRIMARY KEY (customer_group_id);


--
-- Name: customers customers_email_key; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_key UNIQUE (email);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: discounts discounts_coupon_code_key; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.discounts
    ADD CONSTRAINT discounts_coupon_code_key UNIQUE (coupon_code);


--
-- Name: discounts discounts_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.discounts
    ADD CONSTRAINT discounts_pkey PRIMARY KEY (discount_id);


--
-- Name: order_billing order_billing_order_id_key; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_billing
    ADD CONSTRAINT order_billing_order_id_key UNIQUE (order_id);


--
-- Name: order_billing order_billing_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_billing
    ADD CONSTRAINT order_billing_pkey PRIMARY KEY (order_billing_id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);


--
-- Name: order_shipping order_shipping_order_id_key; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_shipping
    ADD CONSTRAINT order_shipping_order_id_key UNIQUE (order_id);


--
-- Name: order_shipping order_shipping_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_shipping
    ADD CONSTRAINT order_shipping_pkey PRIMARY KEY (order_shipping_id);


--
-- Name: order_transactions order_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_transactions
    ADD CONSTRAINT order_transactions_pkey PRIMARY KEY (order_transaction_id);


--
-- Name: order_transactions order_transactions_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_transactions
    ADD CONSTRAINT order_transactions_transaction_id_key UNIQUE (transaction_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: product_inventory product_inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_inventory
    ADD CONSTRAINT product_inventory_pkey PRIMARY KEY (prod_inv_id);


--
-- Name: product_price product_price_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_price
    ADD CONSTRAINT product_price_pkey PRIMARY KEY (prod_price_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (prod_id);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (store_id);


--
-- Name: product_inventory uq_product_store_inventory; Type: CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_inventory
    ADD CONSTRAINT uq_product_store_inventory UNIQUE (prod_id, store_id);


--
-- Name: idx_customer_address_customer; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_customer_address_customer ON public.customer_address USING btree (customer_id);


--
-- Name: idx_customers_group; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_customers_group ON public.customers USING btree (customer_group_id);


--
-- Name: idx_inventory_product; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_inventory_product ON public.product_inventory USING btree (prod_id);


--
-- Name: idx_inventory_store; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_inventory_store ON public.product_inventory USING btree (store_id);


--
-- Name: idx_order_items_order; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_order_items_order ON public.order_items USING btree (order_id);


--
-- Name: idx_order_items_product; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_order_items_product ON public.order_items USING btree (prod_id);


--
-- Name: idx_orders_customer; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_orders_customer ON public.orders USING btree (customer_id);


--
-- Name: idx_orders_store; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_orders_store ON public.orders USING btree (store_id);


--
-- Name: idx_price_product; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_price_product ON public.product_price USING btree (prod_id);


--
-- Name: idx_price_store; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_price_store ON public.product_price USING btree (store_id);


--
-- Name: idx_transactions_order; Type: INDEX; Schema: public; Owner: shahir
--

CREATE INDEX idx_transactions_order ON public.order_transactions USING btree (order_id);


--
-- Name: order_billing fk_billing_order; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_billing
    ADD CONSTRAINT fk_billing_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: customer_address fk_customer_address_customer; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customer_address
    ADD CONSTRAINT fk_customer_address_customer FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id) ON DELETE CASCADE;


--
-- Name: customers fk_customer_group; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT fk_customer_group FOREIGN KEY (customer_group_id) REFERENCES public.customer_group(customer_group_id);


--
-- Name: product_inventory fk_inventory_product; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_inventory
    ADD CONSTRAINT fk_inventory_product FOREIGN KEY (prod_id) REFERENCES public.products(prod_id) ON DELETE CASCADE;


--
-- Name: product_inventory fk_inventory_store; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_inventory
    ADD CONSTRAINT fk_inventory_store FOREIGN KEY (store_id) REFERENCES public.stores(store_id) ON DELETE CASCADE;


--
-- Name: orders fk_order_customer; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- Name: order_items fk_order_item_order; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_item_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: order_items fk_order_item_product; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT fk_order_item_product FOREIGN KEY (prod_id) REFERENCES public.products(prod_id);


--
-- Name: orders fk_order_store; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_order_store FOREIGN KEY (store_id) REFERENCES public.stores(store_id);


--
-- Name: product_price fk_price_product; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_price
    ADD CONSTRAINT fk_price_product FOREIGN KEY (prod_id) REFERENCES public.products(prod_id) ON DELETE CASCADE;


--
-- Name: product_price fk_price_store; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.product_price
    ADD CONSTRAINT fk_price_store FOREIGN KEY (store_id) REFERENCES public.stores(store_id) ON DELETE CASCADE;


--
-- Name: order_shipping fk_shipping_order; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_shipping
    ADD CONSTRAINT fk_shipping_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: order_transactions fk_transaction_order; Type: FK CONSTRAINT; Schema: public; Owner: shahir
--

ALTER TABLE ONLY public.order_transactions
    ADD CONSTRAINT fk_transaction_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict gMwuxasHde7Z8LcMDCcINZhXhrckfsQyeM9NhwW1bdrszdbQDkS8WClGbMyYkix

