package ma.enset.incidents;
import jakarta.persistence.*;
import java.time.Instant;
@lombok.Getter
@Entity @Table(name="app_users")
public class AppUser {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) public Long id;
 @Column(nullable=false) public String fullName;
 @Column(nullable=false,unique=true) public String email;
 @Column(nullable=false) public String password;
 @Enumerated(EnumType.STRING) @Column(nullable=false) public Role role=Role.EMPLOYEE;
 public boolean enabled=true;
 public Instant createdAt=Instant.now();
}
enum Role { EMPLOYEE, TECHNICIAN, ADMIN }
