-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
-- Note: An average score can be a decimal

-- Requirements:

-- Procedure ComputeAverageScoreForUser is taking 1 input:
--        user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN userID INT)

BEGIN
	DECLARE av_score FLOAT;

	SELECT AVG(score) INTO av_score
	FROM corrections
	WHERE user_id = userID;

	UPDATE users
	SET average_score = av_score
	WHERE id = userID;
END $$

DELIMITER ;
