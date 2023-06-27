import http from './httpService';
export interface IUserLogin {
  username: string;
  password: string;
}

class AuthService {
  public async login(payload: IUserLogin): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('username', payload.username);
      formData.append('password', payload.password);

      const response = await http.post('login/token', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      // Handle error
      console.error(error);
      throw error;
    }
  }

  public async signup(): Promise<any> {
    return;
  }
}

export default new AuthService();
