-- Sample 1
WITH RECURSIVE category_tree AS
                   (SELECT id, name, parent_id, 1::integer level
                    FROM category
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, ct.level + 1
                    FROM category c
                             INNER JOIN category_tree ct ON c.parent_id = ct.id)
SELECT *
FROM category_tree;

-- Sample 2
WITH RECURSIVE category_tree AS
                   (SELECT id, name, parent_id, 1::integer level
                    FROM category
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, ct.level + 1
                    FROM category c
                             JOIN category_tree ct ON c.parent_id = ct.id)
SELECT *
FROM category_tree ct
         INNER JOIN category c ON ct.parent_id = c.id
         INNER JOIN category c2 ON c.parent_id = c2.id
WHERE ct.level = 3;

-- Sample 3
WITH RECURSIVE category_tree AS
                   (SELECT id, name, parent_id, 1::integer level
                    FROM category
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, ct.level + 1
                    FROM category c
                             JOIN category_tree ct ON c.parent_id = ct.id)
SELECT ct.id AS category_3_id, c2.name AS category_1, c.name AS category_3, ct.name AS category_3
FROM category_tree ct
         INNER JOIN category c ON ct.parent_id = c.id
         INNER JOIN category c2 ON c.parent_id = c2.id
WHERE ct.level = 3;