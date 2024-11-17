-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

-- Requirements:

-- Procedure ComputeAverageScoreForUser is taking 1 input:
--      user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userID INT)

BEGIN
	DECLARE av_score FLOAT;

	SELECT SUM(projects.weight*corrections.score)/SUM(projects.weight)
	INTO av_score
	FROM corrections JOIN projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = userID;

	UPDATE users
	SET average_score = av_score
	WHERE user_id = userID;
END $$

DELIMITER ;
