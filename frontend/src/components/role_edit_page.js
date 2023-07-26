import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Container, Row, Col, Form, Button, Dropdown } from "react-bootstrap";
import axiosInstance from "../utils/axiosInstance";

function RoleEditPage() {
    const location = useLocation();
    const { role = {}, isLoggedIn = false } = location.state ?? {};
    const newRole = (Object.keys(role).length === 0);
    const [errorMessage, setErrorMessage] = useState("");
    const [formData, setFormData] = useState({
        rolename: role?.rolename ?? "",
        permission: role?.permission ?? "",
        description: role?.description ?? "",
        users: role?.users?.map((user) => user.username) ?? []
    });

    //check login status
    //redirects to login page if not logged in
    //get list of users if logged in 
    const navigate = useNavigate();
    const [users, setUsers] = useState([]);
    useEffect(() => {
        if (!isLoggedIn) {
            navigate("/login");
        } else {
            try {
                axiosInstance.get(`/api/users`)
                    .then((response) => {
                        setUsers(response.data);
                    })
                    .catch((error) => {
                        console.error("Users fetch failed:", error);
                    });
            } catch (error) {
                console.error("Error fetching roles:", error);
            }
        }
    }, [isLoggedIn, navigate]);

    //update form on first two text fields
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };
    //update form on dropdown checkbox
    const handleUserSelect = (e) => {
        let username = e.target.getAttribute("user-id");
        if (formData.users.includes(username)) {
            setFormData({ ...formData, users: formData.users.filter(user => user !== username)});
        } else {
            setFormData({ ...formData, users: [...formData.users, username]});
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
            const endpoint = "/api/role";
            const method = newRole ? "post" : "put";
            await axiosInstance[method](endpoint, formData, { headers });
        } catch (error) {
            let errMessage = error.response.data?.message;
            if (errMessage) {
                setErrorMessage(errMessage);
            }
            console.error(`${newRole ? "Create" : "Update"} Role failed:`, error);
        }
        navigate("/role");
    };
    const handleCancel = (e) => {
        navigate("/role");
    }

    return (
        <Container>
            <Row className="justify-content-center mt-5">
                <Col xs={12} md={6}>
                    <h1>Role Form</h1>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="rolename" className="mt-3">
                            <Form.Label>Rolename</Form.Label>
                            <Form.Control type="text" placeholder="Enter your rolename" name="rolename" value={formData.rolename} 
                                onChange={handleChange} required disabled={!newRole}/>
                        </Form.Group>

                        <Form.Group controlId="permission" className="mt-3">
                            <Form.Label>Permission</Form.Label>
                            <Form.Control type="text" placeholder="Enter your permission" name="permission" value={formData.permission} 
                                onChange={handleChange} required/>
                        </Form.Group>

                        <Form.Group controlId="description" className="mt-3">
                            <Form.Label>Description</Form.Label>
                            <Form.Control type="text" placeholder="Enter your description" name="description" value={formData.description} onChange={handleChange} />
                        </Form.Group>

                        <Form.Group controlId="users" className="mt-3">
                            <Form.Label>Users</Form.Label>
                            <Dropdown autoClose={false}>
                                <Dropdown.Toggle variant="primary">Select Users</Dropdown.Toggle>
                                <Dropdown.Menu>
                                    {users.map((user) => (
                                        <Dropdown.Item key={user.username}>
                                            <Form.Check
                                                type="checkbox"
                                                label={user.username}
                                                checked={formData.users.includes(user.username)}
                                                user-id={user.username}
                                                onChange={handleUserSelect}
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

export default RoleEditPage;
