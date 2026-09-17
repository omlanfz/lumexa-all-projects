// Crew Task Tracker — Interactive To-Do App
// Architecture: single source of truth (`tasks` + `currentFilter`) + one render() function.

const STORAGE_KEY = "lumexa-crew-tasks-v1";

// --- ELEMENTS ---
const taskForm = document.querySelector("#task-form");
const taskInput = document.querySelector("#task-input");
const prioritySelect = document.querySelector("#priority-select");
const formError = document.querySelector("#form-error");
const taskListEl = document.querySelector("#task-list");
const filterButtons = document.querySelectorAll(".filter-btn");
const clearCompletedBtn = document.querySelector("#clear-completed-btn");
const taskCounterEl = document.querySelector("#task-counter");
const emptyStateEl = document.querySelector("#empty-state");

// --- STATE (single source of truth) ---
let tasks = loadTasks();
let currentFilter = "all";
let editingId = null; // id of the task currently being edited in-place, or null

// --- STORAGE FUNCTIONS ---
function loadTasks() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw === null) return [];
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    // Defensive normalization in case older/corrupted data is missing fields
    return parsed
      .filter((item) => item && typeof item.text === "string")
      .map((item) => ({
        id: typeof item.id === "number" ? item.id : Date.now() + Math.random(),
        text: item.text,
        completed: Boolean(item.completed),
        priority: ["low", "medium", "high"].includes(item.priority) ? item.priority : "medium",
      }));
  } catch (error) {
    console.error("Corrupted task data in Local Storage, resetting.", error);
    return [];
  }
}

function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

// --- STATE-CHANGING FUNCTIONS ---
function addTask(text, priority) {
  tasks.push({ id: Date.now(), text, completed: false, priority });
  saveTasks();
  render();
}

function toggleTask(id) {
  tasks = tasks.map((task) =>
    task.id === id ? { ...task, completed: !task.completed } : task
  );
  saveTasks();
  render();
}

function deleteTask(id) {
  tasks = tasks.filter((task) => task.id !== id);
  saveTasks();
  render();
}

function editTaskText(id, newText) {
  const trimmed = newText.trim();
  if (trimmed === "") {
    // An emptied-out edit deletes the task rather than saving a blank one
    deleteTask(id);
    return;
  }
  tasks = tasks.map((task) => (task.id === id ? { ...task, text: trimmed } : task));
  saveTasks();
  render();
}

function clearCompleted() {
  tasks = tasks.filter((task) => !task.completed);
  saveTasks();
  render();
}

function setFilter(filterName) {
  currentFilter = filterName;
  render();
}

// --- DERIVED STATE ---
function getVisibleTasks() {
  if (currentFilter === "active") return tasks.filter((task) => !task.completed);
  if (currentFilter === "completed") return tasks.filter((task) => task.completed);
  return tasks;
}

// --- RENDER (rebuilds the UI entirely from current state) ---
function render() {
  const visibleTasks = getVisibleTasks();

  taskListEl.innerHTML = "";
  emptyStateEl.hidden = tasks.length > 0;

  visibleTasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task-item";
    li.dataset.id = task.id;
    if (task.completed) li.classList.add("completed");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "toggle-checkbox";
    checkbox.checked = task.completed;
    checkbox.setAttribute("aria-label", `Mark "${task.text}" as complete`);

    let textNode;
    if (editingId === task.id) {
      textNode = document.createElement("input");
      textNode.type = "text";
      textNode.className = "task-edit-input";
      textNode.value = task.text;
      textNode.maxLength = 140;
    } else {
      textNode = document.createElement("span");
      textNode.className = "task-text";
      textNode.textContent = task.text;
      textNode.title = "Double-click to edit";
    }

    const priorityBadge = document.createElement("span");
    priorityBadge.className = `priority-badge priority-${task.priority}`;
    priorityBadge.textContent = task.priority;

    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "delete-btn";
    deleteBtn.textContent = "Delete";
    deleteBtn.setAttribute("aria-label", `Delete "${task.text}"`);

    li.append(checkbox, textNode, priorityBadge, deleteBtn);
    taskListEl.appendChild(li);

    // Focus the edit input immediately after it's inserted into the DOM
    if (editingId === task.id) {
      textNode.focus();
      textNode.setSelectionRange(textNode.value.length, textNode.value.length);
    }
  });

  filterButtons.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.filter === currentFilter);
  });

  const remaining = tasks.filter((task) => !task.completed).length;
  if (tasks.length === 0) {
    taskCounterEl.textContent = "";
  } else {
    taskCounterEl.textContent = `${remaining} task${remaining === 1 ? "" : "s"} left of ${tasks.length} total`;
  }

  clearCompletedBtn.hidden = tasks.every((task) => !task.completed);
}

// --- EVENTS ---
taskForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = taskInput.value.trim();
  if (text === "") {
    formError.textContent = "Type a task before adding it.";
    return;
  }
  formError.textContent = "";
  addTask(text, prioritySelect.value);
  taskInput.value = "";
  taskInput.focus();
});

// Event delegation: one listener handles toggle, delete, and edit-entry
// for every task, including tasks added after the page first loaded.
taskListEl.addEventListener("click", (event) => {
  const li = event.target.closest(".task-item");
  if (!li) return;
  const id = Number(li.dataset.id);

  if (event.target.classList.contains("toggle-checkbox")) {
    toggleTask(id);
  } else if (event.target.classList.contains("delete-btn")) {
    deleteTask(id);
  }
});

taskListEl.addEventListener("dblclick", (event) => {
  const textEl = event.target.closest(".task-text");
  if (!textEl) return;
  const li = event.target.closest(".task-item");
  editingId = Number(li.dataset.id);
  render();
});

// Saving an in-place edit: Enter key or blurring the input
taskListEl.addEventListener(
  "blur",
  (event) => {
    if (!event.target.classList.contains("task-edit-input")) return;
    const li = event.target.closest(".task-item");
    const id = Number(li.dataset.id);
    // Clear editingId BEFORE calling editTaskText, since editTaskText triggers
    // render() itself — clearing it after would leave that render() showing
    // the edit <input> again instead of reverting to plain text.
    editingId = null;
    editTaskText(id, event.target.value);
  },
  true // capture phase needed because "blur" does not bubble
);

taskListEl.addEventListener("keydown", (event) => {
  if (!event.target.classList.contains("task-edit-input")) return;
  if (event.key === "Enter") {
    event.target.blur(); // triggers the blur handler above, which saves
  } else if (event.key === "Escape") {
    editingId = null;
    render();
  }
});

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => setFilter(btn.dataset.filter));
});

clearCompletedBtn.addEventListener("click", clearCompleted);

// --- INITIAL RENDER ON PAGE LOAD ---
render();
