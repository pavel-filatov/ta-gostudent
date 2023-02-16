/* 1. What are the most popular subjects? How many lessons were conducted on these subjects?
   (The most popular subject is the subject on which the maximum number of lessons was conducted.
   Some subjects can have the same number of lessons, we want to see them all in the results in this
   case.)
*/

WITH aggregated_lessons AS (
	SELECT
		subject_name,
		count(1) AS lessons_done
	FROM
		lessons l
	JOIN subjects s on
		l.subject_id = s.subject_id
	GROUP BY
		l.subject_id
),
ranked_lessons AS (
	SELECT *, RANK() OVER(ORDER BY lessons_done DESC) AS rank
	FROM aggregated_lessons
)
SELECT * FROM ranked_lessons WHERE rank = 1

