"use client";
import { useState, useEffect } from "react";
import TaskList from "../../components/TaskList";
import Header from "../../components/Header";
import {
  getTasks,
  createTask,
  updateTask,
  toggleTaskCompletion,
  deleteTask,
} from "../../services/tasks";
import { getCurrentUser } from "../../services/auth";
import {
  requestNotificationPermission,
  checkForDueTasks,
  isNotificationPermissionGranted
} from "../../services/notifications";

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("all");
  const [notificationPermission, setNotificationPermission] = useState(false);

  // Request notification permission and set up periodic checks
  useEffect(() => {
    const setupNotifications = async () => {
      // Request notification permission
      const permissionGranted = await requestNotificationPermission();
      setNotificationPermission(permissionGranted);

      if (permissionGranted) {
        // Check for due tasks immediately
        await checkForDueTasks(() => getTasks("all"));
      }
    };

    setupNotifications();
  }, []);

  // Set up periodic checking for due tasks
  useEffect(() => {
    if (!notificationPermission) return;

    // Check for due tasks every minute
    const intervalId = setInterval(async () => {
      try {
        await checkForDueTasks(() => getTasks("all"));
      } catch (err) {
        console.error('Error checking for due tasks:', err);
      }
    }, 60000); // 60 seconds

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, [notificationPermission]);

  // Fetch user and tasks when component mounts
  useEffect(() => {
    const loadUserData = async () => {
      try {
        // Fetch user information
        const userData = await getCurrentUser();
        setUser(userData);

        // Fetch all tasks
        const allTasks = await getTasks("all"); // Always fetch all tasks
        setTasks(allTasks);
      } catch (err) {
        setError(err.message || "Failed to load user data or tasks");
      } finally {
        setLoading(false);
      }
    };

    loadUserData();
  }, []);

  // Separate function to fetch all tasks (for refresh operations)
  const fetchAllTasks = async () => {
    try {
      const allTasks = await getTasks("all"); // Always fetch all tasks
      setTasks(allTasks);
    } catch (err) {
      setError(err.message || "Failed to load tasks");
    }
  };

  // Fetch tasks when needed (e.g., after create/update/delete)
  const fetchTasks = async () => {
    try {
      const allTasks = await getTasks("all"); // Always fetch all tasks
      setTasks(allTasks);
    } catch (err) {
      setError(err.message || "Failed to load tasks");
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      // We can't optimistically add the task since it doesn't have an ID yet
      const newTask = await createTask(taskData);
      if (newTask && newTask.id) {
        // Add the new task to the local state for immediate UI update
        setTasks(prevTasks => [...prevTasks, newTask]);
        return newTask; // Return the created task for the calling component
      } else {
        throw new Error("Task creation failed - invalid response from server");
      }
    } catch (err) {
      setError(err.message || "Failed to create task");
      throw err; // Re-throw the error so the calling component knows it failed
    }
  };

  const handleUpdateTask = async (taskId, taskData) => {
    try {
      // Optimistically update the UI
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, ...taskData } : task
        )
      );

      const updatedTask = await updateTask(taskId, taskData);
      // Update with the server response to ensure consistency
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );
      return updatedTask;
    } catch (err) {
      setError(err.message || "Failed to update task");
      // Revert the optimistic update if the API call fails
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, ...taskData } : task
        )
      );
      throw err;
    }
  };

  const handleToggleTask = async (taskId) => {
    try {
      // Optimistically update the UI
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      );

      const toggledTask = await toggleTaskCompletion(taskId);
      // Update with the server response to ensure consistency
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? toggledTask : task
        )
      );
    } catch (err) {
      setError(err.message || "Failed to toggle task");
      // Revert the optimistic update if the API call fails
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      );
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      // Optimistically update the UI
      setTasks(prevTasks =>
        prevTasks.filter(task => task.id !== taskId)
      );

      await deleteTask(taskId);
    } catch (err) {
      setError(err.message || "Failed to delete task");
      // Revert the optimistic update if the API call fails
      // We would need to restore the task, but since we don't have it anymore,
      // we'll just refetch all tasks
      fetchAllTasks();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto p-6 min-h-screen bg-gray-50">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <svg className="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900">Error loading tasks</h3>
            <p className="mt-2 text-gray-600">{error}</p>
            <div className="mt-6">
              <button
                onClick={() => window.location.reload()}
                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-medium rounded-lg shadow-md transition-all"
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Filter tasks based on current filter
  const filteredTasks =
    filter === "all"
      ? tasks
      : filter === "completed"
        ? tasks.filter(task => task.completed)
        : tasks.filter(task => !task.completed);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} />
      <div className="max-w-4xl mx-auto py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800">Task Manager</h1>
          <p className="text-gray-600 mt-2">Organize your work and boost your productivity</p>
          {!notificationPermission && (
            <div className="mt-4 p-3 bg-yellow-50 text-yellow-700 rounded-lg border border-yellow-200">
              <p>Enable browser notifications to receive task reminders!</p>
              <button
                onClick={async () => {
                  const permission = await requestNotificationPermission();
                  setNotificationPermission(permission);
                }}
                className="mt-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg"
              >
                Enable Notifications
              </button>
            </div>
          )}
        </div>
        <TaskList
          tasks={filteredTasks}
          allTasks={tasks} // Pass all tasks for reference
          onToggle={handleToggleTask}
          onUpdate={handleUpdateTask}
          onDelete={handleDeleteTask}
          onCreate={handleCreateTask}
          filter={filter}
          onFilterChange={setFilter}
          loading={loading}
        />
      </div>
    </div>
  );
}
