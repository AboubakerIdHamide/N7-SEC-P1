package ma.enset.incidents;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.util.*;
@RestController @RequestMapping("/api/admin") @PreAuthorize("hasRole('ADMIN')") @Transactional
public class AdminController {
 private final IncidentService s;public AdminController(IncidentService s){this.s=s;}
 @GetMapping("/users") public List<Views.User> users(){return s.users().findAll().stream().map(Views::user).toList();}
 @PutMapping("/users/{id}/enable") public Views.User enable(@PathVariable Long id){return enabled(id,true);}
 @PutMapping("/users/{id}/disable") public Views.User disable(@PathVariable Long id){return enabled(id,false);}
 private Views.User enabled(Long id,boolean enabled){AppUser u=s.users().findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"User not found"));u.enabled=enabled;return Views.user(u);}
 @GetMapping("/statistics") public Map<String,Long> statistics(){List<AppUser> users=s.users().findAll();List<Incident> incidents=s.incidents().findAll();Map<String,Long> m=new LinkedHashMap<>();m.put("users",(long)users.size());m.put("employees",users.stream().filter(u->u.role==Role.EMPLOYEE).count());m.put("technicians",users.stream().filter(u->u.role==Role.TECHNICIAN).count());m.put("incidents",(long)incidents.size());for(Status status:Status.values())m.put(status.name(),incidents.stream().filter(i->i.status==status).count());return m;}
}
