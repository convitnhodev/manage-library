class ReportService {
  public async getReportData(): Promise<any> {
    const response = await fetch('../src/service/dataReport.json');
    const data = await response.json();
    return data;
  }
}

export default new ReportService();
