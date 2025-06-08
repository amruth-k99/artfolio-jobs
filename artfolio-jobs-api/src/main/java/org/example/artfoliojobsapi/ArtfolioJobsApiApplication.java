package org.example.artfoliojobsapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;

@SpringBootApplication
public class ArtfolioJobsApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(ArtfolioJobsApiApplication.class, args);
    }

    @GetMapping("/health")
    public String serverHealthCheck() {
        return String.format("%s is up and running", this.getClass().getSimpleName());
    }

}
