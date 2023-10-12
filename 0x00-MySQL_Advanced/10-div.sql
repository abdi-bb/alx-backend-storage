-- Create a function SafeDiv
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    IF b <> 0 THEN
        RETURN a / b;
    ELSE
        RETURN 0;
    END IF;
END;
$$
DELIMITER ;