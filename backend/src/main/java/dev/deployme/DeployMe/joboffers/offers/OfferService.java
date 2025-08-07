package dev.deployme.DeployMe.joboffers.offers;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class OfferService {

    private final OfferRepository offerRepository;

    public Page<JobOffer> getOffers(Pageable pageable) {
        Page<JobOffer> offers = offerRepository.findAll(pageable);
        return offers.map(offer -> offer);
    }

    public boolean existsByUrl(String url) {
        return offerRepository.existsByUrl(url);
    }

    public void saveAll(List<JobOffer> offers) {
        offerRepository.saveAll(offers);
    }
}
