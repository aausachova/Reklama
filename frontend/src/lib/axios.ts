import axios from "axios";

const apiClient = axios.create({
  baseURL: "/",
  withCredentials: true,
});

// let isRefreshing = false;

// interface QueueItem {
//   resolve: (value?: unknown) => void;
//   reject: (reason?: any) => void;
// }

// let failedQueue: QueueItem[] = [];

// const processQueue = (error: any = null) => {
//   failedQueue.forEach((prom) => {
//     if (error) {
//       prom.reject(error);
//     } else {
//       prom.resolve();
//     }
//   });
//   failedQueue = [];
// };

// apiClient.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;

//     if (error.response?.status === 401 && !originalRequest._retry) {
//       if (isRefreshing) {
//         return new Promise((resolve, reject) => {
//           failedQueue.push({ resolve, reject });
//         })
//           .then(() => apiClient(originalRequest))
//           .catch((err) => Promise.reject(err));
//       }

//       originalRequest._retry = true;
//       isRefreshing = true;

//       const authStore = useAuthStore();
//       try {
//         await authStore.refreshTokens();
//         processQueue();
//         return apiClient(originalRequest);
//       } catch (refreshError) {
//         processQueue(refreshError);
//         authStore.logout();
//         return Promise.reject(refreshError);
//       } finally {
//         isRefreshing = false;
//       }
//     }

//     return Promise.reject(error);
//   }
// );

export default apiClient;
