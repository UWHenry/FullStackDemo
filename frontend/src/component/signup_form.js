import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import { useState, useContext } from 'react';
import { CsrfContext } from './csrf_provider';
import getCsrfToken from '../utils/csrfToken';


function SignupForm(property) {
    const { csrfToken } = useContext(CsrfContext);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        address: '',
        csrf_token: csrfToken
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log(csrfToken)
            const headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-XSRF-TOKEN': csrfToken
            };
            // console.log(headers)
            axios.post('https://localhost:8000/api/signup', formData, { headers: headers, credentials: 'include', mode: 'cors'})
                .then((response) => {
                    // Handle the response data
                    console.log(response.data);
                })
                .catch((error) => {
                    // Handle errors
                    console.error('POST request failed:', error);
                });
            // console.log('Backend response:', response.data);
            // Do something with the response, such as redirect or display a success message
        } catch (error) {
            console.error('Error submitting form:', error);
            // Handle the error, such as displaying an error message
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
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
        </Form>
    );
}
export { SignupForm };