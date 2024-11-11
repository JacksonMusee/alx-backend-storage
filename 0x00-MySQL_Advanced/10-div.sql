-- SQL script that creates a function SafeDiv that divides (and returns) the first by the
-- second number or returns 0 if the second number is equal to 0.

DELIMITER $$

CREATE FUNCTION SafeDiv(num1 INT, num2 INT)
RETURNS FLOAT
BEGIN
	IF num2 = 0 THEN
		RETURN 0;
	ELSE
		RETURN num1 / num2;
	END IF;
END $$

DELIMITER ;
