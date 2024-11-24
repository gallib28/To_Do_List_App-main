document.addEventListener("DOMContentLoaded", () => {
    const columns = document.querySelectorAll(".kanban-tasks");
    let draggedTask = null;

    // פונקציה לנרמול סטטוס בהתאם ל-id של העמודה
    const normalizeStatus = (columnId) => {
        switch (columnId) {
            case "todo-tasks":
                return "to-do"; // ודא שזה מתאים לשרת
            case "in-progress-tasks":
                return "in progress"; // ודא שזה מתאים לשרת
            case "done-tasks":
                return "done"; // ודא שזה מתאים לשרת
            default:
                console.error("Unknown column ID:", columnId);
                return null;
        }
    };

    // מאזינים למשימות
    const addTaskListeners = () => {
        document.querySelectorAll(".kanban-task").forEach((task) => {
            // מאזין לגרירה
            task.addEventListener("dragstart", (e) => {
                draggedTask = e.target;
                console.log("Drag started for task:", draggedTask.getAttribute("data-task-id"));
                setTimeout(() => {
                    draggedTask.style.display = "none"; // הסתרת המשימה בזמן הגרירה
                }, 0);
            });

            task.addEventListener("dragend", (e) => {
                console.log("Drag ended for task:", draggedTask?.getAttribute("data-task-id"));
                setTimeout(() => {
                    if (draggedTask) draggedTask.style.display = "block"; // הצגת המשימה מחדש
                }, 0);
            });

            // מאזין ללחיצה על משימה לפתיחת עמוד פרטי המשימה
            task.addEventListener("click", () => {
                const taskId = task.getAttribute("data-task-id");
                console.log(`Navigating to details page for task ID: ${taskId}`);
                window.location.href = `/task/${taskId}`; // הפניה לעמוד פרטי המשימה
            });
        });
    };

    // מאזיני Drag על העמודות
    columns.forEach((column) => {
        column.addEventListener("dragover", (e) => {
            e.preventDefault();
            console.log("Dragging over column:", column.id);
            column.classList.add("dragover");
        });

        column.addEventListener("dragleave", () => {
            column.classList.remove("dragover");
        });

        column.addEventListener("drop", (e) => {
            e.preventDefault();
            column.classList.remove("dragover");
            console.log("Drop event triggered on column:", column.id);

            if (draggedTask) {
                const taskId = draggedTask.getAttribute("data-task-id");
                const newStatus = normalizeStatus(column.id);

                if (!newStatus) {
                    console.error("Invalid column ID or status");
                    return;
                }

                console.log("Task ID:", taskId, "New Status:", newStatus);

                // שליחת בקשת POST לשרת לעדכון הסטטוס
                fetch(`/update_task_status/${taskId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        status: newStatus,
                    }),
                })
                    .then(async (response) => {
                        const responseBody = await response.json();
                        if (response.ok) {
                            console.log(`Task ${taskId} successfully updated to ${newStatus}`);

                            // בדוק אם draggedTask הוא Node תקין
                            console.log("Before appending task:", draggedTask);
                            if (draggedTask && draggedTask instanceof Node) {
                                column.appendChild(draggedTask); // העברת המשימה לעמודת היעד
                                console.log("Task appended successfully.");
                            } else {
                                console.error("draggedTask is invalid or not found in DOM:", draggedTask);
                                alert("An error occurred while moving the task. Please refresh the page and try again.");
                            }
                        } else {
                            console.error(`Failed to update task ${taskId} to ${newStatus}`, responseBody);
                            alert(`Failed to update task status: ${responseBody.error}`);
                        }
                    })
                    .catch((error) => {
                        console.error("Error in updating task status:", error);
                        alert("An error occurred while updating task status.");
                    });
            }
        });
    });

    // הפעלת מאזינים על המשימות
    addTaskListeners();
});
