import http from './httpService';

class LoanSlipService {
  public async getLoanSlips(): Promise<any> {
    const response = await http.get('/library-loan-form');
    return response.data;
  }

  public async createLoanSlip(loanSlip: any): Promise<any> {
    const response = await http.post('/library-loan-form', loanSlip);
    return response.data;
  }

  public async getBooksLoan(): Promise<any> {
    const response = await fetch('../src/service/booksLoanData.json');
    const data = await response.json();
    return data;
  }

  public async deleteLoanSlip(id: number): Promise<any> {
    const response = await http.delete(`/library-loan-form/${id}`);
    return response.data;
  }
}

export default new LoanSlipService();
