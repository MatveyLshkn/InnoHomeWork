-- 1
SELECT SUM(amount) as total_sales
FROM orders
WHERE strftime('%Y-%m', order_date) = '2024-03';

-- 2
SELECT 
    customer,
    SUM(amount) as total_spent
FROM orders
GROUP BY customer
ORDER BY total_spent DESC
LIMIT 1;

-- 3
SELECT 
    ROUND(AVG(amount), 2) as average_order_value
FROM orders
WHERE order_date >= date('2024-03-30', '-3 months');