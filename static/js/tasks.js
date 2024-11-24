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
function openTaskForm() {
    const modal = document.getElementById("task-modal");
    modal.style.display = "block";
  }
  
  function closeTaskForm() {
    const modal = document.getElementById("task-modal");
    modal.style.display = "none";
  }
  
  function submitTaskForm() {
    const taskData = {
        task_name: document.getElementById("task-name").value.trim(),
        task_description: document.getElementById("task-description").value.trim(),
        task_due_date: document.getElementById("task-due-date").value || null,
        task_type: document.getElementById("task-type")?.value || 'p', // Default to 'p'
        task_status: document.getElementById("task-status")?.value || 'to-do', // Default to 'to-do'
        task_priority: document.getElementById("task-priority").value || null,
        parent_task_id: null, // Main task has no parent
    };

    // Validate required fields
    if (!taskData.task_name || !taskData.task_description) {
        alert("Task Name and Description are required.");
        return;
    }

    fetch("/add_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(taskData),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Task added successfully!");
                fetchGPTSuggestions(data.task_id, taskData); // Fetch GPT suggestions for the added task
            } else {
                alert("Failed to add task: " + data.error);
            }
        })
        .catch((error) => {
            console.error("Error adding task:", error);
            alert("An error occurred while adding the task. Please try again.");
        });
}

function fetchGPTSuggestions(taskId, taskData) {
    fetch("/get_gpt_assistance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(taskData),
    })
        .then((response) => response.json())
        .then((gptData) => {
            if (gptData.success) {
                displayGPTSuggestions(gptData.suggestions, taskId);
            } else {
                alert("Failed to fetch GPT suggestions.");
            }
        })
        .catch((error) => {
            console.error("Error fetching GPT suggestions:", error);
            alert("An error occurred while fetching GPT suggestions.");
        });
}

function displayGPTSuggestions(suggestions, parentTaskId) {
    // Create a modal to display GPT suggestions
    const modal = document.createElement("div");
    modal.id = "gpt-suggestions-modal";
    modal.style.position = "fixed";
    modal.style.top = "50%";
    modal.style.left = "50%";
    modal.style.transform = "translate(-50%, -50%)";
    modal.style.background = "#fff";
    modal.style.padding = "20px";
    modal.style.boxShadow = "0 0 10px rgba(0,0,0,0.5)";
    modal.innerHTML = `
        <h3>GPT Suggestions</h3>
        <ul id="suggestions-list">
            ${suggestions.map((suggestion, index) => `<li>
                <input type="checkbox" id="suggestion-${index}" value="${suggestion}">
                <label for="suggestion-${index}">${suggestion}</label>
            </li>`).join("")}
        </ul>
        <button id="add-selected-suggestions">Add Selected Suggestions</button>
        <button id="close-suggestions-modal">Close</button>
    `;
    document.body.appendChild(modal);

    // Add event listeners
    document.getElementById("add-selected-suggestions").addEventListener("click", () => {
        const selectedSuggestions = [];
        document.querySelectorAll("#suggestions-list input:checked").forEach((checkbox) => {
            selectedSuggestions.push(checkbox.value);
        });
        addSubtasks(selectedSuggestions, parentTaskId);
        modal.remove(); // Close modal
    });

    document.getElementById("close-suggestions-modal").addEventListener("click", () => {
        modal.remove(); // Close modal
    });
}

function addSubtasks(suggestions, parentTaskId) {
    const subtasks = suggestions.map((suggestion) => ({
        task_name: suggestion,
        task_description: `Subtask for ${suggestion}`,
        task_due_date: null, // Optional
        task_type: 's', // Subtask type
        task_status: 'to-do',
        task_priority: null,
        parent_task_id: parentTaskId,
    }));

    fetch("/add_subtasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subtasks }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Subtasks added successfully!");
                location.reload();
            } else {
                alert("Failed to add subtasks.");
            }
        })
        .catch((error) => {
            console.error("Error adding subtasks:", error);
            alert("An error occurred while adding subtasks.");
        });
}
