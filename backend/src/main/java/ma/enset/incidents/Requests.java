package ma.enset.incidents;
import jakarta.validation.constraints.*;
public class Requests {
 public record Register(@NotBlank @Size(max=120) String fullName,@NotBlank @Email @Size(max=200) String email,@NotBlank @Size(min=8,max=72) String password) {}
 public record Login(@NotBlank @Email String email,@NotBlank String password) {}
 public record Profile(@NotBlank @Size(max=120) String fullName,@NotBlank @Email @Size(max=200) String email) {}
 public record Password(@NotBlank String oldPassword,@NotBlank @Size(min=8,max=72) String newPassword,@NotBlank String confirmation) {}
 public record NewIncident(@NotBlank @Size(max=180) String title,@NotBlank @Size(max=5000) String description,@NotNull Category category,@NotNull Priority priority) {}
 public record ChangeStatus(@NotNull Status status) {}
 public record Note(@NotBlank @Size(max=5000) String content) {}
}
