"""Authentication state management for Next.js frontend."""

// Authentication utilities for managing user state and tokens

export interface AuthUser {
  id: string;
  email: string;
  token: string;
}

/**
 * Get the current authenticated user from localStorage
 */
export function getAuthUser(): AuthUser | null {
  if (typeof window === "undefined") {
    return null;
  }

  const token = localStorage.getItem("auth_token");
  const userId = localStorage.getItem("user_id");
  const userEmail = localStorage.getItem("user_email");

  if (!token || !userId || !userEmail) {
    return null;
  }

  return {
    id: userId,
    email: userEmail,
    token: token,
  };
}

/**
 * Save authenticated user to localStorage
 */
export function setAuthUser(user: AuthUser): void {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.setItem("auth_token", user.token);
  localStorage.setItem("user_id", user.id);
  localStorage.setItem("user_email", user.email);
}

/**
 * Clear authenticated user from localStorage
 */
export function clearAuthUser(): void {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.removeItem("auth_token");
  localStorage.removeItem("user_id");
  localStorage.removeItem("user_email");
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return getAuthUser() !== null;
}

/**
 * Get the authentication token
 */
export function getAuthToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem("auth_token");
}

/**
 * Sign out the current user
 */
export async function signOut(): Promise<void> {
  const token = getAuthToken();

  if (token) {
    try {
      // Call signout endpoint
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signout`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (error) {
      console.error("Signout error:", error);
    }
  }

  // Clear local storage regardless of API call result
  clearAuthUser();

  // Redirect to signin page
  if (typeof window !== "undefined") {
    window.location.href = "/signin";
  }
}

// Better Auth configuration placeholder
export const authConfig = {
  secret: process.env.BETTER_AUTH_SECRET || "",
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  providers: {
    // Email/password authentication configured via API
  },
};

