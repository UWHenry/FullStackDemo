import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../../utils/axiosInstance';
import { Row, Col } from 'react-bootstrap';

function LogoutPage({ setIsLoggedIn }) {
    const navigate = useNavigate();
    useEffect(() => {
        axiosInstance.post('/api/logout')
            .then(() => {
                setIsLoggedIn(false);
                setTimeout(() => {
                    navigate('/login');
                }, 1000);
            });
    }, [setIsLoggedIn, navigate]);
    return (
        <Row className="justify-content-center mt-5">
            <Col xs={12} md={6}>
                <h1>Logout</h1>
            </Col>
        </Row>
    );
}
export default LogoutPage;