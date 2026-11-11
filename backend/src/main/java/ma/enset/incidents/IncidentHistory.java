package ma.enset.incidents;
import jakarta.persistence.*;
import java.time.Instant;
@Entity
public class IncidentHistory {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) public Long id;
 @ManyToOne(fetch=FetchType.LAZY,optional=false) public Incident incident;
 @ManyToOne(fetch=FetchType.LAZY,optional=false) public AppUser author;
 @Column(nullable=false,length=5000) public String event;
 public Instant createdAt=Instant.now();
}
