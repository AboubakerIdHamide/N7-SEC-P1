package ma.enset.incidents;
import jakarta.persistence.*;
import java.time.Instant;
@Entity
public class Incident {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) public Long id;
 @Column(nullable=false) public String title;
 @Column(nullable=false,length=5000) public String description;
 @Enumerated(EnumType.STRING) public Category category;
 @Enumerated(EnumType.STRING) public Priority priority;
 @Enumerated(EnumType.STRING) public Status status=Status.OPEN;
 public Instant createdAt=Instant.now();
 public Instant updatedAt=Instant.now();
 @ManyToOne(fetch=FetchType.LAZY,optional=false) public AppUser createdBy;
 @ManyToOne(fetch=FetchType.LAZY) public AppUser assignedTo;
}
enum Category { NETWORK, MALWARE, PHISHING, ACCESS, SOFTWARE, HARDWARE, DATA_LEAK, OTHER }
enum Priority { LOW, MEDIUM, HIGH, CRITICAL }
enum Status { OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED }
