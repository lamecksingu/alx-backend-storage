-- Creates a stored procedure that computes and store 
-- the average score for a student
delimiter //
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE average FLOAT;

	-- Compute average score
	SELECT AVG(score) INTO average
	FROM corrections
	WHERE corrections.user_id = user_id;

	-- Store the average score for the student with user_id
	UPDATE users
	SET users.average_score = average
	WHERE users.id = user_id;
END//
