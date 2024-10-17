-- Create a stored procedure that adds a new correction for a student
delimiter //
CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
	DECLARE project_id INT;
	DECLARE project_exists INT DEFAULT 0;

	-- Check that the project exists
	SELECT COUNT(*) INTO project_exists
	FROM projects
	WHERE name = project_name;

	-- If it exists, just insert a new correction
	IF project_exists > 0 THEN
		SELECT id INTO project_id 
		FROM projects
		WHERE name = project_name;
		INSERT INTO corrections VALUES (user_id, project_id, score);
	-- Else, create new project first
	ELSE
		INSERT INTO projects (name) VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
		INSERT INTO corrections VALUES (user_id, project_id, score);
	END IF;
END//
