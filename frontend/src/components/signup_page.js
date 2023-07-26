import { useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';


function SignupPage({setIsLoggedIn}) {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState("");
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        address: ''
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
            axiosInstance.post('/api/signup', formData, { headers: headers })
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
                    <h1>Sign Up</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="username" className="mt-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder="Enter your username" name="username"
                                value={formData.username} onChange={handleChange} required />
                        </Form.Group>

                        <Form.Group controlId="password" className="mt-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="text" placeholder="Enter your password" name="password"
                                value={formData.password} onChange={handleChange} required />
                        </Form.Group>

                        <Form.Group controlId="address" className="mt-3">
                            <Form.Label>Address</Form.Label>
                            <Form.Control type="textf" placeholder="Enter your address" name="address"
                                value={formData.address} onChange={handleChange} />
                        </Form.Group>

                        <Button variant="primary" type="submit" className="mt-3">
                            Sign Up
                        </Button>
                        <div>
                            <p className='mt-3'>{errorMessage}</p>
                        </div>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
}
export default SignupPage;