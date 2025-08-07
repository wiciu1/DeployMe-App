import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Offer } from '../models/offer';

@Injectable({
  providedIn: 'root'
})
export class OfferService {

    // URL to GET offers from DB, temporarily localhost
    private apiUrl = 'http://localhost:8080/api/v1/offers';
    
    private http = inject(HttpClient);


    // Sends GET request to backend ( gets offers existing in DB )
    getOffers(): Observable<Offer[]> {
      return this.http.get<Offer[]>(this.apiUrl);
    }

    // Sends POST request to backend ( scrape data )
    syncOffers(max: number): Observable<string> {
      return this.http.post<string>(`${this.apiUrl}/sync?max=${max}`, {});
    }   

}
