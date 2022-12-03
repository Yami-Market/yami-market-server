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
