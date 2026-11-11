package ma.enset.incidents;
import io.jsonwebtoken.*;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import javax.crypto.SecretKey;
import java.util.Date;
@Service
public class JwtService {
 private final SecretKey key; private final long lifetime;
 public JwtService(@Value("${jwt.secret}") String secret,@Value("${jwt.expiration}") long lifetime) { this.key=Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret)); this.lifetime=lifetime; }
 public String issue(AppUser user) { return Jwts.builder().subject(user.email).claim("role",user.role.name()).issuedAt(new Date()).expiration(new Date(System.currentTimeMillis()+lifetime)).signWith(key).compact(); }
 public String email(String token) { return Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload().getSubject(); }
}
