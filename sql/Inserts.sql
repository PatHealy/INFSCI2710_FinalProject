delete from Comments;
delete from Cases;
delete from Resolutions;
delete from Salespersons;
delete from Employees;
delete from Orders;
delete from Customers;
delete from Products;

insert into Products values (default, 'Flagship', 'Our most high-end, premium offering');
insert into Products values (default, 'Signature', 'The top recommended, most well-known product');
insert into Products values (default, 'Economy', 'An affordable option for conservative consumers');
insert into Products values (default, 'Custom', 'Designed specifically for your specifications');
insert into Products values (default, 'Enterprise', 'Scaled for higher performance and reliability');
insert into Products values (default, 'Student', 'Provides main features (eligibility required)');

insert into Customers values (default, 'Russell', 'Timco', '4200 Fifth Ave, Pittsburgh PA, 15260', 'University of Pittsburgh', 50000.00);
insert into Customers values (default, 'Sam', 'Bar', '4496 Canal St, New Orleans LA, 37880', 'Apple', 95000.00);
insert into Customers values (default, 'Theo', 'Rose', '1909 Delaware Ave, Buffalo NY, 12896', 'Amazon', 105000.00);
insert into Customers values (default, 'Dave', 'Copper', '2020 Las Vegas Boulevard, Las Vegas NV, 76908', 'Google', 88000.00);
insert into Customers values (default, 'Frank', 'Sina', '101 Fifth Ave, New York NY, 10001', 'Apple', 125000.00);
insert into Customers values (default, 'Cici', 'Young', '221 Vermont St, San Francisco CA, 32981', 'Microsoft', 76000.00);

insert into Orders values (1, 1, '01/01/2020');
insert into Orders values (2, 3, '02/14/2020');
insert into Orders values (4, 6, '12/08/2019');
insert into Orders values (5, 2, '03/15/2020');
insert into Orders values (6, 2, '04/04/2020');
insert into Orders values (3, 4, '11/01/2019');
insert into Orders values (1, 2, '03/15/2020');
insert into Orders values (6, 4, '04/04/2020');

insert into Employees values (default, 'Anthony', 'Harris', '123 Example St, Brooklyn NY, 12345', '718-555-5555', 'agh41@pitt.edu');
insert into Employees values (default, 'Yiduo', 'Wang', '456 Demo Ave, Pittsburgh PA, 15206', '412-777-7777', 'yiw141@pitt.edu');
insert into Employees values (default, 'Patrick', 'Healy', '789 Project Dr, Pittsburgh PA, 15232', '412-123-4567', 'pat.healy@pitt.edu');
insert into Employees values (default, 'Karumbaiah', 'Thimmaiah', '1010 Team Pl, New York NY, 10001', '212-987-6543', 'kmt86@pitt.edu');

insert into Salespersons values (default, 'Associate', 1);
insert into Salespersons values (default, 'Manager', 3);
insert into Salespersons values (default, 'Team Leader', 2);

insert into Resolutions values (default, 'Return', '1) Confirm reciept 2) Check date 3) Inquire reason 4) Deactivate product');
insert into Resolutions values (default, 'Price Dispute', '1) Check reciept 2) Confirm cost 3) Check order date 4) Refund difference');
insert into Resolutions values (default, 'Wrong Product', '1) Check reciept 2) Check oreder date 3) Replace product');
insert into Resolutions values (default, 'Malfunction', '1) Check reciept 2) Troubleshoot issue 3) Confirm functionality');

insert into Cases values (default, 'Customer incorrectly charged', 'Customer reported overcharge', 'Closed', '01/02/2020 11:15:55', '01/03/2020 10:10:30', 4, 5, 2);
insert into Cases values (default, 'Customer complaint', 'Customer unsatisfied with product feature', 'Open', '02/26/2020 08:25:45', null, 1, 3, null);
insert into Cases values (default, 'Customer wants to make a return', 'Customer decided on an alternative solution', 'Closed', '03/01/2020 12:00:00', '03/01/2020 13:00:00', 1, 2, 1);
insert into Cases values (default, 'Product malfunction', 'Product not working as intended', 'Closed', '04/01/2020 16:45:00', '04/01/2020 16:50:15', 3, 2, 4);
insert into Cases values (default, 'Customer wants to exchange item', 'Customer realized they needed more functionality', 'Closed', '04/04/2020 15:00:00', '04/04/2020 16:30:00', 2, 4, 3);
insert into Cases values (default, 'Product performance error', 'Unknown issue causing error in certain scenarios', 'Active', '04/15/2020 12:00:00', null, 3, 6, null);

insert into Comments values (default, 'Customer wants large feature request. Backlogged until next update', '02/26/2020 09:00:30', 2);
insert into Comments values (default, 'Consider adding feature to Signature product', '04/04/2020 15:30:30', 5);
insert into Comments values (default, 'When activating both features at once, error occurs', '04/15/2020 12:45:10', 6);
insert into Comments values (default, 'Error only occurs with latest version of product', '04/16/2020 11:20:00', 6);



