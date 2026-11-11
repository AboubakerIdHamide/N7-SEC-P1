package ma.enset.incidents;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import jakarta.validation.Valid;
import java.util.Map;
@RestController @RequestMapping("/api/profile") @Transactional
public class ProfileController {
 private final IncidentService s;private final PasswordEncoder passwords;private final JwtService jwt;
 public ProfileController(IncidentService s,PasswordEncoder p,JwtService j){this.s=s;passwords=p;jwt=j;}
 @GetMapping public Views.User profile(Authentication a){return Views.user(s.current(a));}
 @PutMapping public Map<String,Object> update(@Valid @RequestBody Requests.Profile r,Authentication a){AppUser u=s.current(a);String email=r.email().trim().toLowerCase();if(!u.email.equals(email)&&s.users().existsByEmail(email))throw new ResponseStatusException(HttpStatus.CONFLICT,"Email already used");u.fullName=r.fullName().trim();u.email=email;return Map.of("user",Views.user(u),"token",jwt.issue(u),"role",u.role,"fullName",u.fullName);}
 @PutMapping("/password") public Map<String,String> password(@Valid @RequestBody Requests.Password r,Authentication a){AppUser u=s.current(a);if(!passwords.matches(r.oldPassword(),u.password))throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Old password is incorrect");if(!r.newPassword().equals(r.confirmation()))throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Passwords do not match");u.password=passwords.encode(r.newPassword());return Map.of("message","Password changed");}
}
