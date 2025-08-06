package dev.deployme.DeployMe.joboffers.scraperclient;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/scrape")
@RequiredArgsConstructor
public class ScraperController {

    private final ScraperServiceClient scraperServiceClient;

    @GetMapping
    public ResponseEntity<List<JobOfferDto>> getScrapedOffers(
            @RequestParam(defaultValue = "50") int max
    ) {
        return ResponseEntity.ok(scraperServiceClient.getOffers(max));
    }
}
