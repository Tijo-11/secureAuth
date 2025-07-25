import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { clearUser, setLoading, setError } from "@/redux/userSlice";
import axiosInstance from "@/axios";

function Home() {
  const { username, loading } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = async (e) => {
    e.preventDefault();
    if (loading) return;
    dispatch(setLoading());
    try {
      const response = await axiosInstance.post("/api/auth/logout/");
      console.log("Logout response:", response.data); // Debug log
      dispatch(clearUser());
      console.log("Home: Navigating to /"); // Debug log
      navigate("/", { replace: true });
    } catch (err) {
      const message = err.response?.data?.detail || "Logout failed";
      console.error("Logout error:", err, "Message:", message); // Debug log
      dispatch(setError(message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">
        Welcome, {username}!
      </h1>
      <p className="text-lg text-gray-600 mb-8">
        You are now logged in to MyApp.
      </p>
      <button
        onClick={handleLogout}
        disabled={loading}
        className={`px-6 py-3 rounded-lg text-white ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-red-500 hover:bg-red-600"
        }`}
      >
        {loading ? "Logging out..." : "Logout"}
      </button>
    </div>
  );
}

export default Home;
