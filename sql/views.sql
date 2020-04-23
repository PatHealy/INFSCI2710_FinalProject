-- Database Views

-- Salesperson table joined with Employees table
-- Lists salespersons' title and name
-- Provides information without exposing underlying employee information

CREATE VIEW salesteam (Title, First, Last)
    AS SELECT s_title, e_first, e_last
    FROM Salespersons s, Employees e
    WHERE s.employee_id = e.employee_id;


-- Cases table joined with Employees table
-- Lists more complicated cases and assigned employee
-- Provides information without exposing underlying employee information
-- More complicated query simplified to a View

CREATE VIEW longcases (ID, Description, First, Last)
    AS SELECT case_id, c_description, e_first, e_last, 
		date_part('day', c_timeend - c_timestart) * 24 + 
       	date_part('hour', c_timeend - c_timestart) hours
    FROM Cases c,  employees e 
    WHERE e.employee_id = c.employee_id 
    AND date_part('day', c_timeend - c_timestart) * 24 + 
		date_part('hour', c_timeend - c_timestart) > 0;


-- Products table joined with Customers and Orders tables
-- Lists all product orders and associated customers
-- Provides information without exposing underlying customer information

CREATE VIEW productorders (Product, First, Last, Date)
    AS SELECT p_name product, c_first, c_last, o_date ordered
    FROM Customers c, Products p, Orders o
    WHERE c.customer_id = o.customer_id
    AND o.product_id = p.product_id
    ORDER BY p_name;


-- Cases table joined with Products and Resolutions tables
-- Lists resolutions by product
-- More complicated query simplified to a View

CREATE VIEW productresolutions (Product, Resolution, Count)
    AS SELECT p_name product, r_name resolution, COUNT( r_name ) total FROM
    ( SELECT DISTINCT p_name, r_name  
 	    FROM Products p, Cases c, Resolutions r 
		    WHERE p.product_id = c.product_id
            AND c.resolution_id = r.resolution_id ) AS product_resolutions
    GROUP BY product_resolutions.p_name, product_resolutions.r_name
    ORDER BY total;