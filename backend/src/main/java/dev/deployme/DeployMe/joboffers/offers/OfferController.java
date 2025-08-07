package dev.deployme.DeployMe.joboffers.offers;

import dev.deployme.DeployMe.joboffers.offersync.OfferSyncService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/offers")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:4200", allowedHeaders = "*", methods = {RequestMethod.GET, RequestMethod.POST})
public class OfferController {

    // Responsible for posting data to database
    // and communicating with FastAPI microservice
    private final OfferSyncService offerSyncService;

    // Responsible for getting data from database
    private final OfferService offerService;

    private final int perPage = 10;

    // Gets all offers from database
    @GetMapping
    public ResponseEntity<Page<JobOffer>> getOffers(
            @RequestParam(defaultValue = "0" ) int page
    ) {
        Pageable pageable = PageRequest.of(page, perPage);
        Page<JobOffer> offers = offerService.getOffers(pageable);

        return ResponseEntity.ok(offers);
    }

    @PostMapping("/sync")
    public ResponseEntity<String> syncOffers(
            @RequestParam(defaultValue = "50") int max
    ) {
        int addedOffers = offerSyncService.syncOffers(max);
        return ResponseEntity.ok(addedOffers + " offers added");
    }
}
