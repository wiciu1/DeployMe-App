import { Component, Input, input } from '@angular/core';
import { OfferComponent } from '../../pages/offer.component/offer.component';
import { Offer } from '../../models/offer';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-offer-card',
  imports: [CommonModule],
  templateUrl: './offer-card.component.html',
  styleUrl: './offer-card.component.scss'
})
export class OfferCardComponent {
    @Input() offer!: Offer;

}
