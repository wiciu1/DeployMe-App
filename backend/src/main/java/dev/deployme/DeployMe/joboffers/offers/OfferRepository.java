package dev.deployme.DeployMe.joboffers.offers;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface OfferRepository extends
        JpaRepository<JobOffer, Long>,
        JpaSpecificationExecutor<JobOffer> {


    boolean existsByUrl(String url);
}
