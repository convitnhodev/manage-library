import dayjs from 'dayjs';
import { observable, action } from 'mobx';
import { IBook } from './bookStore';
import loanSlipService from '@/service/loanSlipService';

export interface IBooksLoan {
  id: number;
  bookTitle: string;
  borrower: string;
  returnDate: dayjs.Dayjs;
}

export interface ILoanSlip {
  id: number;
  borrower: string;
  borrowerId: number;
  books: IBook[];
  borrowDate: dayjs.Dayjs;
}

class LoanSlipStore {
  @observable booksLoan: IBooksLoan[] = [];
  @observable loanSlips: ILoanSlip[] = [];

  @action getAll = async () => {
    try {
      const result = await loanSlipService.getLoanSlips();
      this.loanSlips = result.loanSlips;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  @action getBooksLoan = async () => {
    try {
      const result = await loanSlipService.getBooksLoan();
      this.booksLoan = result.booksLoan;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
}

export default LoanSlipStore;
