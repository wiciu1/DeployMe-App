import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Offer } from '../../models/offer';
import { OfferService } from '../../services/offer.service';

@Component({
  standalone: true,
  selector: 'app-offer',
  imports: [CommonModule],
  templateUrl: './offer.component.html',
  styleUrl: './offer.component.scss'
})
export class OfferComponent implements OnInit {
  offers: Offer[] = [];

  offersLoading = false;

  error: string | null = null;

  private offerService = inject(OfferService);

  ngOnInit(): void {
    this.loadOffers();
  }

  constructor(private cdr: ChangeDetectorRef) {}

  loadOffers(): void {
  this.offerService.getOffers().subscribe({
    next: (data) => {
      this.offersLoading = true;
      this.offers = data;
      this.cdr.detectChanges();
    },
    error: (error) => {
      this.error = 'Nie udało się pobrać ofert.'
      this.offersLoading = false;
    }
  });
}

  syncOffers(max: number = 50): void {
    this.offerService.syncOffers(max).subscribe({
      next: () => {
        this.loadOffers();
      },
      error: (err) => {
        this.error = 'Błąd synchronizacji';
      }
    });
  }
}