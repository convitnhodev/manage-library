import { URL_API, URL_APP } from '@/util/constants';
import axios from 'axios';
import qs from 'qs';

const http = axios.create({
  baseURL: URL_API,
  timeout: 99999,
  paramsSerializer: function (params) {
    return qs.stringify(params, {
      encode: false,
    });
  },
});

// Add an interceptor to include the Access-Control-Allow-Origin header
http.interceptors.request.use(config => {
  // Retrieve the _auth cookie value
  const authCookie = document.cookie.match('(^|;)\\s*_auth\\s*=\\s*([^;]+)');

  // Set the Authorization header if the _auth cookie exists
  if (authCookie) {
    config.headers['Authorization'] = `Bearer ${authCookie[2]}`;
  }

  return config;
});

export default http;
