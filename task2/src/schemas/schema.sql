
CREATE TABLE customer_group (
    customer_group_id SERIAL PRIMARY KEY,
    name              VARCHAR(100) NOT NULL,
    status            VARCHAR(20) NOT NULL DEFAULT 'active'
                      CHECK (status IN ('active', 'inactive'))
);





CREATE TABLE customers (
    customer_id       BIGSERIAL PRIMARY KEY,
    name              VARCHAR(150) NOT NULL,
    email             VARCHAR(255) NOT NULL UNIQUE,
    phone             VARCHAR(30),
    password          TEXT NOT NULL,
    gender            VARCHAR(20),
    age               INTEGER CHECK (age >= 0),
    customer_group_id BIGINT,
    status            VARCHAR(20) NOT NULL DEFAULT 'active'
                      CHECK (status IN ('active', 'inactive')),
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,



    CONSTRAINT fk_customer_group
        FOREIGN KEY (customer_group_id)
        REFERENCES customer_group(customer_group_id)
);







CREATE TABLE customer_address (
    customer_address_id BIGSERIAL PRIMARY KEY,
    customer_id         BIGINT NOT NULL,
    address_type        VARCHAR(20) NOT NULL
                        CHECK (address_type IN ('billing', 'shipping')),
    address_line1       VARCHAR(255) NOT NULL,
    address_line2       VARCHAR(255),
    city                VARCHAR(100),
    state               VARCHAR(100),
    postal_code         VARCHAR(20),
    country             VARCHAR(100),
    is_default          BOOLEAN NOT NULL DEFAULT FALSE,



    CONSTRAINT fk_customer_address_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);







CREATE TABLE stores (
    store_id      BIGSERIAL PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    description   TEXT,
    location      VARCHAR(255),
    email         VARCHAR(255),
    phone         VARCHAR(30),
    status        VARCHAR(20) NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'inactive')),
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);







CREATE TABLE products (
    prod_id          BIGSERIAL PRIMARY KEY,
    name             VARCHAR(200) NOT NULL,
    short_desc       TEXT,
    description      TEXT,
    specifications   JSONB,
    additional_data  JSONB,
    image_title      VARCHAR(255),
    image_url        TEXT,
    status           VARCHAR(20) NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active', 'inactive')),
    created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);







CREATE TABLE product_inventory (
    prod_inv_id BIGSERIAL PRIMARY KEY,
    prod_id     BIGINT NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 0
                CHECK (quantity >= 0),
    store_id    BIGINT NOT NULL,



    CONSTRAINT fk_inventory_product
        FOREIGN KEY (prod_id)
        REFERENCES products(prod_id)
        ON DELETE CASCADE,



    CONSTRAINT fk_inventory_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
        ON DELETE CASCADE,



    CONSTRAINT uq_product_store_inventory
        UNIQUE (prod_id, store_id)
);







CREATE TABLE product_price (
    prod_price_id BIGSERIAL PRIMARY KEY,
    prod_id       BIGINT NOT NULL,
    price         NUMERIC(12,2) NOT NULL
                  CHECK (price >= 0),
    store_id      BIGINT NOT NULL,



    CONSTRAINT fk_price_product
        FOREIGN KEY (prod_id)
        REFERENCES products(prod_id)
        ON DELETE CASCADE,



    CONSTRAINT fk_price_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
        ON DELETE CASCADE
);







CREATE TABLE discounts (
    discount_id   BIGSERIAL PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    description   TEXT,



    prod_ids      JSONB,


    discount_type VARCHAR(30) NOT NULL
                  CHECK (
                      discount_type IN (
                          'percentage',
                          'fixed',
                          'coupon'
                      )
                  ),

    percentage    NUMERIC(5,2)
                  CHECK (percentage >= 0 AND percentage <= 100),



    coupon_code   VARCHAR(100) UNIQUE,



    start_date    TIMESTAMP NOT NULL,
    end_date      TIMESTAMP NOT NULL,



    status        VARCHAR(20) NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'inactive')),



    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,



    CONSTRAINT chk_discount_dates
        CHECK (end_date >= start_date)
);







CREATE TABLE orders (
    order_id       BIGSERIAL PRIMARY KEY,
    customer_id    BIGINT NOT NULL,
    store_id       BIGINT,
    base_price     NUMERIC(12,2) NOT NULL DEFAULT 0,
    sub_total      NUMERIC(12,2) NOT NULL DEFAULT 0,
    tax            NUMERIC(12,2) NOT NULL DEFAULT 0,
    grand_total    NUMERIC(12,2) NOT NULL DEFAULT 0,
    discount      NUMERIC(12,2) NOT NULL DEFAULT 0,
    payment_type   VARCHAR(50),
    status         VARCHAR(30) NOT NULL DEFAULT 'pending',
    created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,



    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),



    CONSTRAINT fk_order_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id),



    CONSTRAINT chk_order_amounts
        CHECK (
            base_price >= 0 AND
            sub_total >= 0 AND
            tax >= 0 AND
            grand_total >= 0 AND
            discount >= 0
        )
);







CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id      BIGINT NOT NULL,
    prod_id       BIGINT NOT NULL,
    quantity      INTEGER NOT NULL
                  CHECK (quantity > 0),
    unit_price    NUMERIC(12,2) NOT NULL
                  CHECK (unit_price >= 0),
    sub_total     NUMERIC(12,2) NOT NULL
                  CHECK (sub_total >= 0),



    CONSTRAINT fk_order_item_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,



    CONSTRAINT fk_order_item_product
        FOREIGN KEY (prod_id)
        REFERENCES products(prod_id)
);







CREATE TABLE order_shipping (
    order_shipping_id BIGSERIAL PRIMARY KEY,
    order_id          BIGINT NOT NULL UNIQUE,



    name              VARCHAR(150),
    phone             VARCHAR(30),
    address_line1     VARCHAR(255) NOT NULL,
    address_line2     VARCHAR(255),
    city              VARCHAR(100),
    state             VARCHAR(100),
    postal_code       VARCHAR(20),
    country           VARCHAR(100),



    shipping_method   VARCHAR(100),
    shipping_cost     NUMERIC(12,2) NOT NULL DEFAULT 0,
    tracking_number   VARCHAR(150),
    status            VARCHAR(30),



    CONSTRAINT fk_shipping_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE
);





CREATE TABLE order_billing (
    order_billing_id BIGSERIAL PRIMARY KEY,
    order_id         BIGINT NOT NULL UNIQUE,



    name             VARCHAR(150),
    phone            VARCHAR(30),
    address_line1    VARCHAR(255) NOT NULL,
    address_line2    VARCHAR(255),
    city             VARCHAR(100),
    state            VARCHAR(100),
    postal_code      VARCHAR(20),
    country          VARCHAR(100),



    CONSTRAINT fk_billing_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE
);







CREATE TABLE order_transactions (
    order_transaction_id BIGSERIAL PRIMARY KEY,
    order_id             BIGINT NOT NULL,
    transaction_id       VARCHAR(150) NOT NULL UNIQUE,
    amount               NUMERIC(12,2) NOT NULL
                         CHECK (amount >= 0),
    status               VARCHAR(30) NOT NULL,



    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,



    CONSTRAINT fk_transaction_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE
);
 