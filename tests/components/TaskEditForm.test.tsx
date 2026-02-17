import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { TaskEditForm } from "@/components/tasks/TaskEditForm";

const mockTask = {
  id: "1",
  title: "Original Task",
  description: "Original Description",
  completed: false,
};

describe("TaskEditForm", () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders form with task data pre-filled", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i) as HTMLInputElement;
    const descriptionInput = screen.getByLabelText(/description/i) as HTMLTextAreaElement;

    expect(titleInput.value).toBe("Original Task");
    expect(descriptionInput.value).toBe("Original Description");
    expect(screen.getByRole("button", { name: /save changes/i })).toBeInTheDocument();
  });

  it("renders form with empty description when task has no description", () => {
    const taskWithoutDescription = { ...mockTask, description: undefined };

    render(<TaskEditForm task={taskWithoutDescription} onSubmit={mockOnSubmit} />);

    const descriptionInput = screen.getByLabelText(/description/i) as HTMLTextAreaElement;
    expect(descriptionInput.value).toBe("");
  });

  it("shows cancel button when onCancel is provided", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    expect(screen.getByRole("button", { name: /cancel/i })).toBeInTheDocument();
  });

  it("does not show cancel button when onCancel is not provided", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    expect(screen.queryByRole("button", { name: /cancel/i })).not.toBeInTheDocument();
  });

  it("validates required title field", async () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: "" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("validates title max length", async () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const longTitle = "x".repeat(201);

    fireEvent.change(titleInput, { target: { value: longTitle } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(screen.getByText(/title cannot exceed 200 characters/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("calls onSubmit with updated title and description", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.change(descriptionInput, { target: { value: "Updated Description" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("1", "Updated Task", "Updated Description");
    });
  });

  it("calls onSubmit with only title when description is empty", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.change(descriptionInput, { target: { value: "" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("1", "Updated Task", undefined);
    });
  });

  it("trims whitespace from title and description", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "  Updated Task  " } });
    fireEvent.change(descriptionInput, { target: { value: "  Updated Description  " } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("1", "Updated Task", "Updated Description");
    });
  });

  it("treats whitespace-only description as undefined", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.change(descriptionInput, { target: { value: "   " } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("1", "Updated Task", undefined);
    });
  });

  it("displays error message on submission failure", async () => {
    mockOnSubmit.mockRejectedValue(new Error("Failed to update task"));

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(screen.getByText(/failed to update task/i)).toBeInTheDocument();
    });
  });

  it("handles non-Error exceptions", async () => {
    mockOnSubmit.mockRejectedValue("String error");

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(screen.getByText(/failed to update task/i)).toBeInTheDocument();
    });
  });

  it("disables form during submission", async () => {
    mockOnSubmit.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const submitButton = screen.getByRole("button", { name: /save changes/i });

    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.click(submitButton);

    expect(titleInput).toBeDisabled();
    expect(descriptionInput).toBeDisabled();
    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/saving/i)).toBeInTheDocument();
  });

  it("calls onCancel when cancel button is clicked", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const cancelButton = screen.getByRole("button", { name: /cancel/i });
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it("disables cancel button during submission", async () => {
    mockOnSubmit.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const submitButton = screen.getByRole("button", { name: /save changes/i });
    const cancelButton = screen.getByRole("button", { name: /cancel/i });

    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.click(submitButton);

    expect(cancelButton).toBeDisabled();
  });

  it("shows character count for description", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    // Initial count (from pre-filled description)
    expect(screen.getByText("20/1000 characters")).toBeInTheDocument();

    const descriptionInput = screen.getByLabelText(/description/i);

    // After changing
    fireEvent.change(descriptionInput, { target: { value: "Test" } });
    expect(screen.getByText("4/1000 characters")).toBeInTheDocument();
  });

  it("enforces max length on title input", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i) as HTMLInputElement;
    expect(titleInput.maxLength).toBe(200);
  });

  it("enforces max length on description textarea", () => {
    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const descriptionInput = screen.getByLabelText(/description/i) as HTMLTextAreaElement;
    expect(descriptionInput.maxLength).toBe(1000);
  });

  it("clears error message on new submission attempt", async () => {
    mockOnSubmit.mockRejectedValueOnce(new Error("First error"));

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const submitButton = screen.getByRole("button", { name: /save changes/i });

    // First submission - should fail
    fireEvent.change(titleInput, { target: { value: "Updated Task" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/first error/i)).toBeInTheDocument();
    });

    // Second submission - error should be cleared
    mockOnSubmit.mockResolvedValue(undefined);
    fireEvent.change(titleInput, { target: { value: "Updated Task 2" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.queryByText(/first error/i)).not.toBeInTheDocument();
    });
  });

  it("allows editing without changing the title", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const descriptionInput = screen.getByLabelText(/description/i);

    // Only change description, keep original title
    fireEvent.change(descriptionInput, { target: { value: "New Description" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("1", "Original Task", "New Description");
    });
  });

  it("allows editing without changing the description", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskEditForm task={mockTask} onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);

    // Only change title, keep original description
    fireEvent.change(titleInput, { target: { value: "New Title" } });
    fireEvent.click(screen.getByRole("button", { name: /save changes/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("1", "New Title", "Original Description");
    });
  });
});
