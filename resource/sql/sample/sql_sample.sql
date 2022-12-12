SELECT *
FROM "order"
         INNER JOIN
     (SELECT t.order_id                           AS order_id,
             SUM(t.unit_price * t.order_quantity) AS subtotal_price,
             JSON_AGG(ROW_TO_JSON(t))             AS products
      FROM (SELECT "order".id AS order_id,
                   unit_price,
                   order_quantity,
                   p.*
            FROM "order"
                     INNER JOIN order_detail od ON "order".id = od.order_id
                     INNER JOIN product p ON p.id = od.product_id
            WHERE user_id = 'nQdP5R7WoBse'
              AND "order".id = 'xEqToge2Ag1q') AS t
      GROUP BY t.order_id) AS pt
     ON "order".id = pt.order_id;

SELECT id,
       order_date,
       ship_date,
       payment_date,
       shipping_fee,
       tax_rate,
       user_id,
       credit_card_id,
       shipping_address_id,
       subtotal_price,
       products,
       shipping_address,
       credit_card
FROM "order"
         INNER JOIN
     (SELECT t.order_id                           AS order_id,
             SUM(t.unit_price * t.order_quantity) AS subtotal_price,
             JSON_AGG(ROW_TO_JSON(t))             AS products
      FROM (SELECT "order".id AS order_id,
                   unit_price,
                   order_quantity,
                   p.*
            FROM "order"
                     INNER JOIN order_detail od ON "order".id = od.order_id
                     INNER JOIN product p ON p.id = od.product_id
            WHERE user_id = 'nQdP5R7WoBse'
              AND "order".id = 'xEqToge2Ag1q') AS t
      GROUP BY t.order_id) AS pt
     ON "order".id = pt.order_id
         INNER JOIN (SELECT id             AS address_id,
                            ROW_TO_JSON(t) AS shipping_address
                     FROM (SELECT *
                           FROM address
                           WHERE user_id = 'nQdP5R7WoBse') AS t) AS a
                    ON "order".shipping_address_id = a.address_id
         INNER JOIN (SELECT id             AS c_id,
                            ROW_TO_JSON(t) AS credit_card
                     FROM (SELECT *
                           FROM credit_card
                           WHERE user_id = 'nQdP5R7WoBse') AS t) AS c
                    ON "order".credit_card_id = c.c_id;



SELECT id AS address_id,
       ROW_TO_JSON(t)
FROM (SELECT *
      FROM address
      WHERE user_id = 'nQdP5R7WoBse') AS t
