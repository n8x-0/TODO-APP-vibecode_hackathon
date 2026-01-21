import React, { useState } from "react";
import TaskItem from "./TaskItem";
import TaskForm from "./TaskForm";
import Modal from "./Modal";

export default function TaskList({ tasks, onToggle, onUpdate, onDelete, onCreate, filter, onFilterChange, loading }) {
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [operationLoading, setOperationLoading] = useState(false);
  const [operationError, setOperationError] = useState("");

  const handleTaskCreated = async (taskData) => {
    try {
      setOperationLoading(true);
      setOperationError("");
      // Call the onCreate function passed from parent to save to DB
      // The parent component will handle updating the tasks list
      await onCreate(taskData);
      setShowForm(false);
      setEditingTask(null);
    } catch (err) {
      setOperationError(err.message || "Failed to create task");
    } finally {
      setOperationLoading(false);
    }
  };

  const handleTaskUpdated = async (taskId, taskData) => {
    try {
      setOperationLoading(true);
      setOperationError("");
      // Call the onUpdate function passed from parent
      const updatedTask = await onUpdate(taskId, taskData);
      setShowForm(false);
      setEditingTask(null);
      return updatedTask;
    } catch (err) {
      setOperationError(err.message || "Failed to update task");
    } finally {
      setOperationLoading(false);
    }
  };

  const handleTaskDeleted = async (deletedTaskId) => {
    try {
      setOperationLoading(true);
      setOperationError("");
      // Call the onDelete function passed from parent
      await onDelete(deletedTaskId);
    } catch (err) {
      setOperationError(err.message || "Failed to delete task");
    } finally {
      setOperationLoading(false);
    }
  };

  // Tasks are already filtered in the parent component
  // Using the tasks prop directly

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
          <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className={`w-full sm:w-auto px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
              showForm
                ? "bg-gray-500 hover:bg-gray-600 text-white"
                : "bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white shadow-md hover:shadow-lg"
            }`}
          >
            {showForm ? "Cancel" : "Add New Task"}
          </button>
        </div>

        <Modal
          isOpen={showForm}
          onClose={() => {
            setShowForm(false);
            setEditingTask(null);
          }}
          title={editingTask ? "Edit Task" : "Create New Task"}
        >
          <TaskForm
            task={editingTask}
            onSubmit={editingTask ? handleTaskUpdated : handleTaskCreated}
            onCancel={() => {
              setShowForm(false);
              setEditingTask(null);
            }}
          />
        </Modal>

        {operationError && (
          <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {operationError}
            </div>
          </div>
        )}

        <div className="mb-6">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onFilterChange("all")}
              className={`px-5 py-2.5 rounded-lg font-medium transition-all ${
                filter === "all"
                  ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-md"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              All Tasks
            </button>
            <button
              onClick={() => onFilterChange("completed")}
              className={`px-5 py-2.5 rounded-lg font-medium transition-all ${
                filter === "completed"
                  ? "bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-md"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Completed
            </button>
            <button
              onClick={() => onFilterChange("incomplete")}
              className={`px-5 py-2.5 rounded-lg font-medium transition-all ${
                filter === "incomplete"
                  ? "bg-gradient-to-r from-amber-500 to-orange-600 text-white shadow-md"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Incomplete
            </button>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.length === 0 ? (
            <div className="bg-white rounded-xl shadow-lg p-12 text-center">
              <div className="mx-auto w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mb-6">
                <svg className="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {filter === "all"
                  ? "No tasks yet"
                  : filter === "completed"
                    ? "No completed tasks yet"
                    : "No incomplete tasks yet"}
              </h3>
              <p className="text-gray-600 mb-6">
                {filter === "all"
                  ? "Add your first task to get started!"
                  : "Complete some tasks to see them here."}
              </p>
              <button
                onClick={() => setShowForm(true)}
                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-medium rounded-lg shadow-md hover:shadow-lg transition-all"
              >
                Add New Task
              </button>
            </div>
          ) : (
            tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={onToggle}
                onUpdate={onUpdate}
                onDelete={onDelete}
                onEdit={(taskToEdit) => {
                  setEditingTask(taskToEdit);
                  setShowForm(true);
                }}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
}
