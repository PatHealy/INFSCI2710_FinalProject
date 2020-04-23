----------Triggers--------------
-- when the resolution_id is inserted, the c_timeend automatically changes to the current time and c_status changes to closed.--
CREATE OR REPLACE FUNCTION cases_status()
RETURNS trigger AS
$BODY$
BEGIN
	IF NEW.resolution_id <> OLD.resolution_id THEN
		 INSERT INTO cases(c_status,c_timeend)
		 VALUES('Closed',now());
	END IF;
	RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE;

CREATE TRIGGER cases_status
BEFORE UPDATE
ON cases
FOR EACH ROW
EXECUTE PROCEDURE cases_status();

----when the customer applies for refund, delete the relevant record in the orders table----
CREATE OR REPLACE FUNCTION delete_record()
RETURNS trigger AS
$BODY$
BEGIN
	IF NEW.resolution_id == 5 THEN
		DELETE FROM orders WHERE customer_id = old.customer_id and product_id = old.product_id;
	END IF;
	RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE;

CREATE TRIGGER delete_record
BEFORE UPDATE
ON cases
FOR EACH ROW
EXECUTE PROCEDURE delete_record();