package ma.enset.incidents;
import org.springframework.context.annotation.*;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.*;
import java.util.List;
@Configuration @EnableMethodSecurity
public class SecurityConfig {
 @Bean PasswordEncoder passwords() { return new BCryptPasswordEncoder(); }
 @Bean SecurityFilterChain chain(HttpSecurity http,JwtFilter jwt) throws Exception {
  return http.csrf(c->c.disable()).cors(c->c.configurationSource(cors()))
   .headers(h->h.frameOptions(f->f.sameOrigin()))
   .sessionManagement(s->s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
   .authorizeHttpRequests(a->a.requestMatchers("/auth/**","/h2-console/**","/error").permitAll().requestMatchers("/api/admin/**").hasRole("ADMIN").anyRequest().authenticated())
   .exceptionHandling(e->e.authenticationEntryPoint((q,r,x)->{r.setStatus(401);r.setContentType("application/json");r.getWriter().write("{\"status\":401,\"message\":\"Authentication required or token expired\"}");})
    .accessDeniedHandler((q,r,x)->{r.setStatus(403);r.setContentType("application/json");r.getWriter().write("{\"status\":403,\"message\":\"Access forbidden\"}");}))
   .addFilterBefore(jwt,UsernamePasswordAuthenticationFilter.class).build();
 }
 @Bean CorsConfigurationSource cors() { CorsConfiguration c=new CorsConfiguration();c.setAllowedOrigins(List.of("http://localhost:5173","http://127.0.0.1:5173"));c.setAllowedMethods(List.of("GET","POST","PUT","OPTIONS"));c.setAllowedHeaders(List.of("Authorization","Content-Type"));UrlBasedCorsConfigurationSource s=new UrlBasedCorsConfigurationSource();s.registerCorsConfiguration("/**",c);return s; }
}
