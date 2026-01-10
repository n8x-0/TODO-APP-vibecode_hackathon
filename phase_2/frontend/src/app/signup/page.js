"use client";
import SignupForm from "../../components/SignupForm";
import { signup } from "../../services/auth";

export default function SignupPage() {
  const handleSignup = async (userData) => {
    try {
      await signup(userData.email, userData.password);
      // Redirect happens in the SignupForm component
    } catch (error) {
      throw error; // Let the SignupForm handle the error
    }
  };

  return <SignupForm onSignup={handleSignup} />;
}
