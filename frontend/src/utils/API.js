import axios from 'axios'

export default axios.create({
    baseurl: 'http://165.22.177.130:5000',
    responseType: 'json'
})