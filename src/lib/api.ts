"""API client for making authenticated requests to the backend."""

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions extends RequestInit {
  token?: string;
}

/**
 * Make an authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...fetchOptions.headers,
  };

  // Add JWT token to Authorization header if provided
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: "An error occurred",
    }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * API client methods
 */
export const api = {
  // Authentication endpoints
  auth: {
    signup: (email: string, password: string) =>
      apiRequest("/api/auth/signup", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),

    signin: (email: string, password: string) =>
      apiRequest("/api/auth/signin", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),

    signout: (token: string) =>
      apiRequest("/api/auth/signout", {
        method: "POST",
        token,
      }),
  },

  // Task endpoints
  tasks: {
    list: (userId: string, token: string, completed?: boolean) => {
      const query = completed !== undefined ? `?completed=${completed}` : "";
      return apiRequest(`/api/${userId}/tasks${query}`, { token });
    },

    create: (userId: string, token: string, title: string, description?: string) =>
      apiRequest(`/api/${userId}/tasks`, {
        method: "POST",
        token,
        body: JSON.stringify({ title, description }),
      }),

    get: (userId: string, taskId: string, token: string) =>
      apiRequest(`/api/${userId}/tasks/${taskId}`, { token }),

    update: (
      userId: string,
      taskId: string,
      token: string,
      data: { title?: string; description?: string; completed?: boolean }
    ) =>
      apiRequest(`/api/${userId}/tasks/${taskId}`, {
        method: "PUT",
        token,
        body: JSON.stringify(data),
      }),

    delete: (userId: string, taskId: string, token: string) =>
      apiRequest(`/api/${userId}/tasks/${taskId}`, {
        method: "DELETE",
        token,
      }),

    toggleComplete: (userId: string, taskId: string, token: string, completed: boolean) =>
      apiRequest(`/api/${userId}/tasks/${taskId}/complete?completed=${completed}`, {
        method: "PATCH",
        token,
      }),
  },
};
