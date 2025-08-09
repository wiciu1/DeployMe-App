package dev.deployme.DeployMe.joboffers.offers;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.util.List;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "job_offers")
public class JobOffer {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String site;
    private String url;
    private String title;
    private String company;
    private String location;
    private String experience;
    private String salary;

    @Column(name = "date_posted")
    private LocalDate datePosted;

    @Column(name = "valid_through")
    private LocalDate validThrough;

    @ElementCollection
    @CollectionTable(
            name = "job_offer_skills",
            joinColumns = @JoinColumn(name = "job_offer_id")
    )
    @Column(name = "skill")
    private List<String> skills;

    public JobOffer(String site, String url, String title, String company,
                    String location, String experience, String salary, LocalDate datePosted,
                    LocalDate validThrough, List<String> skills) {
        this.site = site;
        this.url = url;
        this.title = title;
        this.company = company;
        this.location = location;
        this.experience = experience;
        this.salary = salary;
        this.datePosted = datePosted;
        this.validThrough = validThrough;
        this.skills = skills;
    }

    // Parsing minSalary (for filtering)
    @Transient
    public Integer getParsedMaxSalary() {
        if (salary == null || salary.isEmpty()) {
            return null;
        }
        try {
            // Format XXXX-YYYY PLN
            if (salary.matches(".*\\d[ \\d]*-[ \\d]*\\d.*")) {
                String normalized = salary.replaceAll("[^0-9-]", "");
                String[] parts = normalized.split("-");

                if (parts.length >= 2) {
                    String maxPart = parts[1].replaceAll("[^0-9]", "");
                    return Integer.parseInt(maxPart);
                }
            }

            // Format "XXX PLN/Hour"
            if (salary.matches(".*\\d+.*PLN/Hour.*")) {
                String numStr = salary.replaceAll("[^0-9]", "");
                int hourlyRate = Integer.parseInt(numStr);
                return hourlyRate * 160; // Assuming its full-time job (+- 160h)
            }

            // 3. Format "XXX PLN/Month"
            if (salary.matches(".*\\d+.*PLN/Month.*")) {
                String numStr = salary.replaceAll("[^0-9]", "");
                return Integer.parseInt(numStr);
            }
        } catch (NumberFormatException e) {
            return -1;
        }
    return -1;
    }
}
