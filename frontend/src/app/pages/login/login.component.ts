import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  loading: boolean = false;
  error: string = '';
  showPassword: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  onLogin(): void {
    if (!this.email || !this.password) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.loading = true;
    this.error = '';

    this.authService.login(this.email, this.password)
      .then(response => {
        this.loading = false;
        if (response.access_token) {
          const role = response.user.role || 'user';
          this.authService.setToken(response.access_token, role);
          
          // store user id and name for client-side operations like diary
          try {
            if (response.user) {
              if (response.user.id) {
                localStorage.setItem('user_id', String(response.user.id));
              }
              if (response.user.name) {
                this.authService.setName(response.user.name);
              }
            }
          } catch (err) {
            console.warn('Could not persist user info', err);
          }

          // Redirect based on role
          if (role === 'admin') {
            this.router.navigate(['/admin-dashboard']);
          } else {
            this.router.navigate(['/user-dashboard']);
          }
        } else {
          this.error = response.detail || 'Login failed';
        }
      })
      .catch(err => {
        this.loading = false;
        this.error = 'Invalid email or password';
        console.error('Login error:', err);
      });
  }

  onSignUp(): void {
    // Navigate to sign up page (to be implemented)
    console.log('Sign up clicked');
  }
}
