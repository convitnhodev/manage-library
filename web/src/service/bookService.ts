import { IBook } from '@/store/bookStore';
import http from './httpService';

class BookService {
  public async getAll(): Promise<any> {
    const response = await http.get('books');
    return response.data;
  }

  public async createNewBook(book: IBook): Promise<any> {
    const { id, ...data } = book;
    const payload = {
      detail_adding_book: [
        {
          book_name: data.name,
          category: data.category,
          author: data.author,
          year_of_publication: data.publicCationYear,
          publisher: data.publisher,
          numbers: data.numberOfCopies,
        },
      ],
    };
    const response = await http.post('books/', payload);
    return response.data;
  }

  public async updateBook(book: IBook): Promise<any> {
    const { id, ...data } = book;
    const payload = {
      book_name: data.name,
      category: data.category,
      author: data.author,
      year_of_publication: data.publicCationYear,
      publisher: data.publisher,
      numbers: data.numberOfCopies,
    };
    const response = await http.put(`books/${id}`, payload);
    return response.data;
  }

  public async deleteBook(id: number): Promise<any> {
    const response = await http.delete(`books/${id}`);
    return response.data;
  }
}

export default new BookService();
