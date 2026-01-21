// UI tests for frontend components

import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import LoginForm from "../components/LoginForm";
import SignupForm from "../components/SignupForm";
import TaskList from "../components/TaskList";
import TaskForm from "../components/TaskForm";
import TaskItem from "../components/TaskItem";

describe("LoginForm Component", () => {
  test("renders login form with email and password fields", () => {
    render(<LoginForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  });

  test("validates required fields", async () => {
    render(<LoginForm />);

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
  });
});

describe("SignupForm Component", () => {
  test("renders signup form with email and password fields", () => {
    render(<SignupForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /sign up/i }),
    ).toBeInTheDocument();
  });

  test("validates required fields", async () => {
    render(<SignupForm />);

    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
  });
});

describe("TaskList Component", () => {
  test("renders task list with empty state", () => {
    render(<TaskList tasks={[]} />);

    expect(screen.getByText(/no tasks found/i)).toBeInTheDocument();
  });

  test("renders tasks when provided", () => {
    const tasks = [
      {
        id: 1,
        title: "Test Task",
        completed: false,
        created_at: new Date().toISOString(),
      },
    ];

    render(<TaskList tasks={tasks} />);

    expect(screen.getByText(/test task/i)).toBeInTheDocument();
  });
});

describe("TaskForm Component", () => {
  test("renders task form with title field", () => {
    render(<TaskForm />);

    expect(screen.getByLabelText(/task title/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /add task/i }),
    ).toBeInTheDocument();
  });

  test("validates required fields", async () => {
    render(<TaskForm />);

    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(screen.getByText(/task title is required/i)).toBeInTheDocument();
    });
  });
});

describe("TaskItem Component", () => {
  test("renders task item with title", () => {
    const task = {
      id: 1,
      title: "Test Task",
      completed: false,
      created_at: new Date().toISOString(),
    };

    render(<TaskItem task={task} />);

    expect(screen.getByText(/test task/i)).toBeInTheDocument();
  });

  test("shows completed status", () => {
    const task = {
      id: 1,
      title: "Test Task",
      completed: true,
      created_at: new Date().toISOString(),
    };

    render(<TaskItem task={task} />);

    const checkbox = screen.getByRole("checkbox");
    expect(checkbox).toBeChecked();
  });
});
