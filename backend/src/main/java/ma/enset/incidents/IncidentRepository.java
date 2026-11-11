package ma.enset.incidents;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
public interface IncidentRepository extends JpaRepository<Incident,Long> {
 List<Incident> findByCreatedByIdOrderByCreatedAtDesc(Long id);
 List<Incident> findByAssignedToIdOrderByCreatedAtDesc(Long id);
 List<Incident> findAllByOrderByCreatedAtDesc();
}
