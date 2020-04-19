drop table Comments;
drop table Cases;
drop table Resolutions;
drop table Salespersons;
drop table Employees;
drop table Orders;
drop table Customers;
drop table Products;

create table Products (
    product_id serial,
    p_name varchar (50) not null,
    p_description text,
    primary key (product_id)
);

create table Customers (
    customer_id serial,
    c_first varchar (20) not null,
    c_last varchar (20) not null,
    c_address varchar (100) not null,
    c_company varchar (50) not null,
    c_income numeric(10,2) check (c_income > 0),
    primary key (customer_id)
);

create table Orders (
    customer_id int,
    product_id int,
    o_date date,
    primary key (customer_id, product_id),
    foreign key (customer_id) references Customers
        on delete cascade, 
    foreign key (product_id) references Products
        on delete cascade
);

create table Employees (
    employee_id serial,
    e_first varchar (20) not null,
    e_last varchar (20) not null,
    e_address varchar (100) not null,
    e_phone varchar (20) not null,
    e_email varchar (50) not null,
    primary key (employee_id)
);

create table Salespersons (
    salesperson_id serial,
    s_title varchar (50),
    employee_id int,
    primary key (salesperson_id),
    foreign key (employee_id) references Employees
        on delete cascade
);

create table Resolutions (
    resolution_id serial,
    r_name varchar (50) not null,
    r_steps text,
    primary key (resolution_id)
);

create table Cases (
    case_id serial,
    c_summary text,
    c_description text,
    c_status varchar (20) check (c_status in ('Open', 'Closed', 'Active')),
    c_timestart timestamp,
    c_timeend timestamp,
    employee_id int,
    product_id int,
    resolution_id int,
    primary key (case_id),
    foreign key (employee_id) references Employees
        on delete set null,
    foreign key (product_id) references Products
        on delete set null,
    foreign key (resolution_id) references Resolutions
        on delete set null
);

create table Comments (
    comment_id serial,
    c_text text not null,
    c_time timestamp,
    case_id int,
    primary key (comment_id),
    foreign key (case_id) references Cases
        on delete cascade
)