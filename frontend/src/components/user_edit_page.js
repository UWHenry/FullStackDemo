import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Container, Row, Col, Form, Button, Dropdown } from 'react-bootstrap';
import axiosInstance from '../utils/axiosInstance';

function UserEditPage({ isLoggedIn }) {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState("");
    const [roles, setRoles] = useState({});
    // const [selectedRoles, setSelectedRoles] = useState([]);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        address: ''
    });

    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/login');
        }
    }, [isLoggedIn, navigate]);

    //get list of roles
    useEffect(() => {
        try {
            axiosInstance.get(`/api/roles`)
                .then((response) => {
                    setRoles(response.data.reduce((acc, role) => {
                        acc[role.rolename] = role;
                        return acc;
                    }, {}));
                })
                .catch((error) => {
                    console.error('Roles fetch failed:', error);
                });
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };
    const handleRoleSelect = (role) => {
        console.log(role.checked)
        if (role.checked) {
            role.checked = false;
        } else {
            role.checked = true;
        }
        // if (selectedRoles.includes(rolename)) {
        //     setSelectedRoles(selectedRoles.filter((role) => role !== rolename));
        // } else {
        //     setSelectedRoles([...selectedRoles, rolename]);
        // }
        // console.log(selectedRoles)
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrorMessage("")
        try {
            // const headers = {
            //     'Accept': 'application/json',
            //     'Content-Type': 'application/json',
            // };
            // axiosInstance.post('/api/signup', formData, { headers: headers })
            //     .then((response) => {
            //         sessionStorage.setItem("jwtToken", response.data.access_token);
            //         navigate('/');
            //     })
            //     .catch((error) => {
            //         let errMessage = error.response.data?.message;
            //         if  (errMessage) {
            //             setErrorMessage(errMessage)
            //         }
            //         console.error('POST request failed:', error);
            //     });
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    return (
        <Container>
            <Row className="justify-content-center mt-5">
                <Col xs={12} md={6}>
                    <h1>User Form</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="username" className="mt-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder="Enter your username" name="username"
                                value={formData.username} onChange={handleChange} required />
                        </Form.Group>

                        <Form.Group controlId="address" className="mt-3">
                            <Form.Label>Address</Form.Label>
                            <Form.Control type="textf" placeholder="Enter your address" name="address"
                                value={formData.address} onChange={handleChange} />
                        </Form.Group>

                        <Form.Group controlId="roles" className="mt-3">
                            <Form.Label>Roles</Form.Label>
                            <Dropdown>
                                <Dropdown.Toggle variant="primary">
                                    Select Roles
                                </Dropdown.Toggle>

                                <Dropdown.Menu>
                                    {Object.keys(roles).map((role) => (
                                        <Dropdown.Item key={role.rolename}>
                                            <Form.Check
                                                type="checkbox"
                                                label={`Name: ${role.rolename}, Permission: ${role.permission}`}
                                                checked={role.checked}
                                                onChange={() => handleRoleSelect(role)}
                                            />
                                        </Dropdown.Item>
                                    ))}
                                </Dropdown.Menu>
                            </Dropdown>
                        </Form.Group>

                        <Button variant="primary" type="submit" className="mt-3">
                            Submit
                        </Button>
                        <div>
                            <p className='mt-3'>{errorMessage}</p>
                        </div>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default UserEditPage;
