// tasks.js - Frontend API service for task operations

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Helper function to make authenticated requests with cookies
const makeRequest = async (url, options = {}) => {
  const response = await fetch(url, {
    ...options,
    credentials: "include", // Include cookies in the request
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "An error occurred");
  }

  return response.json();
};

// Task operations
export const getTasks = async (status = "all") => {
  const url = `${API_BASE_URL}/api/v1/tasks?status=${status}`;
  return makeRequest(url);
};

export const createTask = async (taskData) => {
  const url = `${API_BASE_URL}/api/v1/tasks`;
  return makeRequest(url, {
    method: "POST",
    body: JSON.stringify(taskData),
  });
};

export const updateTask = async (taskId, taskData) => {
  const url = `${API_BASE_URL}/api/v1/tasks/${taskId}`;
  return makeRequest(url, {
    method: "PATCH",
    body: JSON.stringify(taskData),
  });
};

export const toggleTaskCompletion = async (taskId) => {
  const url = `${API_BASE_URL}/api/v1/tasks/${taskId}/toggle`;
  return makeRequest(url, {
    method: "POST",
  });
};

export const deleteTask = async (taskId) => {
  const url = `${API_BASE_URL}/api/v1/tasks/${taskId}`;
  return makeRequest(url, {
    method: "DELETE",
  });
};
