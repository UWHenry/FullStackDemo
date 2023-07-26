import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import NavigationMenu from './navigation_menu';
import SignupPage from './signup_page';
import LoginPage from './login_page';
import LogoutPage from './logout_page';
import UserListPage from './user_list_page';
import UserEditPage from './user_edit_page';
import RoleListPage from './role_list_page';
import RoleEditPage from './role_edit_page';
import OptimisticLockTestingPage from './optimistic_lock_testing_page';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const jwtToken = sessionStorage.getItem('jwtToken');
        setIsLoggedIn(!!jwtToken);
    }, []);

    return (
        <Router>
            <NavigationMenu isLoggedIn={isLoggedIn} />
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
        </Router>
    );
}

export default App;
