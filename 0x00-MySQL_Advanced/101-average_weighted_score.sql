-- Create a stored procedure to compute and store the average weighted score for all users
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    
    -- Declare cursor to iterate over user IDs
    DECLARE cur CURSOR FOR SELECT id FROM users;
    
    -- Variables to store user-specific weighted scores and total weights
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE weighted_average FLOAT;
    
    -- Initialize variables
    SET total_score = 0;
    SET total_weight = 0;
    SET weighted_average = 0;
    
    -- Loop through user IDs
    OPEN cur;
    FETCH cur INTO user_id;
    
    WHILE user_id IS NOT NULL DO
        -- Calculate the weighted average score for each user
        SELECT SUM(c.score * p.weight) INTO total_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;
        
        IF total_weight > 0 THEN
            SET weighted_average = total_score / total_weight;
        ELSE
            SET weighted_average = 0;
        END IF;
        
        -- Update the user's average_score
        UPDATE users
        SET average_score = weighted_average
        WHERE id = user_id;
        
        -- Fetch the next user ID
        FETCH cur INTO user_id;
    END WHILE;
    
    -- Close the cursor
    CLOSE cur;
    
END $$
DELIMITER ;
