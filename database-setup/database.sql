
-- Products table DDL
CREATE TABLE Products (
	id VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255),
	description text,
	brand VARCHAR(255),
	price int,
	discount int,
	stock int,
	category VARCHAR(255),
	sub_category VARCHAR(255),
	sub_sub_category VARCHAR(255),
	sub_sub_sub_category VARCHAR(255),
	recommendable boolean,
	online_only boolean,
	target_demographic VARCHAR(255),
	gender VARCHAR(90),
	color VARCHAR(100),
	unit VARCHAR(255),
	odor_type VARCHAR(255),
	series VARCHAR(255),
	kind VARCHAR(255),
	variant VARCHAR(255),
	type VARCHAR(255),
	type_of_hair_care VARCHAR(255),
	type_of_hair_coloring VARCHAR(255)
);

-- Recommended table DDL
CREATE TABLE Recommended (
	id serial,
	product_id VARCHAR(255),
	profile_id VARCHAR(255)
);

-- Orders table DDL
CREATE TABLE orders (
	id serial,
	session_id VARCHAR(255),
	product_id VARCHAR(255)
);

-- Sessions table DDL
CREATE TABLE sessions (
	id VARCHAR(255) PRIMARY KEY,
	profile_id VARCHAR(255),
	session_start timestamp,
	session_end timestamp,
	browser_name VARCHAR(255),
	os_name VARCHAR(255),
	is_mobile_flag boolean,
	is_tablet_flag boolean,
	is_email_flag boolean,
	device_family VARCHAR(255)
);

-- Profiles table DDL
CREATE TABLE profiles (
	id VARCHAR(255) PRIMARY KEY,
	first_order timestamp,
	latest_order timestamp,
	order_amount int
);

-- Business rule #1
SELECT id FROM products
WHERE target_demographic='<demographic>'
ORDER BY RANDOM()
LIMIT 5;

-- Business rule #2
SELECT session_id FROM orders
WHERE product_id='<product_id>'
ORDER BY RANDOM()
LIMIT 5;
	-- For every session
	SELECT product_id FROM orders
	WHERE session_id = '<session_id>' AND product_id != '<product_id>'
	ORDER BY RANDOM()
	LIMIT 1;

-- Business rule #3
SELECT product_id FROM
	(SELECT product_id FROM
	 orders WHERE session_id IN
		(SELECT session_id FROM orders
		WHERE product_id = '38815')
	AND product_id != '38815')
AS id GROUP BY product_id
ORDER BY COUNT(*) DESC;

-- Business rule #4
SELECT product_id FROM
	(SELECT product_id FROM
	 orders WHERE session_id IN
		(SELECT session_id FROM orders
		WHERE product_id IN ('38815', '29438', '42914'))
	AND product_id NOT IN ('38815', '29438', '42914'))
AS id GROUP BY product_id
ORDER BY COUNT(*) DESC;

-- Business rule #5
SELECT id FROM(
    SELECT id,
    (gender + cat + subcat + subsubcat + brand) as Total FROM
    	(SELECT id,
    		sum(case when gender like 'Man%' then 1 else 0 end) AS gender,
    		sum(case when category = 'Gezond & verzorging' then 1 else 0 end) as cat,
    		sum(case when sub_category = 'Persoonlijke hygiene' then 1 else 0 end) as subcat,
    		sum(case when sub_sub_category = 'Inlegkruisjes' then 1 else 0 end) as subsubcat,
    		sum(case when brand = '8x4' then 1 else 0 end) as brand
    	FROM products
    	WHERE id != '44444'
    	GROUP by id)
    as id
    ORDER BY Total DESC)
as id;

