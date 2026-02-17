import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { SignUpForm } from "@/components/auth/SignUpForm";
import { api } from "@/lib/api";

// Mock the API
jest.mock("@/lib/api", () => ({
  api: {
    auth: {
      signup: jest.fn(),
    },
  },
}));

describe("SignUpForm", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders signup form with all fields", () => {
    render(<SignUpForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign up/i })).toBeInTheDocument();
  });

  it("validates email format", async () => {
    render(<SignUpForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });

    fireEvent.change(emailInput, { target: { value: "invalid-email" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
    });
  });

  it("validates password strength", async () => {
    render(<SignUpForm />);

    const passwordInput = screen.getByLabelText(/^password$/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });

    // Test password too short
    fireEvent.change(passwordInput, { target: { value: "short" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it("validates password confirmation match", async () => {
    render(<SignUpForm />);

    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmInput = screen.getByLabelText(/confirm password/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });

    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.change(confirmInput, { target: { value: "DifferentPass456" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/passwords do not match/i)).toBeInTheDocument();
    });
  });

  it("calls onSuccess callback on successful signup", async () => {
    const mockResponse = {
      id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      token: "mock-jwt-token",
    };

    (api.auth.signup as jest.Mock).mockResolvedValue(mockResponse);

    const onSuccess = jest.fn();
    render(<SignUpForm onSuccess={onSuccess} />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmInput = screen.getByLabelText(/confirm password/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.change(confirmInput, { target: { value: "SecurePass123" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(api.auth.signup).toHaveBeenCalledWith("test@example.com", "SecurePass123");
      expect(onSuccess).toHaveBeenCalledWith(mockResponse);
    });
  });

  it("displays error message on signup failure", async () => {
    (api.auth.signup as jest.Mock).mockRejectedValue(new Error("Email already registered"));

    const onError = jest.fn();
    render(<SignUpForm onError={onError} />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmInput = screen.getByLabelText(/confirm password/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });

    fireEvent.change(emailInput, { target: { value: "existing@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.change(confirmInput, { target: { value: "SecurePass123" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/email already registered/i)).toBeInTheDocument();
      expect(onError).toHaveBeenCalledWith("Email already registered");
    });
  });

  it("disables form during submission", async () => {
    (api.auth.signup as jest.Mock).mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<SignUpForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmInput = screen.getByLabelText(/confirm password/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "SecurePass123" } });
    fireEvent.change(confirmInput, { target: { value: "SecurePass123" } });
    fireEvent.click(submitButton);

    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/creating account/i)).toBeInTheDocument();
  });
});
