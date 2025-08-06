package dev.deployme.DeployMe.joboffers.offers;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class OfferService {

    private final OfferRepository offerRepository;

    public List<JobOffer> getOffers() {
        return offerRepository.findAll();
    }

    public boolean existsByUrl(String url) {
        return offerRepository.existsByUrl(url);
    }

    public void saveAll(List<JobOffer> offers) {
        offerRepository.saveAll(offers);
    }
}
