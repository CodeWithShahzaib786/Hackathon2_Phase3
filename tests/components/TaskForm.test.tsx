import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { TaskForm } from "@/components/tasks/TaskForm";

describe("TaskForm", () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders form with all fields", () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/task title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /add task/i })).toBeInTheDocument();
  });

  it("shows cancel button when onCancel is provided", () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    expect(screen.getByRole("button", { name: /cancel/i })).toBeInTheDocument();
  });

  it("does not show cancel button when onCancel is not provided", () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.queryByRole("button", { name: /cancel/i })).not.toBeInTheDocument();
  });

  it("validates required title field", async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole("button", { name: /add task/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("validates title max length", async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const longTitle = "x".repeat(201); // Exceeds max length of 200

    fireEvent.change(titleInput, { target: { value: longTitle } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(screen.getByText(/title cannot exceed 200 characters/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("calls onSubmit with title only when description is empty", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("Test Task", undefined);
    });
  });

  it("calls onSubmit with title and description", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.change(descriptionInput, { target: { value: "Test Description" } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("Test Task", "Test Description");
    });
  });

  it("trims whitespace from title and description", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "  Test Task  " } });
    fireEvent.change(descriptionInput, { target: { value: "  Test Description  " } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("Test Task", "Test Description");
    });
  });

  it("treats whitespace-only description as undefined", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.change(descriptionInput, { target: { value: "   " } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith("Test Task", undefined);
    });
  });

  it("resets form after successful submission", async () => {
    mockOnSubmit.mockResolvedValue(undefined);

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i) as HTMLInputElement;
    const descriptionInput = screen.getByLabelText(/description/i) as HTMLTextAreaElement;

    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.change(descriptionInput, { target: { value: "Test Description" } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(titleInput.value).toBe("");
      expect(descriptionInput.value).toBe("");
    });
  });

  it("displays error message on submission failure", async () => {
    mockOnSubmit.mockRejectedValue(new Error("Failed to create task"));

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(screen.getByText(/failed to create task/i)).toBeInTheDocument();
    });
  });

  it("handles non-Error exceptions", async () => {
    mockOnSubmit.mockRejectedValue("String error");

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.click(screen.getByRole("button", { name: /add task/i }));

    await waitFor(() => {
      expect(screen.getByText(/failed to create task/i)).toBeInTheDocument();
    });
  });

  it("disables form during submission", async () => {
    mockOnSubmit.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const submitButton = screen.getByRole("button", { name: /add task/i });

    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.click(submitButton);

    expect(titleInput).toBeDisabled();
    expect(descriptionInput).toBeDisabled();
    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/creating/i)).toBeInTheDocument();
  });

  it("calls onCancel when cancel button is clicked", () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const cancelButton = screen.getByRole("button", { name: /cancel/i });
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it("disables cancel button during submission", async () => {
    mockOnSubmit.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const submitButton = screen.getByRole("button", { name: /add task/i });
    const cancelButton = screen.getByRole("button", { name: /cancel/i });

    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.click(submitButton);

    expect(cancelButton).toBeDisabled();
  });

  it("shows character count for description", () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const descriptionInput = screen.getByLabelText(/description/i);

    // Initial count
    expect(screen.getByText("0/1000 characters")).toBeInTheDocument();

    // After typing
    fireEvent.change(descriptionInput, { target: { value: "Test" } });
    expect(screen.getByText("4/1000 characters")).toBeInTheDocument();
  });

  it("enforces max length on title input", () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i) as HTMLInputElement;

    expect(titleInput.maxLength).toBe(200);
  });

  it("enforces max length on description textarea", () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const descriptionInput = screen.getByLabelText(/description/i) as HTMLTextAreaElement;

    expect(descriptionInput.maxLength).toBe(1000);
  });

  it("clears error message on new submission attempt", async () => {
    mockOnSubmit.mockRejectedValueOnce(new Error("First error"));

    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByLabelText(/task title/i);
    const submitButton = screen.getByRole("button", { name: /add task/i });

    // First submission - should fail
    fireEvent.change(titleInput, { target: { value: "Test Task" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/first error/i)).toBeInTheDocument();
    });

    // Second submission - error should be cleared
    mockOnSubmit.mockResolvedValue(undefined);
    fireEvent.change(titleInput, { target: { value: "Test Task 2" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.queryByText(/first error/i)).not.toBeInTheDocument();
    });
  });
});
