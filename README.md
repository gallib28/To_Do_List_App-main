# **TaskFlow - Task Management App Characterization Document**

## **1. Overview**
### **1.1 Project Name:**  
WhatToDo - A to-do list and Productivity App

### **1.2 Purpose and Goals:**  
WhatToDo is a web and mobile application designed to help users organize tasks, track deadlines, and improve productivity. The app provides a structured way to manage daily, weekly, and long-term tasks efficiently.

## **2. Features and Functionalities**

### **2.1 User Authentication:**
- Sign up/login using email and password.
- Google login integration.
- Multi-factor authentication for security.

### **2.2 Task Management:**
- Create, edit, delete tasks.
- Assign due dates and priorities.
- Set task categories and labels.
- Mark tasks as completed.
- Add task descriptions and attachments.

### **2.3 Task Collaboration:**
- Share tasks with other users.
- Assign tasks to team members.
- Real-time task updates and notifications.

### **2.4 Task Views & Filters:**
- List view, calendar view, and Kanban board.
- Filter by priority, due date, and category.
- Search functionality for quick access.

### **2.5 Reminders & Notifications:**
- Push and email notifications for task deadlines.
- Customizable reminder settings.

### **2.6 Integration & Synchronization:**
- Sync tasks across multiple devices.
- Integration with Google Calendar.

### **2.7 Analytics & Reporting:**
- Task completion statistics.
- Productivity insights and trends.

## **3. Technology Stack**

### **3.1 Frontend:**
- Web: html,css,js
- Mobile: ??

### **3.2 Backend:**
Python with Flask

### **3.3 Database:**
- mysql on server rpi

### **3.4 Hosting & Deployment:**
- Cloud-based deployment (AWS / Google Cloud / Firebase)
- Docker containerization
- (for now the server of the app and db is on rpi) need to adjust.
### **3.5 all tht functions in backend:**
1. connect_to_db()
2. create_user(username, password)
3. create_task(name, description, due_date, task_type, task_status, user_id, parent_task_id, task_priority)
4. login_user(username, password)
5. update_existing_password(username,old_password,new_password)
6. get_tasks()
7. get_user_tasks(user_id)
8. get_sub_tasks_by_parent_id(parent_task_id)
9. delete_task(task_id)
10. delete_user_db(user_id)
11. get_unfinished_user_tasks(user_id)
12. count_unfinished_tasks_of_user(user_id)
13. check_tasks_u5(user_id)
14. set_task_status(new_status, task_id)
15. set_task_description(string,task_id)
16. set_task_name(name,task_id)
17. get_average_monthly_completed(user_id)
18. update_username_in_db(user_id, username)
19. get_total_completed_tasks(user_id)
20. get_user_by_id(user_id)
21. update_user_theme(user_id, theme_color)
22. set_user_block_status(user_id, is_blocked)
23. get_all_tasks()
24. get_task_by_id(task_id)
25. update_task_in_db(task_id, task_name, description, due_date, priority, status)
26. delete_completed_tasks() 
## **4. User Roles & Permissions**
- **Admin:** Manage users, set global settings, and view reports.
- **User:** Create, manage, and complete tasks.

## **5. User Interface (UI) & User Experience (UX)**
- **Simple and intuitive UI** with minimal learning curve.
- **Dark mode & light mode options** for accessibility.
- **Drag and drop functionality** for easy task management.
- **drag and drop for subtasks. 

## **6. Security Measures**
- End-to-end encryption for sensitive data.
- Role-based access control (RBAC).
- OAuth 2.0 for third-party authentication.

## **7. Performance & Scalability**
- Load balancing to handle high traffic.
- Efficient indexing and caching for fast data retrieval.
- Scalable microservices architecture.

## **8. Future Enhancements**
- AI-based task recommendations.
- Voice command task creation.
- Automated task prioritization based on deadlines and workload.

## **9. Conclusion**
WhatToDo aims to provide an efficient, user-friendly task management solution for individuals. The app will be continuously improved based on user feedback and technological advancements.

