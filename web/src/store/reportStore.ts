import reportService from '@/service/reportService';
import { observable, action } from 'mobx';

export interface IReportData {
  visitors: number;
  borrowed: number;
  returned: number;
  newMembers: number;
}

export interface IChartData {
  visitors: number[];
  borrowers: number[];
}

class ReportStore {
  @observable dataReport: IReportData = {} as IReportData;
  @observable dataChart: IChartData = {} as IChartData;

  @action getData = async () => {
    try {
      const result = await reportService.getReportData();
      this.dataReport = result.dataReport;
      this.dataChart = result.dataChart;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
}

export default ReportStore;
