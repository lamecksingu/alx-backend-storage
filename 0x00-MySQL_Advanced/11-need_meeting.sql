-- Create a view need_meeting that lists all students that have:
-- A score under 80 (strict)
-- No last_meeting or more than 1 month
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE students.score < 80
AND (students.last_meeting IS NULL
	OR students.last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH));
