-- Create a stored procedure to compute and store the average weighted score for a user
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE weighted_average FLOAT;
    
    -- Initialize variables
    SET total_score = 0;
    SET total_weight = 0;
    SET weighted_average = 0;
    
    -- Calculate the weighted average score for the user
    SELECT SUM(c.score * p.weight) INTO total_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    IF total_weight > 0 THEN
        SET weighted_average = total_score / total_weight;
    END IF;
    
    -- Update the user's average_score
    UPDATE users
    SET average_score = weighted_average
    WHERE id = user_id;
END $$
DELIMITER ;
