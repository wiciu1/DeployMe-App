package dev.deployme.DeployMe.joboffers.offers;

import dev.deployme.DeployMe.joboffers.offersync.OfferSyncService;
import lombok.RequiredArgsConstructor;
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

    // Gets all offers from database
    @GetMapping
    public ResponseEntity<List<JobOffer>> getOffers() {
        return ResponseEntity.ok(offerService.getOffers());
    }

    @PostMapping("/sync")
    public ResponseEntity<String> syncOffers(
            @RequestParam(defaultValue = "50") int max
    ) {
        int addedOffers = offerSyncService.syncOffers(max);
        return ResponseEntity.ok(addedOffers + " offers added");
    }
}
