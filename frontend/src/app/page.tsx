import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <div className="text-center space-y-6 px-4">
        <h1 className="text-5xl font-bold tracking-tight">
          Setup<span className="text-primary-400">FX</span>
        </h1>
        <p className="text-xl text-gray-300 max-w-md mx-auto">
          Secure USDT Investment &amp; Wallet Platform
        </p>
        <div className="flex gap-4 justify-center pt-4">
          <Link
            href="/login"
            className="px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="px-6 py-3 border border-gray-500 hover:border-white rounded-lg font-semibold transition"
          >
            Register
          </Link>
        </div>
      </div>
    </main>
  );
}
