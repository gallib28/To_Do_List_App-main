document.addEventListener("DOMContentLoaded", () => {
    const addTaskBtn = document.getElementById("add-task-btn");
    const addTaskPopup = document.getElementById("add-task-popup");
    const closePopupBtn = document.getElementById("close-popup-btn");
    const addTaskForm = document.getElementById("add-task-form");

    // Show the popup when the "Add Task" button is clicked
    addTaskBtn.addEventListener("click", () => {
        addTaskPopup.classList.remove("hidden");
    });

    // Close the popup
    closePopupBtn.addEventListener("click", () => {
        addTaskPopup.classList.add("hidden");
    });

    // Handle task submission
    addTaskForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const taskName = document.getElementById("task_name").value;
        const taskDescription = document.getElementById("task_description").value;
        const taskDueDate = document.getElementById("task_due_date").value;
        const taskPriority = document.getElementById("task_priority").value;

        // Send the task data to the server
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

        // Check server response and show GPT suggestions
        if (result.success) {
            const subtasks = result.suggestions;
            const userChoice = confirm(
                `Suggested subtasks:\n${subtasks.join("\n")}\n\nDo you want to add these subtasks?`
            );
            if (userChoice) {
                alert("Subtasks added successfully!");
            } else {
                alert("No subtasks were added.");
            }
        }

        // Close the popup
        addTaskPopup.classList.add("hidden");
        // Optionally, refresh the table or update the UI
        location.reload();
    });
});
