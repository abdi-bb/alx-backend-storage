-- Stored Procedure the average score of a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INt)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE user_id = users.id
    )
    WHERE id = user_id;
END;
$$
DELIMITER ;