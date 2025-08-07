import { Routes } from '@angular/router';
    
export const routes: Routes = [
    {
        path: '',
        loadComponent: () => 
            import('./pages/offer.component/offer.component').then((m) => m.OfferComponent),
    },
];
