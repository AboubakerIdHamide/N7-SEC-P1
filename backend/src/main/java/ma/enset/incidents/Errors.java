package ma.enset.incidents;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.http.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.dao.DataIntegrityViolationException;
import java.util.Map;
@RestControllerAdvice
public class Errors {
 @ExceptionHandler(ResponseStatusException.class) ResponseEntity<?> status(ResponseStatusException e){return ResponseEntity.status(e.getStatusCode()).body(Map.of("status",e.getStatusCode().value(),"message",e.getReason()==null?"Request failed":e.getReason()));}
 @ExceptionHandler(MethodArgumentNotValidException.class) ResponseEntity<?> validation(MethodArgumentNotValidException e){return ResponseEntity.badRequest().body(Map.of("status",400,"message","Invalid input","errors",e.getBindingResult().getFieldErrors().stream().map(f->f.getField()+": "+f.getDefaultMessage()).toList()));}
 @ExceptionHandler(HttpMessageNotReadableException.class) ResponseEntity<?> malformed(){return ResponseEntity.badRequest().body(Map.of("status",400,"message","Invalid JSON or enum value"));}
 @ExceptionHandler(AccessDeniedException.class) ResponseEntity<?> forbidden(){return ResponseEntity.status(403).body(Map.of("status",403,"message","Access forbidden"));}
 @ExceptionHandler(DataIntegrityViolationException.class) ResponseEntity<?> conflict(){return ResponseEntity.status(409).body(Map.of("status",409,"message","Conflicting or duplicate data"));}
}
