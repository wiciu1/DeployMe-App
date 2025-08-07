import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Offer } from '../../models/offer';
import { OfferService } from '../../services/offer.service';
import { OfferCardComponent } from '../../components/offer-card.component/offer-card.component';
import {MatPaginatorModule, PageEvent} from '@angular/material/paginator';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  standalone: true,
  selector: 'app-offer',
  imports: [CommonModule, OfferCardComponent, MatPaginatorModule, MatButtonModule, MatProgressSpinnerModule],
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
    this.offerService.getOffers(this.currentPage, this.pageSize)
      .subscribe({
        next: (response) => {
          this.offers = response.content;
          this.totalItems = response.totalElements;
          this.offersLoading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('Error loading offers:', err);
          this.offersLoading = false;
        }
      });
  }

  onPageChange(event: PageEvent) {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadOffers();

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

}