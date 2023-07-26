import axiosInstance from "../utils/axiosInstance";
import { Container, Row, Col, Table } from "react-bootstrap";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router";

function OptimisticLockTestingPage({ isLoggedIn }) {
    const navigate = useNavigate();
    const [testResult, setTestResult] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/login');
        } else {
            axiosInstance.get('/db_testing/test_optimistic_lock')
                .then((response) => {
                    setTestResult(response.data ?? [])
                })
                .catch((error) => {
                    let errMessage = error.response.data?.message;
                    if  (errMessage) {
                        setErrorMessage(errMessage)
                    }
                    console.error('POST request failed:', error);
                });
        }
    }, [isLoggedIn, navigate]);

    return (
        <Container>
            <Row className="justify-content-center mt-5">
                <Col xs={12} md={6}>
                    <h1>Optimistic Lock Testing</h1>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>Process Index</th>
                                <th>Update Result</th>
                            </tr>
                        </thead>

                        <tbody>
                            {testResult.map((result) => (
                                <tr key={result.proccess_index}>
                                    <td>{result.proccess_index}</td>
                                    <td>{result.update_result}</td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>

                    <div>
                        <p className="mt-3">{errorMessage}</p>
                    </div>
                </Col>
            </Row>
        </Container>
    )

}

export default OptimisticLockTestingPage;