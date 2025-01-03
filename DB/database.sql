create table users (
	user_id integer not null primary key AUTO_INCREMENT,
	user_username varchar(200) not null UNIQUE  ,
	user_password varchar(200) not null
) ENGINE=InnoDB;
CREATE TABLE tasks (
    task_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    task_dueDate DATE NULL,
    task_type CHAR(1) NOT NULL,
    CONSTRAINT check_task_type CHECK (task_type IN ('w', 's', 'p', 't')),
    task_name VARCHAR(100) NOT NULL,
    CONSTRAINT check_task_name CHECK (task_name REGEXP '[a-zA-Zא-ת]'),
    task_description VARCHAR(100) NOT NULL,
    CONSTRAINT check_task_description CHECK (task_description REGEXP '[a-zA-Zא-ת]'),
    task_status VARCHAR(11) NOT NULL DEFAULT "to-do",
    CONSTRAINT check_task_status CHECK (task_status IN ("in progress", "done", "To-do")),
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    parent_task_id INTEGER DEFAULT NULL,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    task_priority CHAR(1) NOT NULL,
    CONSTRAINT check_task_priority CHECK (task_priority IN ('1', '2', '3'))
) ENGINE=InnoDB;

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







