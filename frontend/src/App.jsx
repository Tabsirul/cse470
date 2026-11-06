import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginView from "./views/LoginView";
import RegisterView from "./views/RegisterView";
import DashboardView from "./views/DashboardView";
import PrereqVerifyView from "./views/PrereqVerifyView";
import TutorProfileView from "./views/TutorProfileView";
import TutorMatchView from "./views/TutorMatchView";

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
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}