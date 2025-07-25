import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setUser, setLoading, setError } from "@/redux/userSlice";
import axiosInstance from "@/axios";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setLocalError] = useState("");
  const {
    id,
    username: reduxUsername,
    loading,
  } = useSelector((state) => state.user);
  const isAuthenticated = !!id || !!reduxUsername;
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      console.log(
        "Login: Redirecting to /home, isAuthenticated:",
        isAuthenticated
      ); // Debug log
      navigate("/home", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return; // Prevent resubmission
    setLocalError("");
    dispatch(setLoading());
    try {
      const loginResponse = await axiosInstance.post("/api/auth/login/", {
        username,
        password,
      });
      console.log("Login response:", loginResponse.data); // Debug log
      const userResponse = await axiosInstance.get("/api/auth/user/");
      console.log("User data:", JSON.stringify(userResponse.data, null, 2)); // Debug log
      dispatch(setUser(userResponse.data));
      // Fallback navigation
      if (userResponse.data.username) {
        console.log("Login: Fallback navigate to /home"); // Debug log
        navigate("/home", { replace: true });
      }
    } catch (err) {
      const message = err.response?.data?.detail || "Login failed";
      console.error("Login error:", err, "Message:", message); // Debug log
      setLocalError(message);
      dispatch(setError(message));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2" htmlFor="username">
              Username
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          {error && <p className="text-red-500 mb-4">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className={`w-full p-2 rounded text-white ${
              loading
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-500 hover:bg-blue-600"
            }`}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
