import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Offer } from '../../models/offer';
import { OfferService } from '../../services/offer.service';
import { OfferCardComponent } from '../../components/offer-card.component/offer-card.component';
import {MatPaginatorModule, PageEvent} from '@angular/material/paginator';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FilterComponent } from '../../components/filter.component/filter.component';

@Component({
  standalone: true,
  selector: 'app-offer',
  imports: [CommonModule, OfferCardComponent, MatPaginatorModule, MatButtonModule, MatProgressSpinnerModule, FilterComponent],
  templateUrl: './offer.component.html',
  styleUrl: './offer.component.scss'
})
export class OfferComponent implements OnInit {
  
  offers: Offer[] = [];
  
  // Pagination features:
  totalItems = 0;
  currentPage = 0;
  pageSize = 10;
  pageSizeOptions = [5, 10, 15];

  // Filtering
  currentFilters: any = {};

  // Loading and errors
  offersLoading = false;
  error: string | null = null;

  // Injections
  private offerService = inject(OfferService);
  private cdr = inject(ChangeDetectorRef)

  ngOnInit(): void {
    this.loadOffers();
  }

  loadOffers() {
  this.offersLoading = true;
  this.error = null;

  // Wybieramy odpowiednią metodę w zależności od filtrów
  const observable = Object.keys(this.currentFilters).length > 0
    ? this.offerService.getFilteredOffers(this.currentFilters, this.currentPage, this.pageSize)
    : this.offerService.getOffers(this.currentPage, this.pageSize);

  observable.subscribe({
    next: (response) => {
      this.offers = response.content;
      this.totalItems = response.totalElements;
      this.offersLoading = false;
      this.cdr.detectChanges();
    },
    error: (err) => {
      console.error('Error loading offers:', err);
      this.error = 'Wystąpił błąd podczas ładowania ofert';
      this.offersLoading = false;
      this.cdr.detectChanges();
    }
  });
}
  onPageChange(event: PageEvent) {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadOffers();

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Filters
  onFiltersChanged(filters: any) {
    this.currentFilters = filters;
    this.currentPage = 0; 
    this.loadOffers();
  }

    nextPage() {
    this.currentPage++;
    this.loadOffers();
  }

  prevPage() {
    if (this.currentPage > 0) {
      this.currentPage--;
      this.loadOffers();
    }
  }


}