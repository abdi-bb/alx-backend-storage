-- Create a stored procedure to add a bonus correction
DROP PROCEDURE IF EXISTS AddBonus; 
DELIMITER $$
CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_count INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;
    
    -- Check if the project already exists or create it
    SELECT count(id)
        INTO project_id
        FROM projects
        WHERE name = project_name;
    IF project_id IS NULL THEN
        INSERT INTO projects (name)
            VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;
    
    SELECT id
        INTO project_id
        FROM projects
        WHERE name = project_name;

    -- Insert the new correction
    INSERT INTO corrections (user_id, project_id, score)
        VALUES (user_id, project_id, score);
END;
$$
DELIMITER ;
