import { URL_API, URL_APP } from '@/util/constants';
import { notification } from 'antd';
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

// Add an error interceptor to display an alert with the error message
http.interceptors.response.use(
  response => response,
  error => {
    if (error.response.status === 404) {
      notification.destroy('authen');
      notification.error({
        key: 'authen',
        message: 'Không có quyền',
        description:
          'Bạn không có quyền truy cập tài nguyên này!\n Hãy liên hệ với quản trị viên để được cấp quyền truy cập!',
        duration: 5,
      });
    } else {
      notification.destroy('errorGeneric');
      notification.error({
        key: 'errorGeneric',
        message: 'Lỗi hệ thống',
        description: 'Hệ thống đang gặp sự cố, vui lòng thử lại sau!',
        duration: 5,
      });
    }
    return Promise.reject(error);
  },
);

export default http;
