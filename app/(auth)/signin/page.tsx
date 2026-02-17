import { SignInForm } from "@/components/auth/SignInForm";
import Link from "next/link";
import { redirect } from "next/navigation";

export default function SignInPage() {
  const handleSuccess = (data: { id: string; email: string; token: string }) => {
    // Store token in localStorage
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", data.token);
      localStorage.setItem("user_id", data.id);
      localStorage.setItem("user_email", data.email);
    }
    // Redirect to dashboard
    redirect("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Don't have an account?{" "}
            <Link
              href="/signup"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Sign up
            </Link>
          </p>
        </div>

        <SignInForm onSuccess={handleSuccess} />
      </div>
    </div>
  );
}
