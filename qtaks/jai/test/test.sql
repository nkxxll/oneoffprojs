-- @todo Add proper indexing strategy
-- @bug SQL injection in dynamic queries
-- @incomplete Add input sanitization

-- @hack Using temporary tables for simplicity
CREATE TEMPORARY TABLE temp_cache AS SELECT 1;

-- @speed This query uses nested loops, add indexes
-- @warning No query optimization hints
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2023-01-01'
-- @robustness Add NULL handling
-- @incomplete Add transaction handling
GROUP BY u.id, u.name;

-- @feature Add full-text search support
-- @note Current implementation uses LIKE
CREATE INDEX idx_user_name ON users(name);

-- @cleanup Remove commented debug queries
-- SELECT * FROM users WHERE 1=0;

-- @bug Race condition in concurrent updates
-- @warning No row-level locking
UPDATE users SET updated_at = NOW()
-- @stability Test with large batch updates
WHERE id IN (SELECT id FROM users LIMIT 1000);

-- @incomplete Add error handling for stored procedures
-- @todo Implement audit logging
CREATE PROCEDURE sp_process_orders()
BEGIN
    -- @simplify Reduce procedure complexity
    START TRANSACTION;
    
    -- @stability Test rollback scenarios
    INSERT INTO order_log SELECT * FROM orders;
    
    COMMIT;
END;

-- @note Placeholder for analytics queries
-- @todo Optimize for reporting workload
