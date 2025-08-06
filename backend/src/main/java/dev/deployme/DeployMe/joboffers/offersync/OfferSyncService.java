package dev.deployme.DeployMe.joboffers.offersync;

import dev.deployme.DeployMe.joboffers.offers.JobOffer;
import dev.deployme.DeployMe.joboffers.offers.OfferService;
import dev.deployme.DeployMe.joboffers.scraperclient.JobOfferDto;
import dev.deployme.DeployMe.joboffers.scraperclient.ScraperServiceClient;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

//Layer to synchronize getting data from FastAPI scraper and saving to database

@Service
@RequiredArgsConstructor
public class OfferSyncService {

    private final OfferService offerService;
    private final ScraperServiceClient scraperServiceClient;

    public int syncOffers(int maxOffers) {
        List<JobOfferDto> scrapedOffers = scraperServiceClient.getOffers(maxOffers);

        // save those not in DB already
        List<JobOffer> newOffers = scrapedOffers.stream()
                .map(this::mapToEntity)
                .filter(offer -> !offerService.existsByUrl(offer.getUrl()))
                .toList();

        offerService.saveAll(newOffers);

        return newOffers.size();
    }

    // DTO -> JobOffer Entity
    private JobOffer mapToEntity(JobOfferDto dto) {
        return new JobOffer(
                dto.site(),
                dto.url(),
                dto.title(),
                dto.company(),
                dto.location(),
                dto.experience(),
                dto.salary(),
                dto.datePosted(),
                dto.validThrough(),
                dto.skills()
        );
    }


}
