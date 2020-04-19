-----------------------------------------
-- Update Transactions

-- Create a new case.
insert into cases values (default, 'Product damage', 'There are scratches on the surface of the product', 'Active', '04/17/2020 12:00:00', null, 2, 3, null);

-- Update cases. Example: Close a specific case, as the resolution of the case is found.
update cases
SET c_status = closed, c_timeend = "04/17/2020 23:55:00", resolution_id = 1
WHERE case_id=2;

-- Add a new order record.
insert into orders values (5, 5, "05/05/2019");

-- Add a new customer.
insert into customers values ("Brook", "Dorsey", "2006 Maple Ave, Evanston IL, 60201", "Samsung", 80000.00);

-- Update customers. Example: One customer's address and company information has changed.
update customers
set c_address = "124 Lexington St. Middletown, CT 06457", c_company = "Tesla"
where customer_id=2;

-- Add a new resolution.
insert into resolutions values ("Refund", "1) Check reciept 2) Troubleshoot issue 3) Check order date 4) Refund");

-----------------------------------------

-- Error checking
-- Bad support request check
alter table cases c add constraint customer_product_check check (
	c.product_id in(
		select o.product_id
		from orders o
		where c.customer_id = o.customer_id
	)
);

-- something more

-----------------------------------------

-- Data aggregation
-- Support cases by product (ordered by largest)
select c.*
from cases c,(select product_id,count(*) as num 
			  from cases 
			  group by product_id) a 
where c.product_id=a.product_id 
order by a.num desc;

-- Support cases closed by employee (ordered by largest)
select c.*
from cases c,(select employee_id,count(*) as num 
			  from cases 
			  group by employee_id) a 
where c.employee_id=a.employee_id 
order by a.num desc;

-- Support cases by customer (ordered by largest)
select c.*
from cases c,(select customer_id,count(*) as num 
			  from cases 
			  group by customer_id) a 
where c.customer_id=a.customer_id 
order by a.num desc;

-- Support cases by customer’s company (ordered by largest)
select c.*
from cases c,(select cu.customer_id,cu.c_company 
			  from customers cu, (select c_company,count(*) as num 
								 from customers 
								 group by c_company) b
			  where cu.c_company = b.c_company
			  order by b.num desc) a 
where c.customer_id=a.customer_id 
order by b.num desc;

-- something more

-----------------------------------------
