import axios from 'axios';

export default () => {
    if (import.meta.env.PROD) {
        return axios.create({
            baseURL: 'https://api.aranroig.com/',
            headers: {
                "Access-Control-Allow-Origin": "*"
            }
        });
    } else {
        return axios.create({
            baseURL: 'http://localhost:3001/',
            headers: {
                "Access-Control-Allow-Origin": "*"
            }
        });
    }
}