-- category table
INSERT INTO category (id, name)
SELECT DISTINCT category_id, category_name
FROM stage;

-- second_category table

INSERT INTO second_category (id, name, category_id)
SELECT DISTINCT second_category_id, second_category_name, category_id
FROM stage;

-- third_category table

INSERT INTO third_category (id, name, second_category_id)
SELECT DISTINCT third_category_id, third_category_name, second_category_id
FROM stage;

-- product table

INSERT INTO product (id, name, unit_price, image_url, third_category_id)
SELECT DISTINCT product_id, product_name, unit_price, image_url, third_category_id
FROM stage;
