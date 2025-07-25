import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import axiosInstance from "@/axios";
import { clearUser } from "@/redux/userSlice";

function Navbar() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axiosInstance.post("/api/auth/logout/");
      dispatch(clearUser());
      navigate("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <nav className="w-full bg-white shadow-md p-4 flex justify-between items-center fixed top-0">
      <div className="text-xl font-bold text-blue-600">MyApp</div>
      <button
        onClick={handleLogout}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Logout
      </button>
    </nav>
  );
}

export default Navbar;
