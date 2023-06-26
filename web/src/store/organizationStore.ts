import organizationService from '@/service/organizationService';
import dayjs from 'dayjs';
import { observable, action } from 'mobx';

export interface IUser {
  id: number;
  name: string;
  username: string;
  birthday: dayjs.Dayjs;
  address: string;
  email: string;
  phone: string;
}

class OrganizationStore {
  @observable organizationData: IUser[] = [];

  @action getAllUser = async () => {
    try {
      const result = await organizationService.getAllUser();
      this.organizationData = result.organization;
    } catch (error) {
      console.error('Error fetching organization:', error);
    }
  };
}

export default OrganizationStore;
