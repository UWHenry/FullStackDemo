import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Table, FormControl, Pagination, Button } from 'react-bootstrap'
import axiosInstance from '../../utils/axiosInstance';


function RoleListPage({ isLoggedIn }) {
    const navigate = useNavigate();
    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/login', { replace: true });
        }
    }, [isLoggedIn, navigate]);

    const [roles, setRoles] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortBy, setSortBy] = useState('rolename');
    const [sortReverse, setSortReverse] = useState(false)
    const pageSize = 10;

    const fetchRoles = async () => {
        try {
            const response = await axiosInstance.post(`/api/roles/search`, {
                "page": currentPage,
                "page_size": pageSize,
                "sort_by": sortBy,
                "reverse": sortReverse,
                "search_rolename": searchTerm
            });
            setRoles(response.data.roles ?? []);
            setTotalPages(response.data.total_pages);
        } catch (error) {
            console.error('Error fetching roles:', error);
        }
    };
    useEffect(() => {
        if (isLoggedIn) {
            fetchRoles();
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

    const handleDelete = async (rolename) => {
        try {
            await axiosInstance.delete(`/api/role/${rolename}`);
            fetchRoles();
        } catch (error) {
            console.error('Error deleting roles:', error);
        }
    };

    const handleUpdate = async (role) => {
        navigate('/role/edit', { state: { role, isLoggedIn } });
    };
    return (
        !isLoggedIn ?
        null :
        <Row className="justify-content-center mt-5">
            <Col xs={12} md={12}>
                <h1 style={{ textAlign: 'center' }}>Roles</h1>
                <Button variant="primary" type="button" className="mt-3" onClick={() => handleUpdate({})}>
                    Create Role
                </Button>
                <FormControl type="text" value={searchTerm} onChange={handleSearch} placeholder="Search roles" />

                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th onClick={() => handleSort('rolename')}>Rolename</th>
                            <th onClick={() => handleSort('permission')}>Permission</th>
                            <th onClick={() => handleSort('description')}>Description</th>
                            <th onClick={() => handleSort('users')}>Users</th>
                            <th>Update</th>
                            <th>Delete</th>
                        </tr>
                    </thead>

                    <tbody>
                        {roles.map((role) => (
                            <tr key={role.rolename}>
                                <td>{role.rolename}</td>
                                <td>{role.permission}</td>
                                <td>{role.description}</td>
                                <td>{role.users.map(user => user.username).join(', ')}</td>
                                <td>
                                    <Button variant="primary" onClick={() => handleUpdate(role)}>Update</Button>
                                </td>
                                <td>
                                    <Button variant="danger" onClick={() => handleDelete(role.rolename)}>Delete</Button>
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
export default RoleListPage;