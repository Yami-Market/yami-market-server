SELECT product_id, name, quantity, list_price, image_url
FROM shopping_cart sc
         INNER JOIN product p ON p.id = sc.product_id
WHERE user_id = 'Nnxj92ztahI5';