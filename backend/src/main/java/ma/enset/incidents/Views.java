package ma.enset.incidents;
import java.time.Instant;
public class Views {
 public record User(Long id,String fullName,String email,Role role,boolean enabled,Instant createdAt) {}
 public record IncidentView(Long id,String title,String description,Category category,Priority priority,Status status,Instant createdAt,Instant updatedAt,User createdBy,User assignedTo) {}
 public record Event(Long id,String event,String author,Instant createdAt) {}
 public record Comment(Long id,String content,String author,Instant createdAt) {}
 public static User user(AppUser u) { return new User(u.getId(),u.getFullName(),u.getEmail(),u.getRole(),u.isEnabled(),u.getCreatedAt()); }
 public static IncidentView incident(Incident i) { return new IncidentView(i.id,i.title,i.description,i.category,i.priority,i.status,i.createdAt,i.updatedAt,user(i.createdBy),i.assignedTo==null?null:user(i.assignedTo)); }
}
