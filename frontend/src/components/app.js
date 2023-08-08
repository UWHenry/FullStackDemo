import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';

import NavigationMenu from './NavigationMenu';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import LogoutPage from './pages/LogoutPage';
import UserListPage from './pages/UserListPage';
import UserEditPage from './pages/UserEditPage';
import RoleListPage from './pages/RoleListPage';
import RoleEditPage from './pages/RoleEditPage';
import OptimisticLockTestingPage from './pages/OptimisticLockTestingPage';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
        <Router>
            <NavigationMenu isLoggedIn={isLoggedIn} />
            <Container>
                <Routes>
                    <Route path="/" element={<Navigate to="/user" />} />
                    <Route path="/user" element={<UserListPage isLoggedIn={isLoggedIn} />} />
                    <Route path="/user/edit" element={<UserEditPage />} />
                    <Route path="/role" element={<RoleListPage isLoggedIn={isLoggedIn} />} />
                    <Route path="/role/edit" element={<RoleEditPage />} />
                    <Route path="/optimistic_lock_test" element={<OptimisticLockTestingPage isLoggedIn={isLoggedIn} />} />
                    <Route path="/signup" element={<SignupPage setIsLoggedIn={setIsLoggedIn} />} />
                    <Route path="/login" element={<LoginPage setIsLoggedIn={setIsLoggedIn} />} />
                    <Route path="/logout" element={<LogoutPage setIsLoggedIn={setIsLoggedIn} />} />
                </Routes>
            </Container>
        </Router>
    );
}

export default App;
