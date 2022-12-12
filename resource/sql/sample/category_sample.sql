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
                             INNER JOIN category_tree ct ON c.parent_id = ct.id)
SELECT ct.id        AS id,
       ct.name      AS name,
       ct.parent_id AS parent_id,
       c.name       AS parent_name,
       level
FROM category_tree ct
         LEFT JOIN category c ON ct.parent_id = c.id;

-- Sample 3
WITH RECURSIVE category_tree AS
                   (SELECT id, name, parent_id, 1::integer level
                    FROM category
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, ct.level + 1
                    FROM category c
                             JOIN category_tree ct ON c.parent_id = ct.id)
SELECT ct.id        AS id,
       ct.name      AS name,
       ct.parent_id AS parent_id,
       c.name       AS parent_name,
       c2.id        AS grandparent_id,
       c2.name      AS grandparent_name,
       level
FROM category_tree ct
         LEFT JOIN category c ON ct.parent_id = c.id
         LEFT JOIN category c2 ON c.parent_id = c2.id;

-- Sample 4
WITH RECURSIVE category_tree AS
                   (SELECT id, name, parent_id, 1::integer level
                    FROM category
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT c.id, c.name, c.parent_id, ct.level + 1
                    FROM category c
                             JOIN category_tree ct ON c.parent_id = ct.id)
SELECT c2.id   AS level_1_id,
       c2.name AS level_1_name,
       c.id    AS level_2_id,
       c.name  AS level_2_name,
       ct.id   AS level_3_id,
       ct.name AS level_3_name
FROM category_tree ct
         INNER JOIN category c ON ct.parent_id = c.id
         INNER JOIN category c2 ON c.parent_id = c2.id
WHERE ct.level = 3;