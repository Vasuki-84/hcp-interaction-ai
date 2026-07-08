import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateFormField, submitInteraction } from '../store/slices/interactionSlice';
import { Save } from 'lucide-react';

const InteractionForm = () => {
  const dispatch = useDispatch();
  const { formData, status, error } = useSelector((state) => state.interaction);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateFormField({ field: name, value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(submitInteraction(formData));
  };

  return (
    <div className="glass-card fade-in">
      <h2 style={{ marginBottom: '1.5rem', fontSize: '1.2rem', fontWeight: '600' }}>Interaction Details</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="hcp_name">HCP Name *</label>
            <input type="text" id="hcp_name" name="hcp_name" placeholder="Search or select HCP..." value={formData.hcp_name} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="interaction_type">Interaction Type *</label>
            <select id="interaction_type" name="interaction_type" value={formData.interaction_type} onChange={handleChange} required>
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="interaction_date">Date *</label>
            <input type="date" id="interaction_date" name="interaction_date" value={formData.interaction_date} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="interaction_time">Time *</label>
            <input type="time" id="interaction_time" name="interaction_time" value={formData.interaction_time} onChange={handleChange} required />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="attendees">Attendees</label>
          <input type="text" id="attendees" name="attendees" placeholder="Enter names or search..." value={formData.attendees} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="topics_discussed">Topics Discussed</label>
          <textarea id="topics_discussed" name="topics_discussed" placeholder="Enter key discussion points..." value={formData.topics_discussed} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="materials_shared">Materials Shared / Samples Distributed</label>
          <textarea id="materials_shared" name="materials_shared" placeholder="No materials added..." value={formData.materials_shared} onChange={handleChange} />
        </div>
        
        <div className="form-group">
          <label>Observed/Inferred HCP Sentiment</label>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: '400' }}>
              <input type="radio" name="sentiment" value="Positive" checked={formData.sentiment === 'Positive'} onChange={handleChange} /> Positive
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: '400' }}>
              <input type="radio" name="sentiment" value="Neutral" checked={formData.sentiment === 'Neutral'} onChange={handleChange} /> Neutral
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: '400' }}>
              <input type="radio" name="sentiment" value="Negative" checked={formData.sentiment === 'Negative'} onChange={handleChange} /> Negative
            </label>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="outcomes">Outcomes</label>
          <textarea id="outcomes" name="outcomes" placeholder="Key outcomes or agreements..." value={formData.outcomes} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="follow_up_actions">Follow-up Actions</label>
          <textarea id="follow_up_actions" name="follow_up_actions" placeholder="Enter next steps or tasks..." value={formData.follow_up_actions} onChange={handleChange} />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
          <button type="submit" className="btn btn-primary" disabled={status === 'loading'}>
            <Save size={18} /> {status === 'loading' ? 'Saving...' : 'Save Interaction'}
          </button>
        </div>
        
        {status === 'succeeded' && <p style={{ color: 'green', marginTop: '1rem', textAlign: 'right' }}>Interaction saved successfully!</p>}
        {status === 'failed' && <p style={{ color: 'red', marginTop: '1rem', textAlign: 'right' }}>Error saving interaction.</p>}
      </form>
    </div>
  );
};

export default InteractionForm;
