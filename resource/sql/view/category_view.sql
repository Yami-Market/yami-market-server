-- Category Recursive View
CREATE RECURSIVE VIEW category_recursive_view (id, name, parent_id, recursive_level) AS
SELECT id, name, parent_id, 1::integer recursive_level
FROM category
WHERE parent_id IS NULL
UNION ALL
SELECT c.id, c.name, c.parent_id, ct.recursive_level + 1
FROM category c
         INNER JOIN category_recursive_view ct ON c.parent_id = ct.id