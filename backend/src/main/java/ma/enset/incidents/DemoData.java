package ma.enset.incidents;
import org.springframework.context.annotation.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
@Configuration
public class DemoData {
 @Bean CommandLineRunner seed(UserRepository users,PasswordEncoder passwords){return args->{String[][] rows={{"Employee One","employee1@demo.test","EMPLOYEE"},{"Employee Two","employee2@demo.test","EMPLOYEE"},{"Technician A","tech@demo.test","TECHNICIAN"},{"Administrator","admin@demo.test","ADMIN"}};for(String[] r:rows)if(!users.existsByEmail(r[1])){AppUser u=new AppUser();u.fullName=r[0];u.email=r[1];u.role=Role.valueOf(r[2]);u.password=passwords.encode("Demo1234!");users.save(u);}};}
}
