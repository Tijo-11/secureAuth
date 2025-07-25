import axios from "axios";
import store from "@/redux/store";
import { clearUser } from "@/redux/userSlice";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

axiosInstance.interceptors.request.use(async (config) => {
  if (
    config.method.toLowerCase() === "post" &&
    !config.headers["X-CSRFToken"]
  ) {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/auth/csrf/", {
        withCredentials: true,
      });
      console.log("Interceptor: Fetched CSRF token:", response.data.csrfToken); // Debug log
      config.headers["X-CSRFToken"] = response.data.csrfToken;
    } catch (error) {
      console.error(
        "Interceptor: CSRF fetch error:",
        error.response?.data || error.message
      ); // Debug log
    }
  }
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;

    console.log(
      "Interceptor: Error status:",
      status,
      "Request:",
      originalRequest.url,
      "Headers:",
      originalRequest.headers
    ); // Debug log
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const response = await axiosInstance.post("/api/auth/refresh/");
        console.log("Interceptor: Refresh response:", response.data); // Debug log
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error(
          "Interceptor: Refresh token error:",
          refreshError.response?.data || refreshError.message
        ); // Debug log
        store.dispatch(clearUser());
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
