import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { reportIssue } from '../api/issueApi';
// NOTE: Make sure this import matches your actual booking API file!
import { getMyBookings } from '../api/sessionApi'; 

const IssueReportView = () => {
    const [bookings, setBookings] = useState([]);
    const [formData, setFormData] = useState({
        booking_id: '',
        issue_type: 'missed_appointment',
        description: ''
    });
    const navigate = useNavigate();
    
    // Fetch token from local storage (adjust if your app uses a Context instead)
    const token = localStorage.getItem('token'); 

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const data = await getMyBookings(token);
                setBookings(data);
            } catch (error) {
                console.error("Failed to load bookings", error);
            }
        };
        if (token) fetchBookings();
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await reportIssue(token, formData);
            alert("Report submitted successfully!");
            navigate('/dashboard'); // Go back to dashboard
        } catch (error) {
            alert(error.response?.data?.detail || "Failed to submit report");
        }
    };

    return (
        <div className="container mt-4">
            <h2>Report an Issue</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Select Booking:</label>
                    <select 
                        className="form-select"
                        required
                        value={formData.booking_id}
                        onChange={(e) => setFormData({...formData, booking_id: e.target.value})}
                    >
                        <option value="">-- Choose a booking --</option>
                        {bookings.map(b => (
                            <option key={b.id} value={b.id}>
                                Booking #{b.id} - {b.subject || b.course_name || 'Session'}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="mb-3">
                    <label className="form-label">Issue Type:</label>
                    <select 
                        className="form-select"
                        value={formData.issue_type}
                        onChange={(e) => setFormData({...formData, issue_type: e.target.value})}
                    >
                        <option value="missed_appointment">Missed Appointment</option>
                        <option value="late_arrival">Late Arrival</option>
                        <option value="unhelpful_session">Unhelpful Session</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <div className="mb-3">
                    <label className="form-label">Description:</label>
                    <textarea 
                        className="form-control"
                        required 
                        minLength="10" 
                        maxLength="1000"
                        rows="4"
                        value={formData.description}
                        onChange={(e) => setFormData({...formData, description: e.target.value})}
                    />
                </div>

                <button type="submit" className="btn btn-primary">Submit Report</button>
            </form>
        </div>
    );
};

export default IssueReportView;