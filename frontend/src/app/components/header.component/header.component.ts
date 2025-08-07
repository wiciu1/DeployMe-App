import { Component, inject } from '@angular/core';
import { OfferService } from '../../services/offer.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  private offerService = inject(OfferService);
  private router = inject(Router);

  isMenuOpen = false;

  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen
    // Block scroll
    document.body.style.overflow = this.isMenuOpen ? 'hidden' : '';
  }

  closeMenu(): void {
    this.isMenuOpen = false;
    document.body.style.overflow = '';
  }

  syncOffers(max: number = 50): void {
    this.offerService.syncOffers(max).subscribe({
      next: () => {
        this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
          this.router.navigate(['/offers']);
        });
      },
      error: (err) => {
        console.error('Błąd synchronizacji:', err);
      }
    });
  }
}