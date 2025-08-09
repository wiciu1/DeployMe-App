package dev.deployme.DeployMe.joboffers.offers;

import dev.deployme.DeployMe.joboffers.offers.filters.OfferFilterDto;
import jakarta.persistence.criteria.Predicate;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

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

    ///  ### FILTERING ###

    public Page<JobOffer> getFilteredOffers(OfferFilterDto filters, Pageable pageable) {
        Specification<JobOffer> spec = (root, query, cb) -> cb.conjunction();

        // Location filtering
        if (filters.getLocation() != null && !filters.getLocation().isEmpty()) {
                spec = spec.and((root, query, cb) -> {
                    List<Predicate> predicates = filters.getLocation().stream()
                            .map(location -> cb.like(cb.lower(root.get("location")), "%" +
                                    location.toLowerCase() + "%"))
                            .toList();
                    return cb.or(predicates.toArray(new Predicate[0]));
            });
        }

        // Experience levels filtering
        if (filters.getExperience() != null && !filters.getExperience().isEmpty()) {
            spec = spec.and((root, query, cb) ->
                    root.get("experience").in(filters.getExperience()));
        }

        // Skills filtering
        if (filters.getSkill() != null && !filters.getSkill().isEmpty()) {
            spec = spec.and((root, query, cb) -> {
                List<Predicate> predicates = filters.getSkill().stream()
                        .map(skill -> cb.isMember(skill, root.get("skills")))
                        .toList();
                return cb.and(predicates.toArray(new Predicate[0]));
            });
        }


        return offerRepository.findAll(spec, pageable);
    }


}
