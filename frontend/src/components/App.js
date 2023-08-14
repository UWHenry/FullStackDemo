import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';

import { SocketProvider } from './WebSocketProvider';
import axiosInstance from '../utils/axiosInstance';
import NavigationMenu from './NavigationMenu';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import LogoutPage from './pages/LogoutPage';
import UserListPage from './pages/UserListPage';
import UserEditPage from './pages/UserEditPage';
import RoleListPage from './pages/RoleListPage';
import RoleEditPage from './pages/RoleEditPage';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axiosInstance.get('/api/check-auth')
            .then(response => {
                setIsLoggedIn(true);
            })
            .catch(error => {
                setIsLoggedIn(false);
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }
    return (
        <Router>
            <SocketProvider setIsLoggedIn={setIsLoggedIn}>
                <NavigationMenu isLoggedIn={isLoggedIn} />
                <Container>
                    <Routes>
                        <Route path="/" element={<Navigate to="/user" />} />
                        <Route path="/user" element={<UserListPage isLoggedIn={isLoggedIn} />} />
                        <Route path="/user/edit" element={<UserEditPage />} />
                        <Route path="/role" element={<RoleListPage isLoggedIn={isLoggedIn} />} />
                        <Route path="/role/edit" element={<RoleEditPage />} />
                        <Route path="/signup" element={<SignupPage setIsLoggedIn={setIsLoggedIn} />} />
                        <Route path="/login" element={<LoginPage setIsLoggedIn={setIsLoggedIn} />} />
                        <Route path="/logout" element={<LogoutPage setIsLoggedIn={setIsLoggedIn} />} />
                    </Routes>
                </Container>
            </SocketProvider>
        </Router>
    );
}

export default App;
