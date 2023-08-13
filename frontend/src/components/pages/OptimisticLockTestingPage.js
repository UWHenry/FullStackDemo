import axiosInstance from "../../utils/axiosInstance";
import { Row, Col, Table } from "react-bootstrap";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router";

function OptimisticLockTestingPage({ isLoggedIn }) {
    const navigate = useNavigate();
    const [testResult, setTestResult] = useState([]);

    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/login');
        } else {
            axiosInstance.get('/api/test_optimistic_lock')
                .then((response) => {
                    setTestResult(response.data ?? [])
                })
        }
    }, [isLoggedIn, navigate]);

    return (
        !isLoggedIn ?
        null :
        <Row className="justify-content-center mt-5">
            <Col xs={12} md={6}>
                <h1>Optimistic Lock Testing</h1>
                <p>The backend creates 10 processes, where each process tries to update the role "optimistic_lock_test".</p>
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Process ID</th>
                            <th>Update Result</th>
                        </tr>
                    </thead>

                    <tbody>
                        {testResult.map((result) => (
                            <tr key={result.process_id}>
                                <td>{result.process_id}</td>
                                <td>{result.update_result}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </Col>
        </Row>
    )
}

export default OptimisticLockTestingPage;