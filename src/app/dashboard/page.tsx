"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskEditForm } from "@/components/tasks/TaskEditForm";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { api } from "@/lib/api";
import { getAuthUser, signOut } from "@/lib/auth";

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");
  const [isCreating, setIsCreating] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [showChat, setShowChat] = useState(false);

  // Get authenticated user
  const user = getAuthUser();

  useEffect(() => {
    // Redirect to signin if not authenticated
    if (!user) {
      router.push("/signin");
      return;
    }

    // Load tasks
    loadTasks();
  }, [user, router]);

  const loadTasks = async () => {
    if (!user) return;

    setIsLoading(true);
    setError("");

    try {
      const fetchedTasks = await api.tasks.list(user.id, user.token);
      setTasks(fetchedTasks);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to load tasks";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTask = async (title: string, description?: string) => {
    if (!user) return;

    setIsCreating(true);
    setError("");

    try {
      const newTask = await api.tasks.create(user.id, user.token, title, description);
      setTasks([newTask, ...tasks]); // Add to beginning of list
      setShowCreateModal(false);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to create task";
      setError(errorMessage);
      throw error; // Re-throw so TaskForm can handle it
    } finally {
      setIsCreating(false);
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    if (!user) return;

    try {
      const updatedTask = await api.tasks.toggleComplete(user.id, taskId, user.token, completed);
      setTasks(tasks.map((task) => (task.id === taskId ? updatedTask : task)));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to update task";
      setError(errorMessage);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowEditModal(true);
  };

  const handleUpdateTask = async (taskId: string, title: string, description?: string) => {
    if (!user) return;

    setIsUpdating(true);
    setError("");

    try {
      const updatedTask = await api.tasks.update(user.id, taskId, user.token, {
        title,
        description,
      });
      setTasks(tasks.map((task) => (task.id === taskId ? updatedTask : task)));
      setShowEditModal(false);
      setEditingTask(null);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to update task";
      setError(errorMessage);
      throw error; // Re-throw so TaskEditForm can handle it
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user) return;

    try {
      await api.tasks.delete(user.id, taskId, user.token);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to delete task";
      setError(errorMessage);
    }
  };

  const handleSignOut = async () => {
    await signOut();
  };

  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
              <p className="text-sm text-gray-600">{user.email}</p>
            </div>
            <div className="flex gap-2">
              <Button
                variant={showChat ? "primary" : "secondary"}
                size="sm"
                onClick={() => setShowChat(!showChat)}
              >
                {showChat ? "Hide Chat" : "AI Assistant"}
              </Button>
              <Button variant="secondary" size="sm" onClick={handleSignOut}>
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Task list section */}
          <div className={showChat ? "lg:col-span-2" : "lg:col-span-3"}>
            {/* Error message */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
                <button
                  onClick={() => setError("")}
                  className="ml-2 text-red-900 hover:text-red-700 font-medium"
                >
                  Dismiss
                </button>
              </div>
            )}

            {/* Actions bar */}
            <div className="mb-6 flex items-center justify-between">
              <div className="flex gap-2">
                <Button
                  variant={filter === "all" ? "primary" : "secondary"}
                  size="sm"
                  onClick={() => setFilter("all")}
                >
                  All
                </Button>
                <Button
                  variant={filter === "active" ? "primary" : "secondary"}
                  size="sm"
                  onClick={() => setFilter("active")}
                >
                  Active
                </Button>
                <Button
                  variant={filter === "completed" ? "primary" : "secondary"}
                  size="sm"
                  onClick={() => setFilter("completed")}
                >
                  Completed
                </Button>
              </div>

              <Button
                variant="primary"
                size="md"
                onClick={() => setShowCreateModal(true)}
              >
                + New Task
              </Button>
            </div>

            {/* Task list */}
            <TaskList
              tasks={tasks}
              onToggleComplete={handleToggleComplete}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
              isLoading={isLoading}
              filter={filter}
            />
          </div>

          {/* Chat interface section */}
          {showChat && (
            <div className="lg:col-span-1">
              <div className="sticky top-8 h-[calc(100vh-8rem)]">
                <ChatInterface token={user.token} />
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Create task modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Task"
      >
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateModal(false)}
          isLoading={isCreating}
        />
      </Modal>

      {/* Edit task modal */}
      {editingTask && (
        <Modal
          isOpen={showEditModal}
          onClose={() => {
            setShowEditModal(false);
            setEditingTask(null);
          }}
          title="Edit Task"
        >
          <TaskEditForm
            task={editingTask}
            onSubmit={handleUpdateTask}
            onCancel={() => {
              setShowEditModal(false);
              setEditingTask(null);
            }}
            isLoading={isUpdating}
          />
        </Modal>
      )}
    </div>
  );
}
