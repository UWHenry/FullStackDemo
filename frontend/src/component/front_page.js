import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { SignupForm } from './signup_form'

function FrontPage(property) {
    
    return (
        <Container>
            <Row className="justify-content-center mt-5">
                <Col xs={12} md={6}>
                    <SignupForm />
                </Col>
            </Row>

        </Container>
    )
}

export { FrontPage };