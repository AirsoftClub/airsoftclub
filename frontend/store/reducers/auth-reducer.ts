import { PayloadAction, createSlice } from "@reduxjs/toolkit";

export interface AuthSate {
  token: string | null;
}

const initialState: AuthSate = {
  token: null,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login: (state: AuthSate, action: PayloadAction<string>) => {
      state.token = action.payload;
    },
    logout: (state: AuthSate) => {
      state.token = null;
    },
  },
});

export const { login, logout } = authSlice.actions;

export default authSlice.reducer;
