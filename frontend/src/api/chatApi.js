import axiosClient from './axiosClient';

export const chatApi = {
  sendMessage: async (message, history) => {
    const response = await axiosClient.post('/chat/', { message, history });
    return response.data;
  },
};
