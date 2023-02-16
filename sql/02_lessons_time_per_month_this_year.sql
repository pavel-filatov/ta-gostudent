/* 2. How many hours were spent on lessons each month of this year?
 */

SELECT
	STRFTIME("%Y-%m", start_dttm, "start of month") AS month,
	ROUND(SUM(unixepoch(end_dttm) - unixepoch(start_dttm)) / 60 / 60.0, 1) as total_lessons_time_hours
FROM
	lessons l
WHERE STRFTIME("%Y", start_dttm) = STRFTIME("%Y", "now")
GROUP BY 1
