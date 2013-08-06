SELECT SUM(X.SCORE) FROM (
SELECT * FROM PLAYER_PERFORMANCE 
WHERE PLAYER_NAME='EBBO' ORDER BY HOLE_NUMBER LIMIT 9,18



-- Winner front 9 day 1
select player_name,front_day_1 from scores order by front_day_1 desc limit 1

-- Winner Back 9 Day 1
select player_name,back_day_1 from scores order by back_day_1 desc limit 1


-- Winner front 9 day 2

select player_name,front_day_2 from scores order by front_day_2 desc limit 1

-- Winner back 9 day 2

select player_name,back_day_2 from scores order by back_day_2 desc limit 1


--- Overall Winner
select player_name as overall_winner, total_day_1+total_day_2 as total  as points from scores order by total desc limit 2


--- PAR 3 SCRAMBLE
SELECT PLAYER_NAME,SUM(POINTS) from(
select PLAYER_NAME, POINTS from player_performance  P, COURSE_DETAILS D
WHERE D.HOLE_NUMBER = P.HOLE_NUMBER AND p.day=2

