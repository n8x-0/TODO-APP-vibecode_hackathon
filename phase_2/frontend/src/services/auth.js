// Auth service for handling authentication operations

import { getCookie, setCookie, deleteCookie } from "../utils/cookies";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Function to handle user signup
export const signup = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
      credentials: "include", // Include cookies in the request
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Signup failed");
    }

    const data = await response.json();

    // Store the access token in a cookie
    if (data.access_token) {
      setCookie("access_token", data.access_token, {
        path: "/",
        httpOnly: true,
        secure: false, // Set to true in production with HTTPS
        sameSite: "lax", // Can be 'strict', 'lax', or 'none'
        maxAge: 604800, // 7 days in seconds for session persistence
      });
    }

    return data;
  } catch (error) {
    throw new Error(error.message || "An error occurred during signup");
  }
};

// Function to handle user login
export const login = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
      credentials: "include", // Include cookies in the request
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }

    const data = await response.json();

    // Store the access token in a cookie with longer expiration for session persistence
    if (data.access_token) {
      setCookie("access_token", data.access_token, {
        path: "/",
        httpOnly: true,
        secure: false, // Set to true in production with HTTPS
        sameSite: "lax", // Can be 'strict', 'lax', or 'none'
        maxAge: 604800, // 7 days in seconds for session persistence
      });
    }

    return data;
  } catch (error) {
    throw new Error(error.message || "An error occurred during login");
  }
};

// Function to handle user logout
export const logout = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
      method: "POST",
      credentials: "include", // Include cookies in the request
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Logout failed");
    }

    // Clear the access token cookie
    deleteCookie("access_token");

    return { message: "Successfully logged out" };
  } catch (error) {
    throw new Error(error.message || "An error occurred during logout");
  }
};

// Function to get current user information
export const getCurrentUser = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
      method: "GET",
      credentials: "include", // Include cookies in the request
    });

    if (!response.ok) {
      const errorData = await response.json();

      // Handle 401 Unauthorized - redirect to login
      if (response.status === 401) {
        // Redirect to login page
        window.location.href = "/login";
        return null;
      }

      throw new Error(errorData.detail || "Failed to get user information");
    }

    const data = await response.json();

    // Check if session is about to expire (within 5 minutes)
    if (data.session_expires_at) {
      const now = new Date();
      const expiresAt = new Date(data.session_expires_at);
      const timeUntilExpiration = expiresAt.getTime() - now.getTime();

      // If session expires in less than 5 minutes, refresh it
      if (timeUntilExpiration < 5 * 60 * 1000) {
        // 5 minutes in milliseconds
        // Refresh the session by making a request to the refresh endpoint
        // Note: This would require implementing a refresh endpoint in the backend
        // For now, we'll just log a warning
        console.warn(
          "Session is about to expire, consider implementing refresh mechanism",
        );
      }
    }

    return data;
  } catch (error) {
    throw new Error(
      error.message || "An error occurred while fetching user information",
    );
  }
};

// Function to get JWT token for API calls to FastAPI backend
export const getJwtToken = async () => {
  // Get the token from the cookie
  return getCookie("access_token");
};
