import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { interactionApi } from '../../api/interactionApi';

export const submitInteraction = createAsyncThunk(
  'interaction/submit',
  async (interactionData, { rejectWithValue }) => {
    try {
      const response = await interactionApi.createInteraction(interactionData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || { message: "Something went wrong." });
    }
  }
);

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    formData: {
      hcp_name: '',
      interaction_type: 'Meeting',
      interaction_date: new Date().toISOString().split('T')[0],
      interaction_time: new Date().toTimeString().split(' ')[0].substring(0, 5),
      attendees: '',
      topics_discussed: '',
      materials_shared: '',
      samples_distributed: '',
      sentiment: 'Neutral',
      outcomes: '',
      follow_up_actions: ''
    },
    status: 'idle',
    error: null,
  },
  reducers: {
    updateFormField: (state, action) => {
      const { field, value } = action.payload;
      state.formData[field] = value;
    },
    resetForm: (state) => {
      state.formData = {
        hcp_name: '',
        interaction_type: 'Meeting',
        interaction_date: new Date().toISOString().split('T')[0],
        interaction_time: new Date().toTimeString().split(' ')[0].substring(0, 5),
        attendees: '',
        topics_discussed: '',
        materials_shared: '',
        samples_distributed: '',
        sentiment: 'Neutral',
        outcomes: '',
        follow_up_actions: ''
      };
      state.status = 'idle';
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(submitInteraction.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(submitInteraction.fulfilled, (state, action) => {
        state.status = 'succeeded';
        // Can optionally clear form here or leave it to component
      })
      .addCase(submitInteraction.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  }
});

export const { updateFormField, resetForm } = interactionSlice.actions;
export default interactionSlice.reducer;
