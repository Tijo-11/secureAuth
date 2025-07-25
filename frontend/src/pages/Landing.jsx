import { useNavigate } from "react-router-dom";

function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">
          Welcome to MyApp
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Join us to explore amazing features and connect with others!
        </p>
        <div className="flex justify-center gap-4">
          <button
            onClick={() => navigate("/login")}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/register")}
            className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
}

export default Landing;
