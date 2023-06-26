class LoanSlipService {
  public async getLoanSlips(): Promise<any> {
    const response = await fetch('../src/service/loanSlips.json');
    const data = await response.json();
    return data;
  }

  public async getBooksLoan(): Promise<any> {
    const response = await fetch('../src/service/booksLoanData.json');
    const data = await response.json();
    return data;
  }
}

export default new LoanSlipService();
