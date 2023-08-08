import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Table, FormControl, Pagination, Button } from 'react-bootstrap'
import axiosInstance from '../../utils/axiosInstance';


function UserListPage({ isLoggedIn }) {
    const navigate = useNavigate();
    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/login');
        }
    }, [isLoggedIn, navigate]);

    const [users, setUsers] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortBy, setSortBy] = useState(null);
    const [sortReverse, setSortReverse] = useState(false)
    const pageSize = 10;

    const fetchUsers = async () => {
        try {
            const response = await axiosInstance.post(`/api/users/search`, {
                "page": currentPage,
                "page_size": pageSize,
                "sort_by": sortBy,
                "reverse": sortReverse,
                "search_username": searchTerm
            });
            setUsers(response.data.users ?? []);
            setTotalPages(response.data.total_pages);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };
    useEffect(() => {
        if (isLoggedIn) {
            fetchUsers();
        }
    }, [currentPage, searchTerm, sortBy, sortReverse]);

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
        setCurrentPage(1);
    };

    const handleSort = (columnName) => {
        // Reset page when sorting
        // sorting a sorted column reverse the order
        if (columnName === sortBy) {
            setSortReverse(!sortReverse);
        } else {
            setSortReverse(false);
        }
        setSortBy(columnName);
        setCurrentPage(1);
    };

    const handleDelete = async (username) => {
        try {
            const response = await axiosInstance.delete(`/api/user/${username}`);
            if (response.data.message === "Success") {
                fetchUsers();
            }
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const handleUpdate = async (user) => {
        navigate('/user/edit', { state: { user, isLoggedIn } });
    };
    return (
        !isLoggedIn ?
        null :
        <Row className="justify-content-center mt-5">
            <Col xs={12} md={12}>
                <h1 style={{ textAlign: 'center' }}>Users</h1>
                <Button variant="primary" type="button" className="mt-3" onClick={() => handleUpdate({})}>
                    Create User
                </Button>
                <FormControl type="text" value={searchTerm} onChange={handleSearch} placeholder="Search users" />

                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th onClick={() => handleSort('username')}>Username</th>
                            <th onClick={() => handleSort('address')}>Address</th>
                            <th onClick={() => handleSort('roles')}>Roles</th>
                            <th>Update</th>
                            <th>Delete</th>
                        </tr>
                    </thead>

                    <tbody>
                        {users.map((user) => (
                            <tr key={user.username}>
                                <td>{user.username}</td>
                                <td>{user.address}</td>
                                <td>{user.roles.map(role => role.rolename).join(', ')}</td>
                                <td>
                                    <Button variant="primary" onClick={() => handleUpdate(user)}>Update</Button>
                                </td>
                                <td>
                                    <Button variant="danger" onClick={() => handleDelete(user.username)}>Delete</Button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>

                <div className="d-flex justify-content-center">
                    <Pagination>
                        {Array.from({ length: totalPages }, (_, index) => index + 1).map((page) => (
                            <Pagination.Item
                                key={page}
                                active={page === currentPage}
                                onClick={() => setCurrentPage(page)}
                            >
                                {page}
                            </Pagination.Item>
                        ))}
                    </Pagination>
                </div>
            </Col>
        </Row>
    );
}
export default UserListPage;