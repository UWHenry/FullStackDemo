import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Container, Row, Col, Form, Button, Dropdown } from "react-bootstrap";
import axiosInstance from "../utils/axiosInstance";

function UserEditPage() {
    const location = useLocation();
    const { user = {}, isLoggedIn = false } = location.state ?? {};
    const newUser = (Object.keys(user).length === 0);
    const [errorMessage, setErrorMessage] = useState("");
    const [formData, setFormData] = useState({
        username: user?.username ?? "",
        password: "",
        address: user?.address ?? "",
        roles: user?.roles?.map((role) => role.rolename) ?? []
    });

    //check login status
    //redirects to login page if not logged in
    //get list of roles if logged in 
    const navigate = useNavigate();
    const [roles, setRoles] = useState([]);
    useEffect(() => {
        if (!isLoggedIn) {
            navigate("/login");
        } else {
            try {
                axiosInstance.get(`/api/roles`)
                    .then((response) => {
                        setRoles(response.data);
                    })
                    .catch((error) => {
                        console.error("Roles fetch failed:", error);
                    });
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        }
    }, [isLoggedIn, navigate]);

    //update form on first two text fields
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };
    //update form on dropdown checkbox
    const handleRoleSelect = (e) => {
        let rolename = e.target.getAttribute("role-id");
        if (formData.roles.includes(rolename)) {
            setFormData({ ...formData, roles: formData.roles.filter(role => role !== rolename)});
        } else {
            setFormData({ ...formData, roles: [...formData.roles, rolename]});
        }
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrorMessage("");
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        };
        try {
            const endpoint = newUser ? "/api/signup" : `/api/user/${formData.username}`;
            const method = newUser ? "post" : "put";
            const { address, roles } = formData;
            const payload = newUser ? formData: {address, roles};
            await axiosInstance[method](endpoint, payload, { headers });
        } catch (error) {
            let errMessage = error.response.data?.message;
            if (errMessage) {
                setErrorMessage(errMessage);
            }
            console.error(`${newUser ? "Create" : "Update"} User failed:`, error);
        }
        navigate("/user");
    };
    const handleCancel = (e) => {
        navigate("/user");
    }

    return (
        <Container>
            <Row className="justify-content-center mt-5">
                <Col xs={12} md={6}>
                    <h1>User Form</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="username" className="mt-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder="Enter your username" name="username" value={formData.username} 
                                onChange={handleChange} required disabled={!newUser}/>
                        </Form.Group>

                        <Form.Group controlId="password" className="mt-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="text" placeholder="Enter your password" name="password" value={formData.password} 
                                onChange={handleChange} required disabled={!newUser}/>
                        </Form.Group>

                        <Form.Group controlId="address" className="mt-3">
                            <Form.Label>Address</Form.Label>
                            <Form.Control type="text" placeholder="Enter your address" name="address" value={formData.address} onChange={handleChange} />
                        </Form.Group>

                        <Form.Group controlId="roles" className="mt-3">
                            <Form.Label>Roles</Form.Label>
                            <Dropdown autoClose={false}>
                                <Dropdown.Toggle variant="primary">Select Roles</Dropdown.Toggle>
                                <Dropdown.Menu>
                                    {roles.map((role) => (
                                        <Dropdown.Item key={role.rolename}>
                                            <Form.Check
                                                type="checkbox"
                                                label={`Name: ${role.rolename}, Permission: ${role.permission}`}
                                                checked={formData.roles.includes(role.rolename)}
                                                role-id={role.rolename}
                                                onChange={handleRoleSelect}
                                                key={JSON.stringify(formData)}
                                            />
                                        </Dropdown.Item>
                                    ))}
                                </Dropdown.Menu>
                            </Dropdown>
                        </Form.Group>
                        <Row className="mt-3">
                            <Col className="d-flex justify-content-between">
                                <Button variant="primary" type="submit" className="mt-3">Submit</Button>
                                <Button variant="danger" type="button" className="mt-3" onClick={handleCancel}>Cancel</Button>
                            </Col>
                        </Row>
                    </Form>
                    <div>
                        <p className="mt-3">{errorMessage}</p>
                    </div>
                </Col>
            </Row>
        </Container>
    );
}

export default UserEditPage;
