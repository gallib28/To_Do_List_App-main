document.addEventListener("DOMContentLoaded", () => {
    console.log("Main JavaScript loaded.");

    const form = document.getElementById("add-task-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const taskName = document.getElementById("task_name").value;
        const taskDescription = document.getElementById("task_description").value;
        const taskDueDate = document.getElementById("task_due_date").value;
        const taskPriority = document.getElementById("task_priority").value;

        // שליחת המשימה לשרת
        const response = await fetch("/add_task", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                task_name: taskName,
                task_description: taskDescription,
                task_due_date: taskDueDate,
                task_priority: taskPriority,
            }),
        });

        const result = await response.json();

        // בדיקת התשובה מהשרת ושאילת המשתמש אם הוא רוצה הצעה לתתי-משימות
        if (confirm("Would you like suggestions for subtasks?")) {
            const subtasks = result.suggestions;
            if (subtasks.length > 0) {
                const selectedSubtasks = prompt(`Suggested subtasks:\n${subtasks.join("\n")}\n\nPlease select the subtasks you want to add (e.g., 1,2,3):`);
                if (selectedSubtasks) {
                    alert(`You have selected the following subtasks:\n${selectedSubtasks}`);
                }
            } else {
                alert("No suggestions were found.");
            }
        }
    });
});
