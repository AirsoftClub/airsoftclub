import { axiosInstance } from "@/services/axios/axios-service";
import { useQuery } from "@tanstack/react-query";

export const GET_ME_QUERY_KEY = ["me"];

export const getMe = async () => {
  const { data } = await axiosInstance.get("/users/me");
  return data;
};

export const useMe = () => useQuery(GET_ME_QUERY_KEY, getMe);
