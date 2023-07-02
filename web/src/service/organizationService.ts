import { IUser } from '@/store/organizationStore';
import http from './httpService';

class Organization {
  public async getAllUser(): Promise<any> {
    try {
      const response = await http.get('/user/admin/users');
      return response.data;
    } catch (error) {
      return error;
    }
  }

  public async createUser(user: IUser): Promise<any> {
    const response = await http.post('/user/registration', user);
    return response.data;
  }

  public async deleteUser(id: number): Promise<any> {
    const response = await http.delete(`/user/admin/users/${id}`);
    return response.data;
  }
}

export default new Organization();
