package dev.deployme.DeployMe.joboffers.scraperclient;

import java.time.LocalDate;
import java.util.List;

public record JobOfferDto(
        String site,
        String url,
        String title,
        String company,
        String location,
        String experience,
        String salary,
        LocalDate datePosted,
        LocalDate validThrough,
        List<String> skills
) {}