package ma.enset.incidents;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.http.HttpStatus;
import jakarta.validation.Valid;
import java.util.*;
@RestController @RequestMapping("/api/incidents") @Transactional
public class IncidentController {
 private final IncidentService s;public IncidentController(IncidentService s){this.s=s;}
 @PostMapping @PreAuthorize("hasRole('EMPLOYEE')") @ResponseStatus(HttpStatus.CREATED) public Views.IncidentView create(@Valid @RequestBody Requests.NewIncident r,Authentication a){return s.create(r,s.current(a));}
 @GetMapping("/my") @PreAuthorize("hasRole('EMPLOYEE')") public List<Views.IncidentView> mine(Authentication a){return s.incidents().findByCreatedByIdOrderByCreatedAtDesc(s.current(a).id).stream().map(Views::incident).toList();}
 @GetMapping("/assigned") @PreAuthorize("hasRole('TECHNICIAN')") public List<Views.IncidentView> assigned(Authentication a){return s.incidents().findByAssignedToIdOrderByCreatedAtDesc(s.current(a).id).stream().map(Views::incident).toList();}
 @GetMapping @PreAuthorize("hasRole('ADMIN')") public List<Views.IncidentView> all(){return s.incidents().findAllByOrderByCreatedAtDesc().stream().map(Views::incident).toList();}
 @GetMapping("/{id}") public Map<String,Object> detail(@PathVariable Long id,Authentication a){return s.detail(id,s.current(a));}
 @PutMapping("/{id}/status") @PreAuthorize("hasAnyRole('TECHNICIAN','ADMIN')") public Views.IncidentView status(@PathVariable Long id,@Valid @RequestBody Requests.ChangeStatus r,Authentication a){return s.status(id,r.status(),s.current(a));}
 @PutMapping("/{id}/assign/{technicianId}") @PreAuthorize("hasRole('ADMIN')") public Views.IncidentView assign(@PathVariable Long id,@PathVariable Long technicianId,Authentication a){return s.assign(id,technicianId,s.current(a));}
 @PostMapping("/{id}/comments") @PreAuthorize("hasRole('TECHNICIAN')") @ResponseStatus(HttpStatus.CREATED) public Views.Comment note(@PathVariable Long id,@Valid @RequestBody Requests.Note r,Authentication a){return s.note(id,r.content(),s.current(a));}
}
