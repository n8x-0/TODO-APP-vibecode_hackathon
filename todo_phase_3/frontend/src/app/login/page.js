"use client";
import LoginForm from "../../components/LoginForm";
import { login } from "../../services/auth";

export default function LoginPage() {
  const handleLogin = async (email, password) => {
    try {
      await login(email, password);
      // Redirect happens in the LoginForm component
    } catch (error) {
      throw error; // Let the LoginForm handle the error
    }
  };

  return <LoginForm onLogin={handleLogin} />;
}
