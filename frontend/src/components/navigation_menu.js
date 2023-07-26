import { Container, Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function NavigationMenu({ isLoggedIn }) {
    return (
        <Navbar bg="dark" data-bs-theme="dark">
            <Container>
                <Navbar.Brand>Welcome</Navbar.Brand>
                <Nav className="me-auto">
                    <Link to="/user" className="nav-link">Users</Link>
                    <Link to="/role" className="nav-link">Roles</Link>
                    <Link to="/optimistic_lock_test" className="nav-link">Optimistic Lock Test</Link>
                    {isLoggedIn ? <Link to="/logout" className="nav-link">Logout</Link> : null}
                    {isLoggedIn ? null : <Link to="/login" className="nav-link">Login</Link>}
                    {isLoggedIn ? null : <Link to="/signup" className="nav-link">Signup</Link>}
                </Nav>
            </Container>
        </Navbar>
    );
}

export default NavigationMenu;