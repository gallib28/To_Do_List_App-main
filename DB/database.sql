create table users (
	user_id integer not null primary key AUTO_INCREMENT,
	user_username varchar(200) not null UNIQUE  ,
	user_password varchar(200) not null
);
create table Tasks(
	task_id integer NOT null primary key AUTO_INCREMENT  ,
    
	task_dueDate DATE  null,
    
	task_type char(1) not null,
	constraint check_task_type check (task_type in ('w','s','p','t')),
	
    task_name varchar(100) not null ,
    constraint check_task_name check (task_name REGEXP '[a-zA-Zא-ת]' ),
    
	task_description varchar(100) not null ,
	constraint check_task_description check (task_description REGEXP  '[a-zA-Zא-ת]' ),
	
	task_status varchar(11) not null default "to-do",
	constraint check_task_status check (task_status in ("in progress","done","To-do")),
	
	user_id integer , 
	FOREIGN KEY (user_id) references users(user_id) ON DELETE CASCADE ,
	
    parent_task_id INTEGER default null,
    FOREIGN KEY (parent_task_id) REFERENCES Tasks(task_id) ON DELETE CASCADE  ,
    
    task_priority char(1) not null , 
    constraint check_task_priority check (task_priority in ('1','2','3'))
);
insert into users (user_username,user_password) values 
('gallib','gallib'),
('shahar','shahar') 
;
insert into tasks(task_id,task_dueDate,task_type,task_name,task_description,task_status,user_id,parent_task_id,task_priority) values
 (1,'2024-10-13',"s","ללמוד למבחן במבני נתונים","e","To-do",1,1,'2'),
 (2,'2024-10-13',"s","הרצאה 1","e","To-do",1,1,'2'),
 (3,'2024-10-13',"s","הרצאה 2","e","To-do",1,1,'2'),
 (4,'2024-10-13',"s","jrt","e","To-do",2,1,'2'),
 (5,'2024-10-13',"s","jrt 4","e","To-do",2,1,'2'),
 (6,'2024-09-30',"s","jrt3234","e","To-do",2,1,'2')
 ;



select * from tasks ; 


delete from users 
where user_username = "test_user";
delete from tasks 
where user_id = "1";

drop table tasks ;
drop table users ;

-- query for due <= 5 
select task_id,task_dueDate,task_status ,DATEDIFF(task_dueDate, CURRENT_DATE) AS days_until_due
from tasks 
where DATEDIFF(task_dueDate, CURRENT_DATE) <= 5 and task_status != "done" ;

-- query for quantity of unfinished tasks 
select task_id,task_name,task_status 
from tasks 
where task_status != "done" ;

-- query for unfinished tasks for tommorow 
select task_id,task_name,task_status 
from tasks 
where task_status != "done" and DATEDIFF(task_dueDate, CURRENT_DATE)=1;

-- query for counting unfinished tasks of the user
select task_id,task_name,task_status 
from tasks 
where task_status != "done" and  DATEDIFF(task_dueDate, CURRENT_DATE) >= 0 ;

-- query for counting finished tasks of the user
select task_id,task_name,task_status 
from tasks 
where task_status = "done" and  DATEDIFF(task_dueDate, CURRENT_DATE) > 0 ;

-- getting all the high prioraty tasks
select task_id,task_name,task_priority
from tasks 
where task_priority = '2' ;


-- queries for updating task status
update tasks 
set task_status = "in progress" 
where task_id = 1;
update tasks 
set task_status = "done" 
where task_id = 1;
update tasks 
set task_status = "To-do" 
where task_id = 1;


-- queries for updating task description 
update tasks 
set task_description = "description" 
where task_id = 1;

-- queries for updating task description 
update tasks 
set task_name = "name" 
where task_id = 1;


-- queries for updating task priority 
update tasks 
set task_priority = "1" 
where task_id = 1 and task_priority != "1" ;
update tasks 
set task_priority = "2" 
where task_id = 1 and task_priority != "2" ;
update tasks 
set task_priority = "3" 
where task_id = 1 and task_priority != "3" ;

-- deleting tuples
delete from tasks 
where task_id=1;
delete from users 
where user_id=3;

-- queries for updating task types 
update tasks 
set task_type = "w" 
where task_id = 1 ;
update tasks 
set task_type = "p" 
where task_id = 1  ;
update tasks 
set task_type = "s" 
where task_id = 1 ;
update tasks 
set task_type = "t" 
where task_id = 1;




update tasks 
set task_type = "w" 
where task_id = 1 ;
update tasks 
set task_type = "p" 
where task_id = 1  ;
update tasks 
set task_type = "s" 
where task_id = 1 ;
update tasks 
set task_type = "t" 
where task_id = 1;







