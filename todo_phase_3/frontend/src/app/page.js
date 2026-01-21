"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getCurrentUser } from "../services/auth";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const checkAuthAndRedirect = async () => {
      try {
        // Try to get current user to check if authenticated
        const {current_user} = await getCurrentUser();
        if (current_user) {
          // If user is authenticated, redirect to tasks page
          router.push("/tasks");
        } else {
          // If not authenticated, redirect to login page
          router.push("/login");
        }
      } catch (error) {
        // If there's an error (e.g., no valid session), redirect to login
        router.push("/login");
      }
    };

    checkAuthAndRedirect();
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p>Redirecting...</p>
    </div>
  );
}
