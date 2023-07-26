import { useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

function LoginPage({setIsLoggedIn}) {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState("");
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrorMessage("")
        try {
            const headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            };
            axiosInstance.post('/api/login', formData, { headers: headers })
                .then((response) => {
                    sessionStorage.setItem("jwtToken", response.data.access_token);
                    setIsLoggedIn(true);
                    navigate('/');
                })
                .catch((error) => {
                    let errMessage = error.response.data?.message;
                    if  (errMessage) {
                        setErrorMessage(errMessage)
                    }
                    console.error('POST request failed:', error);
                });
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };


    return (
        <Container>
            <Row className="justify-content-center mt-5">
                <Col xs={12} md={6}>
                    <h1>Login</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="username" className="mt-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder="Enter your username" name="username"
                                value={formData.username} onChange={handleChange} required/>
                        </Form.Group>

                        <Form.Group controlId="password" className="mt-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Enter your password" name="password"
                                value={formData.password} onChange={handleChange} required />
                        </Form.Group>

                        <Button variant="primary" type="submit" className="mt-3">
                            Login
                        </Button>
                    </Form>
                    <div>
                        <p className='mt-3'>{errorMessage}</p>
                    </div>
                </Col>
            </Row>
        </Container >
    );
}
export default LoginPage;