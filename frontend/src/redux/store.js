import { configureStore, combineReducers } from "@reduxjs/toolkit";
import userReducer from "./userSlice.js";

export default configureStore({
  reducer: combineReducers({
    user: userReducer,
  }),
});
