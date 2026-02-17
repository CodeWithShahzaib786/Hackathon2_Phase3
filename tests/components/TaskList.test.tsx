import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { TaskList } from "@/components/tasks/TaskList";

const mockTasks = [
  {
    id: "1",
    title: "Task 1",
    description: "Description 1",
    completed: false,
    created_at: "2024-01-01T12:00:00Z",
    updated_at: "2024-01-01T12:00:00Z",
  },
  {
    id: "2",
    title: "Task 2",
    description: "Description 2",
    completed: true,
    created_at: "2024-01-02T12:00:00Z",
    updated_at: "2024-01-02T12:00:00Z",
  },
  {
    id: "3",
    title: "Task 3",
    completed: false,
    created_at: "2024-01-03T12:00:00Z",
    updated_at: "2024-01-03T12:00:00Z",
  },
];

describe("TaskList", () => {
  const mockOnToggleComplete = jest.fn();
  const mockOnEdit = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders all tasks when filter is 'all'", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        filter="all"
      />
    );

    expect(screen.getByText("Task 1")).toBeInTheDocument();
    expect(screen.getByText("Task 2")).toBeInTheDocument();
    expect(screen.getByText("Task 3")).toBeInTheDocument();
    expect(screen.getByText("3 tasks")).toBeInTheDocument();
  });

  it("renders only active tasks when filter is 'active'", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        filter="active"
      />
    );

    expect(screen.getByText("Task 1")).toBeInTheDocument();
    expect(screen.getByText("Task 3")).toBeInTheDocument();
    expect(screen.queryByText("Task 2")).not.toBeInTheDocument();
    expect(screen.getByText("2 tasks (active)")).toBeInTheDocument();
  });

  it("renders only completed tasks when filter is 'completed'", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        filter="completed"
      />
    );

    expect(screen.getByText("Task 2")).toBeInTheDocument();
    expect(screen.queryByText("Task 1")).not.toBeInTheDocument();
    expect(screen.queryByText("Task 3")).not.toBeInTheDocument();
    expect(screen.getByText("1 task (completed)")).toBeInTheDocument();
  });

  it("displays empty state when no tasks exist", () => {
    render(
      <TaskList
        tasks={[]}
        onToggleComplete={mockOnToggleComplete}
        filter="all"
      />
    );

    expect(screen.getByText("No tasks yet")).toBeInTheDocument();
    expect(screen.getByText("Get started by creating a new task.")).toBeInTheDocument();
  });

  it("displays empty state for active tasks when none exist", () => {
    const completedTasks = [mockTasks[1]]; // Only completed task

    render(
      <TaskList
        tasks={completedTasks}
        onToggleComplete={mockOnToggleComplete}
        filter="active"
      />
    );

    expect(screen.getByText("No active tasks")).toBeInTheDocument();
    expect(screen.getByText("You don't have any active tasks.")).toBeInTheDocument();
  });

  it("displays empty state for completed tasks when none exist", () => {
    const activeTasks = [mockTasks[0], mockTasks[2]]; // Only active tasks

    render(
      <TaskList
        tasks={activeTasks}
        onToggleComplete={mockOnToggleComplete}
        filter="completed"
      />
    );

    expect(screen.getByText("No completed tasks")).toBeInTheDocument();
    expect(screen.getByText("You don't have any completed tasks.")).toBeInTheDocument();
  });

  it("displays loading state", () => {
    render(
      <TaskList
        tasks={[]}
        onToggleComplete={mockOnToggleComplete}
        isLoading={true}
      />
    );

    expect(screen.getByText("Loading tasks...")).toBeInTheDocument();
  });

  it("calls onToggleComplete when checkbox is clicked", async () => {
    mockOnToggleComplete.mockResolvedValue(undefined);

    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    const checkboxes = screen.getAllByRole("button", { name: /mark as/i });
    fireEvent.click(checkboxes[0]); // Click first task's checkbox

    await waitFor(() => {
      expect(mockOnToggleComplete).toHaveBeenCalledWith("1", true);
    });
  });

  it("calls onDelete when delete button is clicked", async () => {
    mockOnDelete.mockResolvedValue(undefined);
    window.confirm = jest.fn(() => true); // Mock confirm dialog

    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const deleteButtons = screen.getAllByRole("button", { name: /delete/i });
    fireEvent.click(deleteButtons[0]); // Click first task's delete button

    await waitFor(() => {
      expect(mockOnDelete).toHaveBeenCalledWith("1");
    });
  });

  it("calls onEdit when edit button is clicked", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onEdit={mockOnEdit}
      />
    );

    const editButtons = screen.getAllByRole("button", { name: /edit/i });
    fireEvent.click(editButtons[0]); // Click first task's edit button

    expect(mockOnEdit).toHaveBeenCalledWith(mockTasks[0]);
  });

  it("does not show edit/delete buttons when handlers not provided", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    expect(screen.queryByRole("button", { name: /edit/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /delete/i })).not.toBeInTheDocument();
  });

  it("disables interactions when isLoading is true", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
        isLoading={true}
      />
    );

    const checkboxes = screen.getAllByRole("button", { name: /mark as/i });
    const deleteButtons = screen.getAllByRole("button", { name: /delete/i });

    expect(checkboxes[0]).toBeDisabled();
    expect(deleteButtons[0]).toBeDisabled();
  });

  it("renders task descriptions when provided", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    expect(screen.getByText("Description 1")).toBeInTheDocument();
    expect(screen.getByText("Description 2")).toBeInTheDocument();
  });

  it("renders tasks without descriptions", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    // Task 3 has no description
    expect(screen.getByText("Task 3")).toBeInTheDocument();
    expect(screen.queryByText("Description 3")).not.toBeInTheDocument();
  });

  it("displays correct task count with singular form", () => {
    const singleTask = [mockTasks[0]];

    render(
      <TaskList
        tasks={singleTask}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    expect(screen.getByText("1 task")).toBeInTheDocument();
  });

  it("displays correct task count with plural form", () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    expect(screen.getByText("3 tasks")).toBeInTheDocument();
  });
});
