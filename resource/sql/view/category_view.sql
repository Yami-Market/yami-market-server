-- Active: 1669593277665@@127.0.0.1@5432@yami-market@public
-- Category Recursive View
CREATE OR REPLACE VIEW category_recursive_view
AS
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


CREATE OR REPLACE VIEW category_flatten_view
AS
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


CREATE OR REPLACE VIEW category_path_view
AS
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
