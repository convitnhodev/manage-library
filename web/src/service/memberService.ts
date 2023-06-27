import { IMember } from '@/store/memberStore';
import http from './httpService';

class Members {
  public async getAll(): Promise<any> {
    const response = await http.get('card');
    return response.data;
  }

  public async createNewMember(member: IMember): Promise<any> {
    const { id, ...payload } = member;
    const response = await http.post('card', payload);
    return response.data;
  }

  public async updateMember(member: IMember): Promise<any> {
    const { id, ...payload } = member;
    const response = await http.put(`card/${id}`, payload);
    return response.data;
  }

  public async deleteMember(id: number): Promise<any> {
    const response = await http.delete(`card/${id}`);
    return response.data;
  }
}

export default new Members();
