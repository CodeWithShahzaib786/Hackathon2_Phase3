import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { SignInForm } from "@/components/auth/SignInForm";
import { api } from "@/lib/api";

// Mock the API
jest.mock("@/lib/api", () => ({
  api: {
    auth: {
      signin: jest.fn(),
    },
  },
}));

describe("SignInForm", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders signin form with all fields", () => {
    render(<SignInForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign in/i })).toBeInTheDocument();
  });

  it("validates required fields", async () => {
    render(<SignInForm />);

    const submitButton = screen.getByRole("button", { name: /sign in/i });

    // Try to submit without filling any fields
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/email and password are required/i)).toBeInTheDocument();
    });
  });

  it("calls onSuccess callback on successful signin", async () => {
    const mockResponse = {
      id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      token: "mock-jwt-token",
    };

    (api.auth.signin as jest.Mock).mockResolvedValue(mockResponse);

    const onSuccess = jest.fn();
    render(<SignInForm onSuccess={onSuccess} />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(api.auth.signin).toHaveBeenCalledWith("test@example.com", "SecurePass123");
      expect(onSuccess).toHaveBeenCalledWith(mockResponse);
    });
  });

  it("displays error message on signin failure", async () => {
    (api.auth.signin as jest.Mock).mockRejectedValue(new Error("Invalid credentials"));

    const onError = jest.fn();
    render(<SignInForm onError={onError} />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: "wrong@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "WrongPassword" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
      expect(onError).toHaveBeenCalledWith("Invalid credentials");
    });
  });

  it("disables form during submission", async () => {
    (api.auth.signin as jest.Mock).mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<SignInForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.click(submitButton);

    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/signing in/i)).toBeInTheDocument();
  });

  it("handles non-Error exceptions", async () => {
    (api.auth.signin as jest.Mock).mockRejectedValue("String error");

    render(<SignInForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/sign in failed/i)).toBeInTheDocument();
    });
  });

  it("clears error message on new submission", async () => {
    (api.auth.signin as jest.Mock).mockRejectedValueOnce(new Error("Invalid credentials"));

    render(<SignInForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    // First submission - should fail
    fireEvent.change(emailInput, { target: { value: "wrong@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "WrongPassword" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });

    // Second submission - error should be cleared during submission
    (api.auth.signin as jest.Mock).mockResolvedValue({
      id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      token: "mock-jwt-token",
    });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "CorrectPassword" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.queryByText(/invalid credentials/i)).not.toBeInTheDocument();
    });
  });
});
