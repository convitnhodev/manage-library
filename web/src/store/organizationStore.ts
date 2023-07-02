import organizationService from '@/service/organizationService';
import dayjs from 'dayjs';
import { observable, action } from 'mobx';

export interface IUser {
  id: number;
  name: string;
  username: string;
  dob: dayjs.Dayjs;
  address: string;
  email: string;
  numberphone: string;
}

class OrganizationStore {
  @observable organizationData: IUser[] = [];

  @action getAllUser = async () => {
    try {
      const result = await organizationService.getAllUser();
      this.organizationData = result;
    } catch (error) {
      console.error('Error fetching organization:', error);
    }
  };

  @action createUser = async (user: IUser) => {
    try {
      const result = await organizationService.createUser(user);
      this.organizationData.push(result);
      return result;
    } catch (error) {
      console.error('Error creating new organization:', error);
    }
  };

  @action deleteUser = async (id: number) => {
    try {
      const result = await organizationService.deleteUser(id);
      return result;
    } catch (error) {
      console.error('Error deleting organization:', error);
    }
  };
}

export default OrganizationStore;
