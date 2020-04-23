-- Table Indexes

-- Products table
-- Too small

-- Customers table
-- First and Last Name 
-- Common search criteria (WHERE clause)

CREATE INDEX cfirst_last
ON Customers(c_first, c_last);


-- Orders table
-- Order Date
-- Common search criteria

CREATE INDEX odate
ON Orders(o_date);


-- Employees table
-- Occasional writes
-- First and Last Name
-- Common search criteria
-- Rare duplicate values

CREATE INDEX efirst_last
ON Employees(e_first, e_last);

-- Employee email
-- Common search criteria
-- Values should be unique

CREATE INDEX eemail
ON Employees(e_email);


-- Salespersons table
-- Subset of Employees table
-- Too many repeating values


-- Resolutions table
-- Too small


-- Cases table
-- Time Start
-- Common search criteria
-- Rare duplicate values
-- No null values (Time End)

CREATE INDEX ctimestart
ON Cases(c_timestart);


-- Comments table
-- Too many repeating values
-- Uncommon search criteria 