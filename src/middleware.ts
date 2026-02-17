import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Middleware to protect routes that require authentication
 */
export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;
  const { pathname } = request.nextUrl;

  // Public routes that don't require authentication
  const publicRoutes = ["/", "/signin", "/signup"];
  const isPublicRoute = publicRoutes.includes(pathname);

  // If trying to access protected route without token, redirect to signin
  if (!isPublicRoute && !token) {
    const signinUrl = new URL("/signin", request.url);
    signinUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(signinUrl);
  }

  // If authenticated user tries to access auth pages, redirect to dashboard
  if (token && (pathname === "/signin" || pathname === "/signup")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

/**
 * Configure which routes this middleware should run on
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
