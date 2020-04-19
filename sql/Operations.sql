-- Employee Browsing

-- Search for Cases by different attributes

-- Find cases within a time range. Example: Throughout April
select *
from Cases
where c_timestart between '03/31/2020 00:00:00' and '04/30/2020 23:59:59';

-- Find cases + details by status. Example: That are still Open
select c_summary, c_description, c_timestart, c_text
from Cases ca, Comments co
where ca.case_id = co.case_id
and c_status = 'Open';

-- Find cases and employee info by timeframe. Example: Taking an hour or more
select case_id, c_description, e_first, e_last, 
		date_part('day', c_timeend - c_timestart) * 24 + 
       	date_part('hour', c_timeend - c_timestart) hours
from Cases c,  employees e 
where e.employee_id = c.employee_id 
and date_part('day', c_timeend - c_timestart) * 24 + 
		date_part('hour', c_timeend - c_timestart) > 0


-- Search for Customers and purchase history

-- Find all customers and sort. Example: by income
select *
from Customers
order by c_income desc;

-- Find all customer orders. Example: sort by product
select c_first, c_last, p_name product, o_date ordered
from Customers c, Products p, Orders o
where c.customer_id = o.customer_id
and o.product_id = p.product_id
order by p_name;

-- Find specific customer and their orders. Example: Customer 1
select c_first, c_last, p_name product, o_date ordered
from Customers c, Products p, Orders o
where c.customer_id = o.customer_id
and o.product_id = p.product_id
and c.customer_id = 1
order by o_date;


-- Search for Resolutions related to Products

-- Find most common resolutions by product
select p_name product, r_name resolution, count( r_name ) total from
( select distinct p_name, r_name  
 	from Products p, Cases c, Resolutions r 
		where p.product_id = c.product_id
        and c.resolution_id = r.resolution_id ) as product_resolutions
group by product_resolutions.p_name, product_resolutions.r_name
order by total;
