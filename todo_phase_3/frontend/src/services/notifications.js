// notifications.js - Service for handling browser notifications

// Request notification permission from the user
export const requestNotificationPermission = async () => {
  if ('Notification' in window) {
    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }
  return false;
};

// Check if notification permission is granted
export const isNotificationPermissionGranted = () => {
  return Notification.permission === 'granted';
};

// Show a task reminder notification
export const showTaskReminder = (task) => {
  if (isNotificationPermissionGranted()) {
    const notification = new Notification(`Task Reminder: ${task.title}`, {
      body: task.description || `Task "${task.title}" is due now!`,
      icon: '/favicon.ico', // Use the app's favicon
      tag: `task-${task.id}`, // Unique tag to prevent duplicate notifications
      requireInteraction: false, // Auto-dismiss after a few seconds
    });

    // Optional: Add click handler to redirect to the task
    notification.onclick = () => {
      window.focus();
      // Optionally redirect to the task page
      // window.open(`/tasks/${task.id}`, '_self');
    };

    return notification;
  }
  return null;
};

// Check for due tasks and show notifications
export const checkForDueTasks = async (getTasksFn) => {
  if (!isNotificationPermissionGranted()) {
    return [];
  }

  try {
    // Fetch all tasks (or tasks with due dates)
    const tasks = await getTasksFn("all");

    const now = new Date();
    // Add a small buffer (5 minutes) to show notifications for tasks that are due soon
    const bufferTime = 5 * 60 * 1000; // 5 minutes in milliseconds
    const dueTasks = tasks.filter(task => {
      if (!task.due_at || task.completed) {
        return false; // Skip tasks without due date or already completed
      }

      const dueDate = new Date(task.due_at);
      // Check if the task is due now or was due in the last 5 minutes
      // This helps catch tasks that were due while the user was away
      return dueDate <= new Date(now.getTime() + bufferTime);
    });

    // Show notifications for due tasks
    dueTasks.forEach(task => {
      showTaskReminder(task);
    });

    return dueTasks;
  } catch (error) {
    console.error('Error checking for due tasks:', error);
    throw error;
  }
};