-- Active: 1669593277665@@127.0.0.1@5432@yami-market@public
-- category table
INSERT INTO category (id, name, parent_id)
SELECT DISTINCT category_id, category_name, NULL
FROM stage;

-- second_category table

INSERT INTO category (id, name, parent_id)
SELECT DISTINCT second_category_id, second_category_name, category_id
FROM stage;

-- third_category table

INSERT INTO category (id, name, parent_id)
SELECT DISTINCT third_category_id, third_category_name, second_category_id
FROM stage;

-- product table

INSERT INTO product (id, name, list_price, image_url, category_id)
SELECT DISTINCT product_id, product_name, unit_price, image_url, third_category_id
FROM stage;
