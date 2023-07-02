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
  borrowerId: number;
  books: number[];
  borrowDate: dayjs.Dayjs;
}

class LoanSlipStore {
  @observable booksLoan: IBooksLoan[] = [];
  @observable loanSlips: ILoanSlip[] = [];

  @action getAll = async () => {
    try {
      const result = await loanSlipService.getLoanSlips();
      const data: ILoanSlip[] = result.map((item: any) => {
        return {
          id: item.id,
          borrowerId: item.id_card,
          books: item.ids_books,
          borrowDate: dayjs(item.created_at),
        };
      });
      this.loanSlips = data;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  @action createLoanSlip = async (loanSlip: ILoanSlip) => {
    try {
      const result = await loanSlipService.createLoanSlip(loanSlip);
      if (result === 433) {
        return result;
      }
      const data = {
        id: result.id,
        borrowerId: result.id_card,
        books: result.ids_books,
        borrowDate: dayjs(result.created_at),
      };
      this.loanSlips.push(data);
      return result;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  @action deleteLoanSlip = async (id: number) => {
    try {
      const result = await loanSlipService.deleteLoanSlip(id);
      this.loanSlips = this.loanSlips.filter(item => item.id !== id);
      return result;
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
