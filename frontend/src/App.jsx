import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginView from "./views/LoginView";
import RegisterView from "./views/RegisterView";
import DashboardView from "./views/DashboardView";
import PrereqVerifyView from "./views/PrereqVerifyView";
import TutorProfileView from "./views/TutorProfileView";
import TutorMatchView from "./views/TutorMatchView";
import TutorSlotsView from "./views/TutorSlotsView";
import BookSessionView from "./views/BookSessionView";
import PaymentsView from "./views/PaymentsView";
import TutorEarningsView from "./views/TutorEarningsView";
import TutorReviewsView from "./views/TutorReviewsView";
import IssueReportView from './views/IssueReportView';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginView />} />
          <Route path="/register" element={<RegisterView />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardView />
              </ProtectedRoute>
            }
            />
          
          <Route 
            path="/issues" 
            element={
              <ProtectedRoute>
                <IssueReportView />
              </ProtectedRoute>
            } 
            />  
          <Route
            path="/verify"
            element={
              <ProtectedRoute>
                <PrereqVerifyView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <TutorProfileView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/find-tutor"
            element={
              <ProtectedRoute>
                <TutorMatchView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/my-slots"
            element={
              <ProtectedRoute>
                <TutorSlotsView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/sessions"
            element={
              <ProtectedRoute>
                <BookSessionView />
              </ProtectedRoute>
            }
          />
                    <Route
            path="/payments"
            element={
              <ProtectedRoute>
                <PaymentsView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/earnings"
            element={
              <ProtectedRoute>
                <TutorEarningsView />
              </ProtectedRoute>
            }
          />          <Route
            path="/tutors/:tutorId/reviews"
            element={
              <ProtectedRoute>
                <TutorReviewsView />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
