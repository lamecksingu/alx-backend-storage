-- Create a stored procedure that computes and store
-- the average weighted score for ALL the students
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE done INT DEFAULT FALSE;
	DECLARE user_id INT;

	-- Declare cursor for users ids
	DECLARE id_cursor CURSOR FOR
		SELECT id FROM users;

	-- Declare continue handler to exit the loop
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

	-- Open the cursor
	OPEN id_cursor;

	-- Loop Through cursor
	id_loop: LOOP
		-- Fetch next id into user_id
		FETCH id_cursor INTO user_id;

		-- Leave if done
		IF done = TRUE THEN
			LEAVE id_loop;
		END IF;

		-- Compute sum of weights
		SELECT SUM(weight) INTO @weight_sum FROM projects;

		-- Compute (score * weight) + (score * weight) + ...
		SELECT SUM(c.score * p.weight) INTO @scores_weights_products_sum
		FROM projects p
		JOIN corrections c
		ON p.id = c.project_id
		WHERE c.user_id = user_id;

		SET @average_weighted_score = @scores_weights_products_sum / @weight_sum;

		-- Store average_score
		UPDATE users
		SET users.average_score = @average_weighted_score
		WHERE users.id = user_id;

	END LOOP;

	-- Close cursor
	CLOSE id_cursor;
END//
