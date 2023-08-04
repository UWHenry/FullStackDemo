import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function LogoutPage({ setIsLoggedIn }) {
    const navigate = useNavigate();
    useEffect(() => {
        sessionStorage.removeItem('jwtToken');
        setIsLoggedIn(false);
        navigate('/login');
    }, [setIsLoggedIn, navigate]);
    return null;
}
export default LogoutPage;