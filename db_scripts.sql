drop table scores;
drop table player_performance;

create table scores(player_name varchar(100), handicap_1 integer, front_day_1 integer, back_day_1 integer, total_day_1 integer, handicap_2 integer, front_day_2 integer, back_day_2 integer, total_day_2, PRIMARY KEY (player_name));



create table player_performance(player_name varchar(100), hole_number integer, course varchar(100), score integer, points integer, day integer, play_date date default(datetime('now','localtime')), PRIMARY KEY (player_name,hole_number,day));



create table course_details(name varchar(100), hole_number integer, par integer, si_index integer, primary key(name,hole_number));

insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 1,4,7);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 2,4,3);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 3,4,1);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 4,4,9);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 5,5,15);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 6,3,13);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 7,5,11);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 8,4,5);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 9,3,17);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 10,5,14);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 11,3,6);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 12,5,16);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 13,4,8);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 14,4,18);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 15,4,2);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 16,3,12);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 17,4,10);
insert into course_details(name,hole_number,par,si_index) values ('MOUNT WOSELEY', 18,4,4);




