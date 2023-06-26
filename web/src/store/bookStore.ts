import bookService from '@/service/bookService';
import dayjs from 'dayjs';
import { observable, action } from 'mobx';

export interface IBook {
  id: number;
  name: string;
  category: string;
  author: string;
  numberOfCopies: number;
  numberOfBorrowedCopies?: number;
  publicCationYear: number;
  publisher: string;
  importDate: dayjs.Dayjs;
}

class BookStore {
  @observable booksData: IBook[] = [];

  @action getAll = async () => {
    try {
      const result = await bookService.getAll();
      const data = result.data;
      this.booksData = data.map((book: any) => {
        return {
          id: book.id,
          name: book.book_name,
          category: book.category,
          author: book.author,
          numberOfCopies: book.numbers,
          numberOfBorrowedCopies: book.amount_borrowed,
          publicCationYear: book.year_of_publication,
          publisher: book.publisher,
          importDate: dayjs(book.created_at),
        };
      });
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  @action createNewBook = async (book: IBook) => {
    try {
      const result = await bookService.createNewBook(book);
      const data: IBook = {
        id: result[0].id,
        name: result[0].book_name,
        category: result[0].category,
        author: result[0].author,
        numberOfCopies: result[0].numbers,
        numberOfBorrowedCopies: result[0].amount_borrowed,
        publicCationYear: result[0].year_of_publication,
        publisher: result[0].publisher,
        importDate: dayjs(result[0].created_at),
      };
      return data;
    } catch (error) {
      console.error('Error creating new member:', error);
    }
  };

  @action updateBook = async (book: IBook) => {
    try {
      const result = await bookService.updateBook(book);
      console.log(result);
      const data: IBook = {
        id: result.id,
        name: result.book_name,
        category: result.category,
        author: result.author,
        numberOfCopies: result.numbers,
        numberOfBorrowedCopies: result.amount_borrowed,
        publicCationYear: result.year_of_publication,
        publisher: result.publisher,
        importDate: dayjs(result.created_at),
      };
      return data;
    } catch (error) {
      console.error('Error updating member:', error);
    }
  };

  @action deleteBook = async (id: number) => {
    try {
      const result = await bookService.deleteBook(id);
      return result;
    } catch (error) {
      console.error('Error deleting member:', error);
    }
  };
}

export default BookStore;
