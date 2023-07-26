import axios from "axios";

const getCsrfToken = async () => {
    let response = await axios.get('https://localhost:8000/api/get_csrf_token')
    return response.data.csrf_token
};
  
export default getCsrfToken;