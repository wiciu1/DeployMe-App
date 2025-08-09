package dev.deployme.DeployMe.joboffers.offers.filters;


import lombok.*;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Data
public class OfferFilterDto {

    private List<String> location;
    private List<String> experience;
    private List<String> skill;
}
