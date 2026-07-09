import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { chatApi } from '../../api/chatApi';
import { updateFormField } from './interactionSlice';

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async (message, { getState, dispatch, rejectWithValue }) => {
    try {
      const { history } = getState().chat;
      const response = await chatApi.sendMessage(message, history);
      
      let extracted = response.extracted_data;
      if (typeof extracted === 'string') {
        try {
          extracted = JSON.parse(extracted);
        } catch (e) {
          console.error("Failed to parse extracted_data", e);
        }
      }

      if (extracted && typeof extracted === 'object') {
        console.log("Structured AI Extraction payload received:", extracted);
        Object.entries(extracted).forEach(([key, value]) => {
          if (value !== null && value !== undefined && value !== '') {
             console.log(`Mapping AI field -> ${key}:`, value);
             dispatch(updateFormField({ field: key, value }));
          } else {
             console.warn(`Ignoring empty/null AI field -> ${key}`);
          }
        });
      } else if (extracted) {
        console.error("AI returned non-object extraction data:", extracted);
      }
      
      return response.response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "Something went wrong." });
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    history: [],
    status: 'idle',
    error: null,
  },
  reducers: {
    clearChat: (state) => {
      state.history = [];
      state.status = 'idle';
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state, action) => {
        state.status = 'loading';
        // Optimistically add user message
        state.history.push({ role: 'user', content: action.meta.arg });
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.history.push({ role: 'assistant', content: action.payload });
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  }
});

export const { clearChat } = chatSlice.actions;
export default chatSlice.reducer;
