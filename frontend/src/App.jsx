import {
  Routes,
  Route,
  Navigate,
  useNavigate,
  useLocation,
} from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { useEffect } from "react";
import { setUser, setLoading, setError } from "@/redux/userSlice";
import axiosInstance from "@/axios";
import Home from "@/pages/Home";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Landing from "@/pages/Landing";
import Navbar from "@/components/Navbar";

function App() {
  const { id, username, email, loading, isLoggedOut } = useSelector(
    (state) => state.user
  );
  const isAuthenticated = !!id || !!username;
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    console.log(
      "App: isAuthenticated:",
      isAuthenticated,
      "User:",
      { id, username, email, isLoggedOut },
      "Path:",
      location.pathname
    ); // Debug log
    const checkAuth = async () => {
      // Skip auth check for /, /login, /register, or if logged out
      if (
        location.pathname === "/" ||
        location.pathname === "/login" ||
        location.pathname === "/register" ||
        isLoggedOut
      ) {
        return;
      }

      if (!isAuthenticated && !loading) {
        dispatch(setLoading());
        try {
          const response = await axiosInstance.get("/api/auth/user/");
          console.log("App: User fetched:", response.data); // Debug log
          dispatch(setUser(response.data));
        } catch (error) {
          console.error("App: Auth error:", error); // Debug log
          dispatch(setError("Not authenticated"));
          navigate("/login", { replace: true });
        }
      }
    };

    checkAuth();
  }, [
    isAuthenticated,
    loading,
    isLoggedOut,
    dispatch,
    navigate,
    location.pathname,
  ]);

  return (
    <div className="min-h-screen bg-gray-100">
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route
          path="/home"
          element={
            isAuthenticated ? <Home /> : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/login"
          element={
            !isAuthenticated ? <Login /> : <Navigate to="/home" replace />
          }
        />
        <Route
          path="/register"
          element={
            !isAuthenticated ? <Register /> : <Navigate to="/home" replace />
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;
