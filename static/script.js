// API Base URL - Change this if needed
const API_BASE = "";

// State
let users = [];

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  checkServerStatus();
  loadUsers();
  setupNavigation();
  setupForm();
  setupPreview();
});

// Check server status
async function checkServerStatus() {
  const statusDot = document.querySelector(".status-dot");
  const statusText = document.getElementById("server-status");

  try {
    const response = await fetch(`${API_BASE}/health`);
    const data = await response.json();

    if (data.status === "healthy" || response.ok) {
      statusDot.classList.add("online");
      statusDot.classList.remove("offline");
      statusText.textContent = "Server Online";
    } else {
      throw new Error("Unhealthy");
    }
  } catch (error) {
    statusDot.classList.add("offline");
    statusDot.classList.remove("online");
    statusText.textContent = "Server Offline";
  }
}

// Load users from API
async function loadUsers() {
  try {
    const response = await fetch(`${API_BASE}/api/expo-tokens/`);
    users = await response.json();

    updateStats();
    renderRecentUsers();
    renderUsersTable();
    updateUserSelect();
  } catch (error) {
    console.error("Error loading users:", error);
    showToast("Failed to load users", "error");
  }
}

// Update dashboard stats
function updateStats() {
  document.getElementById("total-users").textContent = users.length;
  document.getElementById("total-tokens").textContent = users.length;
}

// Render recent users on dashboard
function renderRecentUsers() {
  const container = document.getElementById("recent-users");

  if (users.length === 0) {
    container.innerHTML = '<p class="loading">No users registered yet</p>';
    return;
  }

  const recentUsers = users.slice(-5).reverse();

  container.innerHTML = recentUsers
    .map(
      (user) => `
        <div class="user-item">
            <div class="user-info">
                <div class="user-avatar"><i class="ri-user-line"></i></div>
                <div class="user-details">
                    <h4>${user.user_id}</h4>
                    <p>${user.device_type || "Unknown device"}</p>
                </div>
            </div>
            <span class="user-token">${user.expo_token.substring(
              0,
              30
            )}...</span>
        </div>
    `
    )
    .join("");
}

// Render users table
function renderUsersTable() {
  const tbody = document.getElementById("users-table-body");

  if (users.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="5" class="loading">No users registered yet</td></tr>';
    return;
  }

  tbody.innerHTML = users
    .map(
      (user) => `
        <tr>
            <td><strong>${user.user_id}</strong></td>
            <td class="token-cell" title="${user.expo_token}">${
        user.expo_token
      }</td>
            <td>${user.device_type || "Unknown"}</td>
            <td>${formatDate(user.created_at)}</td>
            <td>
                <button class="btn btn-secondary btn-sm" onclick="sendToUser('${
                  user.user_id
                }')">
                    <i class="ri-send-plane-line"></i> Send
                </button>
            </td>
        </tr>
    `
    )
    .join("");
}

// Update user select dropdown
function updateUserSelect() {
  const select = document.getElementById("user-id");

  if (users.length === 0) {
    select.innerHTML = '<option value="">No users available</option>';
    return;
  }

  select.innerHTML = users
    .map(
      (user) =>
        `<option value="${user.user_id}">${user.user_id} (${
          user.device_type || "Unknown"
        })</option>`
    )
    .join("");
}

// Navigation
function setupNavigation() {
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const section = item.dataset.section;
      showSection(section);
    });
  });
}

function showSection(sectionId) {
  // Update nav
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.section === sectionId);
  });

  // Update sections
  document.querySelectorAll(".section").forEach((section) => {
    section.classList.toggle("active", section.id === sectionId);
  });

  // Refresh data when switching to users
  if (sectionId === "users") {
    loadUsers();
  }
}

// Form handling
function setupForm() {
  document
    .getElementById("notification-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const target = document.getElementById("target").value;
      const title = document.getElementById("title").value;
      const body = document.getElementById("body").value;

      if (target === "all") {
        await sendNotificationToAll(title, body);
      } else {
        const userId = document.getElementById("user-id").value;
        await sendNotificationToUser(userId, title, body);
      }
    });
}

function toggleUserSelect() {
  const target = document.getElementById("target").value;
  const userSelectGroup = document.getElementById("user-select-group");
  userSelectGroup.style.display = target === "specific" ? "block" : "none";
}

// Preview
function setupPreview() {
  const titleInput = document.getElementById("title");
  const bodyInput = document.getElementById("body");

  titleInput.addEventListener("input", updatePreview);
  bodyInput.addEventListener("input", updatePreview);
}

function updatePreview() {
  const title = document.getElementById("title").value || "Notification Title";
  const body = document.getElementById("body").value || "Notification message";

  document.getElementById("preview-title").textContent = title;
  document.getElementById("preview-body").textContent = body;
}

// API calls
async function sendTestNotification() {
  try {
    showToast("Sending test notification...", "info");

    const response = await fetch(`${API_BASE}/api/notifications/send-test`, {
      method: "POST",
    });

    const data = await response.json();

    if (data.success) {
      showToast(
        `<i class="ri-check-line"></i> Sent: ${data.sent} succeeded, ${data.failed} failed`,
        "success"
      );
      document.getElementById("last-sent").textContent = "Just now";
    } else {
      showToast(`<i class="ri-close-line"></i> ${data.message}`, "error");
    }
  } catch (error) {
    showToast("Failed to send notification", "error");
  }
}

async function sendNotificationToAll(title, body) {
  try {
    showToast("Sending notifications...", "info");

    const response = await fetch(`${API_BASE}/api/notifications/send-all`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, body }),
    });

    const data = await response.json();

    if (data.success || data.sent > 0) {
      showToast(
        `<i class="ri-check-line"></i> Sent to ${data.sent} users, ${data.failed} failed`,
        "success"
      );
      document.getElementById("last-sent").textContent = "Just now";
    } else {
      showToast(
        `<i class="ri-close-line"></i> Failed: ${
          data.results?.[0]?.message || "Unknown error"
        }`,
        "error"
      );
    }
  } catch (error) {
    showToast("Failed to send notifications", "error");
  }
}

async function sendNotificationToUser(userId, title, body) {
  try {
    showToast(`Sending to ${userId}...`, "info");

    const response = await fetch(
      `${API_BASE}/api/notifications/send-to-user/${userId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, body }),
      }
    );

    const data = await response.json();

    if (data.success) {
      showToast(
        `<i class="ri-check-line"></i> Notification sent to ${userId}`,
        "success"
      );
      document.getElementById("last-sent").textContent = "Just now";
    } else {
      showToast(`<i class="ri-close-line"></i> ${data.message}`, "error");
    }
  } catch (error) {
    showToast("Failed to send notification", "error");
  }
}

async function sendToUser(userId) {
  const title = prompt("Notification title:", "Hello!");
  if (!title) return;

  const body = prompt("Notification message:", "You have a new message!");
  if (!body) return;

  await sendNotificationToUser(userId, title, body);
}

// Template functions
function sendTemplate(button) {
  const card = button.closest(".template-card");
  const title = card.dataset.title;
  const body = card.dataset.body;

  // Send immediately to all users
  sendNotificationToAll(title, body);
}

function editTemplate(button) {
  const card = button.closest(".template-card");
  const title = card.dataset.title;
  const body = card.dataset.body;

  // Fill the form with template data
  document.getElementById("title").value = title;
  document.getElementById("body").value = body;

  // Update preview
  document.getElementById("preview-title").textContent = title;
  document.getElementById("preview-body").textContent = body;

  // Scroll to form
  document.querySelector(".custom-form-section").scrollIntoView({
    behavior: "smooth",
    block: "start",
  });

  showToast("Template loaded - customize and send!", "info");
}

// Utility functions
function refreshData() {
  checkServerStatus();
  loadUsers();
  showToast("Data refreshed", "success");
}

function formatDate(dateString) {
  if (!dateString) return "Unknown";

  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function showToast(message, type = "info") {
  const toast = document.getElementById("toast");
  // Changed to innerHTML to support icons
  toast.innerHTML = message;
  toast.className = `toast show ${type}`;

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}
