/* 2. How many hours were spent on lessons each month of this year?
*/

.width
.headers on
.output output/02_lessons_time_per_month_this_year.txt

SELECT
	STRFTIME("%Y-%m", start_dttm, "start of month") AS month,
	ROUND(SUM(julianday(end_dttm) - julianday(start_dttm)) * 24, 1) AS total_lessons_time_hours
FROM
	lessons l
-- Get this year only
WHERE STRFTIME("%Y", start_dttm) = STRFTIME("%Y", "now")
GROUP BY 1
