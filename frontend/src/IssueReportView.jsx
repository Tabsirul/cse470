import React, { useState } from 'react';

const IssueReportView = ({ sessionId }) => {
  const [issueType, setIssueType] = useState('missed_appointment');
  const [description, setDescription] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage('Submitting...');

    try {
      const response = await fetch('http://localhost:8000/api/issues/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId || 1,
          issue_type: issueType,
          description: description
        })
      });

      if (response.ok) {
        setStatusMessage('Issue reported successfully. An admin will review it shortly.');
        setDescription('');
      } else {
        setStatusMessage('Failed to submit the report. Please try again.');
      }
    } catch (error) {
      console.error("Error submitting report:", error);
      setStatusMessage('Network error. Is the server running?');
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto', padding: '20px', fontFamily: 'sans-serif', background: '#fff', borderRadius: '8px' }}>
      <h2>Report an Issue</h2>
      <p>Use this form to report missed appointments, late arrivals, or unhelpful sessions.</p>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <div>
          <label htmlFor="issueType" style={{ fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>Issue Type:</label>
          <select 
            id="issueType" 
            value={issueType} 
            onChange={(e) => setIssueType(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
          >
            <option value="missed_appointment">Missed Appointment / No-show</option>
            <option value="late_arrival">Late Arrival</option>
            <option value="unhelpful_session">Unhelpful Session</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <label htmlFor="description" style={{ fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>Description & Proof:</label>
          <textarea 
            id="description" 
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Please provide details about what went wrong..."
            rows="5"
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <button 
          type="submit" 
          style={{ padding: '10px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Submit Escalation
        </button>
      </form>

      {statusMessage && (
        <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px' }}>
          {statusMessage}
        </div>
      )}
    </div>
  );
};

export default IssueReportView;