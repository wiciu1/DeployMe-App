package dev.deployme.DeployMe.offers;

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
}
