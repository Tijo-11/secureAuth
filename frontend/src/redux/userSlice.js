import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  id: null,
  username: null,
  email: null,
  loading: false,
  error: null,
  isLoggedOut: false, // New flag
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action) => {
      state.id = action.payload.id;
      state.username = action.payload.username;
      state.email = action.payload.email;
      state.loading = false;
      state.error = null;
      state.isLoggedOut = false; // Reset on login
    },
    clearUser: (state) => {
      state.id = null;
      state.username = null;
      state.email = null;
      state.loading = false;
      state.error = null;
      state.isLoggedOut = true; // Set on logout
    },
    setLoading: (state) => {
      state.loading = true;
      state.error = null;
    },
    setError: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
  },
});

export const { setUser, clearUser, setLoading, setError } = userSlice.actions;
export default userSlice.reducer;
