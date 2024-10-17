-- Create a stored procedure that computes and store
-- the average weighted score for a student
delimiter //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
	DECLARE average_weighted_score FLOAT;
	DECLARE weight_sum INT;
	DECLARE scores_weights_products_sum INT;

	-- Compute sum of weights
	SELECT SUM(weight) INTO weight_sum FROM projects;

	-- Compute (score * weight) + (score * weight) + ...
	SELECT SUM(c.score * p.weight) INTO scores_weights_products_sum
	FROM projects p
	JOIN corrections c
	ON p.id = c.project_id
	WHERE c.user_id = user_id;

	SET average_weighted_score = scores_weights_products_sum / weight_sum;

	-- Store average_score
	UPDATE users
	SET users.average_score = average_weighted_score
	WHERE users.id = user_id;
END//
