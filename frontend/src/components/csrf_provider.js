import React, { createContext, useState, useEffect } from 'react';
import axiosInstance from '../utils/axiosInstance';

const CsrfContext = createContext();

function CsrfProvider({ children }) {
    const [csrfToken, setCsrfToken] = useState('');

    useEffect(() => {
        // Fetch the CSRF token from the backend
        axiosInstance.get('/api/get_csrf_token')
            .then(response => {
                setCsrfToken(response.data.csrf_token);
            })
            .catch(error => {
                console.error('Error fetching CSRF token:', error);
            });
    }, []);

    return (
        <CsrfContext.Provider value={{ csrfToken, setCsrfToken }}>
            {children}
        </CsrfContext.Provider>
    );
};

export { CsrfProvider, CsrfContext };