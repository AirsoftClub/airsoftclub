"use client"

import axios, { AxiosInstance } from "axios";
import { cookies } from "next/headers"

const createAxiosInstace = (): AxiosInstance => {
    const instance = axios.create({
        baseURL: process.env.NEXT_PUBLIC_API_URL,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    instance.interceptors.request.use((config) => {
        const cookieStore = cookies();
        const token = cookieStore.get('token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    });

    return instance;
}

export const axiosService = createAxiosInstace();