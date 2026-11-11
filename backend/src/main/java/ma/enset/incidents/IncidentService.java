package ma.enset.incidents;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.security.core.Authentication;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.time.Instant;
import java.util.*;
@Service @Transactional
public class IncidentService {
 final UserRepository users; final IncidentRepository incidents;final IncidentHistoryRepository history;final IncidentCommentRepository comments;
 public IncidentService(UserRepository u,IncidentRepository i,IncidentHistoryRepository h,IncidentCommentRepository c){users=u;incidents=i;history=h;comments=c;}
 public UserRepository users(){return users;}
 public IncidentRepository incidents(){return incidents;}
 public AppUser current(Authentication a){return users.findByEmail(a.getName()).orElseThrow(()->new ResponseStatusException(HttpStatus.UNAUTHORIZED,"User not found"));}
 public Incident get(Long id){return incidents.findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Incident not found"));}
 public void readable(Incident i,AppUser u){if(u.role==Role.ADMIN)return;if(u.role==Role.EMPLOYEE&&i.createdBy.getId().equals(u.id))return;if(u.role==Role.TECHNICIAN&&i.assignedTo!=null&&i.assignedTo.getId().equals(u.id))return;throw new ResponseStatusException(HttpStatus.FORBIDDEN,"This incident is not accessible to you");}
 public void editable(Incident i,AppUser u){if(u.role==Role.ADMIN)return;if(u.role==Role.TECHNICIAN&&i.assignedTo!=null&&i.assignedTo.getId().equals(u.id))return;throw new ResponseStatusException(HttpStatus.FORBIDDEN,"Only the assigned technician or an administrator may update this incident");}
 public void record(Incident i,AppUser u,String text){IncidentHistory h=new IncidentHistory();h.incident=i;h.author=u;h.event=text;history.save(h);i.updatedAt=Instant.now();}
 public Views.IncidentView create(Requests.NewIncident r,AppUser u){Incident i=new Incident();i.title=r.title().trim();i.description=r.description().trim();i.category=r.category();i.priority=r.priority();i.createdBy=u;incidents.save(i);record(i,u,"Incident created");return Views.incident(i);}
 public Map<String,Object> detail(Long id,AppUser u){Incident i=get(id);readable(i,u);return Map.of("incident",Views.incident(i),"history",history.findByIncidentIdOrderByCreatedAtAsc(id).stream().map(h->new Views.Event(h.id,h.event,h.author.getFullName(),h.createdAt)).toList(),"comments",comments.findByIncidentIdOrderByCreatedAtAsc(id).stream().map(c->new Views.Comment(c.id,c.content,c.author.getFullName(),c.createdAt)).toList());}
 public Views.IncidentView status(Long id,Status next,AppUser u){Incident i=get(id);editable(i,u);if(i.status==Status.CLOSED)throw new ResponseStatusException(HttpStatus.CONFLICT,"Closed incidents cannot be changed");if(i.status!=next){Status previous=i.status;i.status=next;record(i,u,previous+" -> "+next);}return Views.incident(i);}
 public Views.IncidentView assign(Long id,Long technicianId,AppUser admin){Incident i=get(id);if(i.status==Status.CLOSED)throw new ResponseStatusException(HttpStatus.CONFLICT,"Closed incidents cannot be assigned");AppUser t=users.findById(technicianId).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Technician not found"));if(t.role!=Role.TECHNICIAN||!t.enabled)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Select an enabled technician");i.assignedTo=t;Status old=i.status;if(i.status==Status.OPEN)i.status=Status.ASSIGNED;record(i,admin,"Assigned to "+t.fullName+(old!=i.status?" ("+old+" -> "+i.status+")":""));return Views.incident(i);}
 public Views.Comment note(Long id,String text,AppUser u){Incident i=get(id);editable(i,u);if(i.status==Status.CLOSED)throw new ResponseStatusException(HttpStatus.CONFLICT,"Closed incidents cannot be changed");IncidentComment c=new IncidentComment();c.incident=i;c.author=u;c.content=text.trim();comments.save(c);record(i,u,"Treatment note added");return new Views.Comment(c.id,c.content,u.fullName,c.createdAt);}
}
