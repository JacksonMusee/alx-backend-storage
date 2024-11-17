-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

-- Requirements:

--    Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE av_score FLOAT;
    DECLARE user_id INT;
    DECLARE done INT DEFAULT 0;
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN user_cursor;

    read_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SELECT IFNULL(SUM(projects.weight * corrections.score) / SUM(projects.weight), 0)
        INTO av_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        UPDATE users
        SET average_score = av_score
        WHERE id = user_id;

    END LOOP;

    CLOSE user_cursor;
END $$

DELIMITER ;