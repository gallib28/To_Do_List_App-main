document.addEventListener("DOMContentLoaded", () => {
    console.log("Main JavaScript loaded.");
});
document.getElementById("tasks-list").addEventListener("click", async (e) => {
    if (confirm("Would you like suggestions for subtasks?")) {
        alert("Fetching subtasks suggestions...");
    }
});
