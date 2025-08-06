package dev.deployme.DeployMe.scraperclient;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public record JobOfferDto(
        String site,
        String url,
        String title,
        String company,
        String location,
        String experience,
        String salary,
        @JsonProperty("datePosted") String datePosted,
        @JsonProperty("validThrough") String validThrough,
        List<String> skills
) {}