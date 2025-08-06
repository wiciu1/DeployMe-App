package dev.deployme.DeployMe.scraperclient;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Optional;

@Service
public class ScraperServiceClient {

    private final RestTemplate restTemplate;
    private final String scraperServiceUrl;

    public ScraperServiceClient(
            @Value("${scraper.service.url}") String scraperServiceUrl,
            RestTemplateBuilder restTemplateBuilder
    ) {
        this.scraperServiceUrl = scraperServiceUrl;
        this.restTemplate = restTemplateBuilder.build();
    }

    public List<JobOfferDto> getOffers(int max) {
        // Build url
        String url = String.format("%s/offers?max_offers=%d",
                scraperServiceUrl,
                max
        );

        // Send request (GET)
        ResponseEntity<List<JobOfferDto>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null, // GET is without body
                new ParameterizedTypeReference<>() {}
        );

        return response.getBody();
    }
}
