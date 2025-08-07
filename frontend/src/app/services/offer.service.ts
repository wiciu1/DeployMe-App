import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Offer } from '../models/offer';

interface PaginatedResponse<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  number: number;
  size: number;
}


@Injectable({
  providedIn: 'root'
})
export class OfferService {

    // URL to GET offers from DB, temporarily localhost
    private apiUrl = 'http://localhost:8080/api/v1/offers';
    
    private http = inject(HttpClient);


    // Sends GET request to backend ( gets offers existing in DB )
    getOffers(page: number = 0, perPage: number = 15) : Observable<PaginatedResponse<Offer>> {

      const params = new HttpParams()
        .set('page', page.toString())
        .set('perPage', perPage.toString())

      return this.http.get<PaginatedResponse<Offer>>(this.apiUrl, { params });
    }

    // Sends POST request to backend ( scrape data )
    syncOffers(max: number): Observable<string> {
      return this.http.post<string>(`${this.apiUrl}/sync?max=${max}`, {});
    }   

}
