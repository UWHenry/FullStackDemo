import { Form, Button } from 'react-bootstrap';


function LoginForm(property) {
    return (
        <Form>
            <Form.Group controlId="username" className="mt-3">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Enter your username" />
            </Form.Group>

            <Form.Group controlId="password" className="mt-3">
                <Form.Label>Password</Form.Label>
                <Form.Control type="email" placeholder="Enter your password" />
            </Form.Group>

            <Button variant="primary" type="submit" className="mt-3">
                Login          
            </Button>
        </Form>
    );
}
export { LoginForm };