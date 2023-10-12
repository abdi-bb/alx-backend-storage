-- Create a stored procedure to compute and store the average score for a user
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_projects INT DEFAULT 0;

    -- Calculate the total score for the user
    SELECT SUM(score)
        INTO total_score
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Calculate the total number of projects for the user
    SELECT COUNT(*)
        INTO total_projects
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Update the average_score for the user
     UPDATE users
        SET users.average_score = IF(total_projects = 0, 0, total_score / total_projects)
        WHERE users.id = user_id;
END;
$$

DELIMITER ;