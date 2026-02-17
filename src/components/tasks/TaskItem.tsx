"use client";

import React from "react";
import { Button } from "@/components/ui/Button";

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: string, completed: boolean) => Promise<void>;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => Promise<void>;
  isLoading?: boolean;
}

export function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
  isLoading = false,
}: TaskItemProps) {
  const handleToggle = async () => {
    await onToggleComplete(task.id, !task.completed);
  };

  const handleDelete = async () => {
    if (onDelete && confirm("Are you sure you want to delete this task?")) {
      await onDelete(task.id);
    }
  };

  return (
    <div
      className={`border rounded-lg p-4 transition-all ${
        task.completed ? "bg-gray-50 border-gray-200" : "bg-white border-gray-300"
      } ${isLoading ? "opacity-50 pointer-events-none" : ""}`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          disabled={isLoading}
          className="mt-1 flex-shrink-0 w-5 h-5 rounded border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed"
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.completed && (
            <svg
              className="w-full h-full text-blue-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </button>

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-base font-medium ${
              task.completed ? "line-through text-gray-500" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}

          <p className="mt-2 text-xs text-gray-400">
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-2 flex-shrink-0">
          {onEdit && (
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onEdit(task)}
              disabled={isLoading}
              aria-label="Edit task"
            >
              Edit
            </Button>
          )}

          {onDelete && (
            <Button
              variant="danger"
              size="sm"
              onClick={handleDelete}
              disabled={isLoading}
              aria-label="Delete task"
            >
              Delete
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
