"use client";

import React from "react";
import { TaskItem } from "./TaskItem";

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (taskId: string, completed: boolean) => Promise<void>;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => Promise<void>;
  isLoading?: boolean;
  filter?: "all" | "active" | "completed";
}

export function TaskList({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
  isLoading = false,
  filter = "all",
}: TaskListProps) {
  // Filter tasks based on filter prop
  const filteredTasks = tasks.filter((task) => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true; // "all"
  });

  // Empty state
  if (filteredTasks.length === 0 && !isLoading) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          {filter === "active" && "No active tasks"}
          {filter === "completed" && "No completed tasks"}
          {filter === "all" && "No tasks yet"}
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          {filter === "all"
            ? "Get started by creating a new task."
            : `You don't have any ${filter} tasks.`}
        </p>
      </div>
    );
  }

  // Loading state
  if (isLoading && filteredTasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-sm text-gray-500">Loading tasks...</p>
      </div>
    );
  }

  // Task list
  return (
    <div className="space-y-3">
      {/* Task count */}
      <div className="text-sm text-gray-600">
        {filteredTasks.length} {filteredTasks.length === 1 ? "task" : "tasks"}
        {filter !== "all" && ` (${filter})`}
      </div>

      {/* Tasks */}
      {filteredTasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onEdit={onEdit}
          onDelete={onDelete}
          isLoading={isLoading}
        />
      ))}
    </div>
  );
}
