document.addEventListener("DOMContentLoaded", () => {
    const columns = document.querySelectorAll(".kanban-column .kanban-tasks");

    let draggedTask = null;

    // Handle dragging
    document.querySelectorAll(".kanban-task").forEach((task) => {
        task.addEventListener("dragstart", (e) => {
            draggedTask = e.target;
            setTimeout(() => {
                e.target.style.display = "none";
            }, 0);
        });

        task.addEventListener("dragend", (e) => {
            setTimeout(() => {
                draggedTask.style.display = "block";
                draggedTask = null;
            }, 0);
        });
    });

    // Handle dropping
    columns.forEach((column) => {
        column.addEventListener("dragover", (e) => {
            e.preventDefault();
        });

        column.addEventListener("drop", (e) => {
            e.preventDefault();
            if (draggedTask) {
                column.appendChild(draggedTask);

                // Update task status via AJAX
                const taskId = draggedTask.getAttribute("data-task-id");
                const newStatus = column.id.replace("-tasks", ""); // Extract new status
                fetch(`/update_task_status/${taskId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ status: newStatus }),
                }).then((response) => {
                    if (!response.ok) {
                        alert("Failed to update task status.");
                    }
                });
            }
        });
    });
});
document.querySelectorAll(".kanban-task").forEach((task) => {
    task.addEventListener("click", () => {
        const taskId = task.getAttribute("data-task-id");
        fetch(`/get_task_details/${taskId}`)
            .then((response) => response.json())
            .then((data) => {
                // Show task details in a modal
                alert(`Task: ${data.name}\nDescription: ${data.description}\nDue Date: ${data.dueDate}\nPriority: ${data.priority}`);
            });
    });
});
const normalizeStatus = (columnId) => {
    switch (columnId) {
        case "todo-tasks":
            return "to-do";
        case "in-progress-tasks":
            return "in-progress";
        case "done-tasks":
            return "done";
        default:
            return null;
    }
};

// Handle dropping
columns.forEach((column) => {
    column.addEventListener("dragover", (e) => {
        e.preventDefault();
    });

    column.addEventListener("drop", (e) => {
        e.preventDefault();
        if (draggedTask) {
            const newStatus = normalizeStatus(column.id);
            if (!newStatus) {
                alert("Invalid column ID");
                return;
            }

            const taskId = draggedTask.getAttribute("data-task-id");

            // Send the updated status to the server
            fetch(`/update_task_status/${taskId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ status: newStatus }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.error) {
                        alert(`Error: ${data.error}`);
                    } else {
                        column.appendChild(draggedTask); // Move task visually
                    }
                });
        }
    });
});
