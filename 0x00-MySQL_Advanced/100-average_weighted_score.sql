-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

-- Requirements:

-- Procedure ComputeAverageScoreForUser is taking 1 input:
--      user_id, a users.id value (you can assume user_id is linked to an existing user

DELIMITER $$

-- Create the stored procedure to compute average weighted score for a user
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE av_score FLOAT;

    -- Calculate the weighted average score
    SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
    INTO av_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- If there are no corrections for the user, set average score to 0
    IF av_score IS NULL THEN
        SET av_score = 0;
    END IF;

    -- Update the user's average score in the 'users' table
    UPDATE users
    SET average_score = av_score
    WHERE id = user_id;
END $$

DELIMITER ;
