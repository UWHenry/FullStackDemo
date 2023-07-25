import React from 'react';
import ReactDOM from 'react-dom/client';
import { FrontPage } from './component/front_page'
import { CsrfProvider } from './component/csrf_provider';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <CsrfProvider>
            <FrontPage />
        </CsrfProvider>
    </React.StrictMode>
);