package ma.enset.incidents;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import jakarta.validation.Valid;
import java.util.Map;
@RestController @RequestMapping("/auth")
public class AuthController {
 private final UserRepository users;private final PasswordEncoder passwords;private final JwtService jwt;
 public AuthController(UserRepository u,PasswordEncoder p,JwtService j){users=u;passwords=p;jwt=j;}
 @PostMapping("/register") @ResponseStatus(HttpStatus.CREATED) @Transactional
 public Map<String,Object> register(@Valid @RequestBody Requests.Register r){String email=r.email().trim().toLowerCase();if(users.existsByEmail(email))throw new ResponseStatusException(HttpStatus.CONFLICT,"Email already used");AppUser u=new AppUser();u.fullName=r.fullName().trim();u.email=email;u.password=passwords.encode(r.password());u.role=Role.EMPLOYEE;users.save(u);return response(u);}
 @PostMapping("/login") public Map<String,Object> login(@Valid @RequestBody Requests.Login r){AppUser u=users.findByEmail(r.email().trim().toLowerCase()).orElseThrow(()->new ResponseStatusException(HttpStatus.UNAUTHORIZED,"Invalid credentials"));if(!u.enabled||!passwords.matches(r.password(),u.password))throw new ResponseStatusException(HttpStatus.UNAUTHORIZED,"Invalid credentials or disabled account");return response(u);}
 private Map<String,Object> response(AppUser u){return Map.of("token",jwt.issue(u),"role",u.role,"fullName",u.fullName,"user",Views.user(u));}
}
