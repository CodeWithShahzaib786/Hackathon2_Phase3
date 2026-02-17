"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
}

interface TaskEditFormProps {
  task: Task;
  onSubmit: (taskId: string, title: string, description?: string) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
}

export function TaskEditForm({ task, onSubmit, onCancel, isLoading = false }: TaskEditFormProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    if (title.length > 200) {
      setError("Title cannot exceed 200 characters");
      return;
    }

    setError("");

    try {
      await onSubmit(task.id, title.trim(), description.trim() || undefined);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to update task";
      setError(errorMessage);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      <Input
        label="Task Title"
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="What needs to be done?"
        disabled={isLoading}
        required
        maxLength={200}
      />

      <div className="space-y-2">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details..."
          disabled={isLoading}
          maxLength={1000}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <p className="text-xs text-gray-500">
          {description.length}/1000 characters
        </p>
      </div>

      <div className="flex gap-2">
        <Button
          type="submit"
          variant="primary"
          size="md"
          disabled={isLoading}
          className="flex-1"
        >
          {isLoading ? "Saving..." : "Save Changes"}
        </Button>

        {onCancel && (
          <Button
            type="button"
            variant="secondary"
            size="md"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}
