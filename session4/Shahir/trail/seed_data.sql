-- Add 50 related seed rows to every ecommerce table.
-- Run after output_file.sql, for example:
--   psql -U admin -h localhost -d postgres -f seed_data.sql

BEGIN;

CREATE TEMP TABLE seed_groups ON COMMIT DROP AS
SELECT COALESCE(MAX(customer_group_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.customer_group
CROSS JOIN generate_series(1, 50);

INSERT INTO public.customer_group (customer_group_id, name, status)
SELECT id, 'Customer Group ' || n,
       CASE WHEN n % 10 = 0 THEN 'inactive' ELSE 'active' END
FROM seed_groups;

CREATE TEMP TABLE seed_customers ON COMMIT DROP AS
SELECT COALESCE(MAX(customer_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.customers
CROSS JOIN generate_series(1, 50);

INSERT INTO public.customers
    (customer_id, name, email, phone, password, gender, age,
     customer_group_id, status, created_at, updated_at)
SELECT c.id,
    'Customer ' || c.n,
    'customer.' || c.n || '@example.test',
       '90000' || lpad(c.n::text, 5, '0'),
    'seed_password_' || c.n,
       CASE WHEN c.n % 2 = 0 THEN 'Female' ELSE 'Male' END,
       21 + (c.n % 45),
       g.id,
       CASE WHEN c.n % 10 = 0 THEN 'inactive' ELSE 'active' END,
       CURRENT_TIMESTAMP - (c.n || ' days')::interval,
       CURRENT_TIMESTAMP - (c.n || ' days')::interval
FROM seed_customers c
JOIN seed_groups g ON g.n = ((c.n - 1) % 50) + 1;

CREATE TEMP TABLE seed_addresses ON COMMIT DROP AS
SELECT COALESCE(MAX(customer_address_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.customer_address
CROSS JOIN generate_series(1, 50);

INSERT INTO public.customer_address
    (customer_address_id, customer_id, address_type, address_line1,
     address_line2, city, state, postal_code, country, is_default)
SELECT a.id, c.id,
       CASE WHEN a.n % 2 = 0 THEN 'shipping' ELSE 'billing' END,
    (10 + a.n)::text || ' MG Road',
       'Suite ' || (100 + a.n),
       (ARRAY['Bengaluru', 'Chennai', 'Hyderabad', 'Mumbai', 'Pune'])[1 + ((a.n - 1) % 5)],
       (ARRAY['Karnataka', 'Tamil Nadu', 'Telangana', 'Maharashtra', 'Maharashtra'])[1 + ((a.n - 1) % 5)],
       (ARRAY['560001', '600001', '500001', '400001', '411001'])[1 + ((a.n - 1) % 5)],
       'India',
       true
FROM seed_addresses a
JOIN seed_customers c ON c.n = a.n;

CREATE TEMP TABLE seed_stores ON COMMIT DROP AS
SELECT COALESCE(MAX(store_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.stores
CROSS JOIN generate_series(1, 50);

INSERT INTO public.stores
    (store_id, name, description, location, email, phone, status,
     created_at, updated_at)
SELECT id,
    'Store Branch ' || n,
    'Seed store branch ' || n,
       'Market District ' || n,
    'store.' || n || '@example.test',
       '91000' || lpad(n::text, 5, '0'),
       CASE WHEN n % 10 = 0 THEN 'inactive' ELSE 'active' END,
       CURRENT_TIMESTAMP - (n || ' days')::interval,
       CURRENT_TIMESTAMP - (n || ' days')::interval
FROM seed_stores;

CREATE TEMP TABLE seed_products ON COMMIT DROP AS
SELECT COALESCE(MAX(prod_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.products
CROSS JOIN generate_series(1, 50);

INSERT INTO public.products
    (prod_id, name, short_desc, description, specifications,
     additional_data, image_title, image_url, status, created_at, updated_at)
SELECT id,
    'Product ' || n,
    'Product for testing',
    'Ecommerce product number ' || n,
       jsonb_build_object('model', 'SYN-' || lpad(n::text, 3, '0'), 'warranty_months', 12),
    jsonb_build_object('brand', 'OpenCart Labs', 'color', CASE WHEN n % 2 = 0 THEN 'Black' ELSE 'Silver' END),
    'Product ' || n,
    'https://example.test/products/product-' || n || '.jpg',
       CASE WHEN n % 10 = 0 THEN 'inactive' ELSE 'active' END,
       CURRENT_TIMESTAMP - (n || ' days')::interval,
       CURRENT_TIMESTAMP - (n || ' days')::interval
FROM seed_products;

CREATE TEMP TABLE seed_prices ON COMMIT DROP AS
SELECT COALESCE(MAX(prod_price_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.product_price
CROSS JOIN generate_series(1, 50);

INSERT INTO public.product_price (prod_price_id, prod_id, price, store_id)
SELECT p.id, prod.id, (1000 + (p.n * 125))::numeric(12, 2), store.id
FROM seed_prices p
JOIN seed_products prod ON prod.n = p.n
JOIN seed_stores store ON store.n = ((p.n - 1) % 50) + 1;

CREATE TEMP TABLE seed_inventory ON COMMIT DROP AS
SELECT COALESCE(MAX(prod_inv_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.product_inventory
CROSS JOIN generate_series(1, 50);

INSERT INTO public.product_inventory (prod_inv_id, prod_id, quantity, store_id)
SELECT i.id, prod.id, 25 + (i.n * 3), store.id
FROM seed_inventory i
JOIN seed_products prod ON prod.n = i.n
JOIN seed_stores store ON store.n = ((i.n - 1) % 50) + 1;

CREATE TEMP TABLE seed_orders ON COMMIT DROP AS
SELECT COALESCE(MAX(order_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.orders
CROSS JOIN generate_series(1, 50);

INSERT INTO public.orders
    (order_id, customer_id, store_id, base_price, sub_total, tax,
     grand_total, discount, payment_type, status, created_at, updated_at)
SELECT o.id, c.id, s.id,
       base.base_price,
       base.base_price - base.discount,
       round((base.base_price - base.discount) * 0.18, 2),
       round((base.base_price - base.discount) * 1.18, 2),
       base.discount,
       (ARRAY['card', 'upi', 'cash', 'netbanking'])[1 + ((o.n - 1) % 4)],
       (ARRAY['completed', 'pending', 'cancelled'])[1 + ((o.n - 1) % 3)],
       CURRENT_TIMESTAMP - (o.n || ' hours')::interval,
       CURRENT_TIMESTAMP - (o.n || ' hours')::interval
FROM seed_orders o
JOIN seed_customers c ON c.n = o.n
JOIN seed_stores s ON s.n = ((o.n - 1) % 50) + 1
CROSS JOIN LATERAL (
    SELECT (1000 + (o.n * 125))::numeric(12, 2) AS base_price,
           CASE WHEN o.n % 4 = 0 THEN 100 ELSE 0 END::numeric(12, 2) AS discount
) base;

CREATE TEMP TABLE seed_order_items ON COMMIT DROP AS
SELECT COALESCE(MAX(order_item_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.order_items
CROSS JOIN generate_series(1, 50);

INSERT INTO public.order_items
    (order_item_id, order_id, prod_id, quantity, unit_price, sub_total)
SELECT i.id, o.id, p.id, 1 + (i.n % 3),
       (1000 + (i.n * 125))::numeric(12, 2),
       ((1 + (i.n % 3)) * (1000 + (i.n * 125)))::numeric(12, 2)
FROM seed_order_items i
JOIN seed_orders o ON o.n = i.n
JOIN seed_products p ON p.n = i.n;

CREATE TEMP TABLE seed_billing ON COMMIT DROP AS
SELECT COALESCE(MAX(order_billing_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.order_billing
CROSS JOIN generate_series(1, 50);

INSERT INTO public.order_billing
    (order_billing_id, order_id, name, phone, address_line1, address_line2,
     city, state, postal_code, country)
SELECT b.id, o.id, 'Customer ' || b.n, '90000' || lpad(b.n::text, 5, '0'),
       (10 + b.n)::text || ' MG Road', 'Suite ' || (100 + b.n),
       'City ' || b.n, 'State ' || b.n, lpad((10000 + b.n)::text, 6, '0'), 'India'
FROM seed_billing b
JOIN seed_orders o ON o.n = b.n;

CREATE TEMP TABLE seed_shipping ON COMMIT DROP AS
SELECT COALESCE(MAX(order_shipping_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.order_shipping
CROSS JOIN generate_series(1, 50);

INSERT INTO public.order_shipping
    (order_shipping_id, order_id, name, phone, address_line1, address_line2,
     city, state, postal_code, country, shipping_method, shipping_cost,
     tracking_number, status)
SELECT s.id, o.id, 'Customer ' || s.n, '90000' || lpad(s.n::text, 5, '0'),
       (10 + s.n)::text || ' MG Road', 'Suite ' || (100 + s.n),
       'City ' || s.n, 'State ' || s.n, lpad((10000 + s.n)::text, 6, '0'), 'India',
       CASE WHEN s.n % 2 = 0 THEN 'Express' ELSE 'Standard' END,
       CASE WHEN s.n % 2 = 0 THEN 199.00 ELSE 99.00 END,
       'SYNTRACK' || lpad(s.n::text, 6, '0'),
       CASE WHEN s.n % 3 = 0 THEN 'delivered' ELSE 'shipped' END
FROM seed_shipping s
JOIN seed_orders o ON o.n = s.n;

CREATE TEMP TABLE seed_transactions ON COMMIT DROP AS
SELECT COALESCE(MAX(order_transaction_id), 0) + row_number() OVER () AS id,
       row_number() OVER () AS n
FROM public.order_transactions
CROSS JOIN generate_series(1, 50);

INSERT INTO public.order_transactions
    (order_transaction_id, order_id, transaction_id, amount, status, created_at)
SELECT t.id, o.id, 'SYN-TXN-' || lpad(t.n::text, 6, '0'),
       round((1000 + (t.n * 125)) * 1.18, 2),
       CASE WHEN t.n % 3 = 0 THEN 'pending' ELSE 'success' END,
       CURRENT_TIMESTAMP - (t.n || ' hours')::interval
FROM seed_transactions t
JOIN seed_orders o ON o.n = t.n;

INSERT INTO public.discounts
    (discount_id, name, description, prod_ids, discount_type, percentage,
     coupon_code, start_date, end_date, status, created_at, updated_at)
SELECT COALESCE((SELECT MAX(discount_id) FROM public.discounts), 0) + g,
    'Discount ' || g,
    'Discount for testing',
       jsonb_build_array((SELECT id FROM seed_products WHERE n = g)),
       'percentage',
       (5 + (g % 5))::numeric(5, 2),
       'SYNTH' || lpad(g::text, 3, '0'),
       CURRENT_TIMESTAMP - interval '7 days',
       CURRENT_TIMESTAMP + interval '30 days',
       CASE WHEN g % 10 = 0 THEN 'inactive' ELSE 'active' END,
       CURRENT_TIMESTAMP,
       CURRENT_TIMESTAMP
FROM generate_series(1, 50) AS g;

SELECT setval('public.customer_address_customer_address_id_seq', COALESCE(MAX(customer_address_id), 1), true) FROM public.customer_address;
SELECT setval('public.customer_group_customer_group_id_seq', COALESCE(MAX(customer_group_id), 1), true) FROM public.customer_group;
SELECT setval('public.customers_customer_id_seq', COALESCE(MAX(customer_id), 1), true) FROM public.customers;
SELECT setval('public.discounts_discount_id_seq', COALESCE(MAX(discount_id), 1), true) FROM public.discounts;
SELECT setval('public.order_billing_order_billing_id_seq', COALESCE(MAX(order_billing_id), 1), true) FROM public.order_billing;
SELECT setval('public.order_items_order_item_id_seq', COALESCE(MAX(order_item_id), 1), true) FROM public.order_items;
SELECT setval('public.order_shipping_order_shipping_id_seq', COALESCE(MAX(order_shipping_id), 1), true) FROM public.order_shipping;
SELECT setval('public.order_transactions_order_transaction_id_seq', COALESCE(MAX(order_transaction_id), 1), true) FROM public.order_transactions;
SELECT setval('public.orders_order_id_seq', COALESCE(MAX(order_id), 1), true) FROM public.orders;
SELECT setval('public.product_inventory_prod_inv_id_seq', COALESCE(MAX(prod_inv_id), 1), true) FROM public.product_inventory;
SELECT setval('public.product_price_prod_price_id_seq', COALESCE(MAX(prod_price_id), 1), true) FROM public.product_price;
SELECT setval('public.products_prod_id_seq', COALESCE(MAX(prod_id), 1), true) FROM public.products;
SELECT setval('public.stores_store_id_seq', COALESCE(MAX(store_id), 1), true) FROM public.stores;

COMMIT;
