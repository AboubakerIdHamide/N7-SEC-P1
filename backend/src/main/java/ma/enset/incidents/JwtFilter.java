package ma.enset.incidents;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;
import org.springframework.stereotype.Component;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;
import java.util.List;
@Component
public class JwtFilter extends OncePerRequestFilter {
 private final JwtService jwt; private final UserRepository users;
 public JwtFilter(JwtService jwt,UserRepository users) {this.jwt=jwt;this.users=users;}
 @Override protected void doFilterInternal(HttpServletRequest req,HttpServletResponse res,FilterChain chain) throws ServletException,IOException {
  String header=req.getHeader("Authorization");
  if(header!=null && header.startsWith("Bearer ")) {
   try { AppUser u=users.findByEmail(jwt.email(header.substring(7))).orElse(null);
    // Read enabled and role from the database on every request: disabling a user takes effect immediately.
    if(u!=null && u.enabled) SecurityContextHolder.getContext().setAuthentication(new UsernamePasswordAuthenticationToken(u.email,null,List.of(new SimpleGrantedAuthority("ROLE_"+u.role.name()))));
   } catch(io.jsonwebtoken.JwtException | IllegalArgumentException e) { SecurityContextHolder.clearContext(); }
  }
  chain.doFilter(req,res);
 }
}
