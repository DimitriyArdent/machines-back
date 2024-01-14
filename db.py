
'''



CREATE TABLE Users (
    UserId SERIAL PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    FullName VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

INSERT INTO Users (Username, FullName, Password) 
VALUES ('johns', 'John Smith', 'P@ssw07d!');

ALTER TABLE Users
ADD CONSTRAINT unique_full_name UNIQUE (FullName);






CREATE TABLE MachineManufacturers (
    ManufacturerId SERIAL PRIMARY KEY,
    ManufacturerName VARCHAR(255) NOT NULL
);

INSERT INTO MachineManufacturers (ManufacturerId, ManufacturerName) 
VALUES (1, 'Arburg'), (2, 'ABB');






CREATE TABLE Machines (
    MachineId SERIAL PRIMARY KEY,
    MachineName VARCHAR(255) NOT NULL,
    ManufacturerId INTEGER REFERENCES MachineManufacturers(ManufacturerId),
    PurchaseDateTime TIMESTAMP NOT NULL,
    YearOfManufacture INTEGER NOT NULL,
    MachineStatus INTEGER NOT NULL CHECK (MachineStatus IN (0, 1)),
    Capacity DECIMAL(5, 2) NOT NULL CHECK (Capacity >= 0 AND Capacity <= 1)
 );

 

 

INSERT INTO Machines (MachineName, ManufacturerId, PurchaseDateTime, YearOfManufacture, MachineStatus, Capacity)
SELECT
    'Machine ' || gs AS MachineName,
    (gs % 2) + 1 AS ManufacturerId,
    NOW() - INTERVAL '1 year' * (gs % 5) AS PurchaseDateTime,
    2020 - (gs % 10) AS YearOfManufacture,
    gs % 2 AS MachineStatus,
    RANDOM() AS Capacity
FROM
    GENERATE_SERIES(1, 100) gs;


    


 CREATE TABLE images (
    imageid SERIAL PRIMARY KEY,
    imageurl TEXT,
    machineid INT 
 );
ALTER TABLE images
ADD CONSTRAINT unique_machineid
UNIQUE (machineid);















CREATE OR REPLACE FUNCTION login(p_fullname text, p_password text)
RETURNS setof users 
AS 
$$
   Select * 
   From users 
   where fullname = p_fullname and password = p_password ;
$$ LANGUAGE sql;







    CREATE OR REPLACE FUNCTION get_machines(p_limit int default 10)
RETURNS setof machines 
AS 
$$
   Select * 
   From machines 
   order by purchasedatetime  desc
   limit p_limit
   ;
$$ LANGUAGE sql;














INSERT INTO  machines(
	machineid, machinename, manufacturerid, purchasedatetime, yearofmanufacture, machinestatus, capacity)
	VALUES (?, ?, ?, ?, ?, ?, ?);
	
	 
    
 	
	
	CREATE OR REPLACE FUNCTION add_machine(
    
    p_machinename text,
    p_manufacturerid int,
    p_purchasedatetime timestamp,
    p_yearofmanufacture int,
    p_machinestatus int,
    p_capacity text
)
RETURNS setof machines
AS
$$
BEGIN
     
    INSERT INTO machines (
          machinename, manufacturerid, 
        purchasedatetime, yearofmanufacture, machinestatus,
        capacity
    )
    VALUES (
          p_machinename, p_manufacturerid,
        p_purchasedatetime, p_yearofmanufacture, p_machinestatus,
        p_capacity
    );

     
    RETURN query select * from machines where machinename = p_machinename ;
 
END;
$$ LANGUAGE plpgsql;
	




	
CREATE OR REPLACE FUNCTION delete_machine(p_machine_id int)
RETURNS bool 
AS 
$$
begin
   delete   
   From machines 
   where machineid = p_machine_id ;
   return true;
end;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION update_machine(
    p_machine_id INT,
	p_machinename VARCHAR DEFAULT NULL,
	 p_manufacturerid INT DEFAULT NULL,
	     p_purchasedatetime TIMESTAMP DEFAULT NULL,
p_yearofmanufacture INT DEFAULT NULL,
   
	  p_machinestatus INT DEFAULT NULL,
     p_capacity VARCHAR DEFAULT NULL
     
     
) RETURNS setof machines as $$
BEGIN
    UPDATE  machines
    SET
         
        machinename = COALESCE(p_machinename, machinename),
        manufacturerid = COALESCE(p_manufacturerid, manufacturerid),
        purchasedatetime = COALESCE(p_purchasedatetime, purchasedatetime),
        yearofmanufacture = COALESCE(p_yearofmanufacture, yearofmanufacture),
		 machinestatus = COALESCE(p_machinestatus, machinestatus),
		 capacity = COALESCE(p_capacity, capacity)
        
        
    WHERE machineid = p_machine_id;
	RETURN QUERY
  SELECT *
  FROM  machines
  WHERE machineid = p_machine_id;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION add_image(
  p_imageurl text,
  p_machineid int 
)
RETURNS setof images
AS
$$
BEGIN
   BEGIN
    INSERT INTO images (imageurl, machineid)
    VALUES (p_imageurl, p_machineid);
  EXCEPTION WHEN unique_violation THEN
    UPDATE images SET imageurl = p_imageurl WHERE machineid = p_machineid;
  END;

  RETURN query select * from images where machineid = p_machineid ;
END;
$$ LANGUAGE plpgsql;




 

'''



 CREATE OR REPLACE FUNCTION filter_machine_name(pattern text)
RETURNS SETOF machines
AS
$$
BEGIN
    RETURN QUERY EXECUTE 'SELECT * FROM machines WHERE machinename LIKE ''%' || pattern || '%''';
END;
$$ LANGUAGE plpgsql;

__________________________________


  CREATE OR REPLACE FUNCTION filter_manufacturerid(pattern integer)
RETURNS SETOF machines
AS
$$
BEGIN
    RETURN QUERY    SELECT * FROM machines WHERE manufacturerid  = pattern ;
END;
$$ LANGUAGE plpgsql;


________________________________-

  CREATE OR REPLACE FUNCTION filter_status(pattern integer)
RETURNS SETOF machines
AS
$$
BEGIN
    RETURN QUERY    SELECT * FROM machines WHERE machinestatus  = pattern ;
END;
$$ LANGUAGE plpgsql;


_____________________

CREATE OR REPLACE FUNCTION order_by(p_direction text, p_variable_name text)
RETURNS SETOF machines
AS
$$
BEGIN
   RETURN QUERY EXECUTE 'SELECT * FROM machines ORDER BY ' || p_variable_name || ' ' || p_direction;
END;
$$ LANGUAGE plpgsql;

