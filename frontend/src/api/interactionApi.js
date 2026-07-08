import axiosClient from './axiosClient';

export const interactionApi = {
  createInteraction: async (interactionData) => {
    const response = await axiosClient.post('/interactions/', interactionData);
    return response.data;
  },
  getInteractions: async (skip = 0, limit = 100) => {
    const response = await axiosClient.get(`/interactions/?skip=${skip}&limit=${limit}`);
    return response.data;
  },
};
