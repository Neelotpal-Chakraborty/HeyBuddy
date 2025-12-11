import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-user-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './user-dashboard.component.html',
  styleUrls: ['./user-dashboard.component.css']
})
export class UserDashboardComponent {
  constructor(private authService: AuthService, private router: Router) {}

  get userName(): string {
    return this.authService.getName() || 'User';
  }

  get userRole(): string {
    return this.authService.getRole() || 'user';
  }

  openChat() {
    this.router.navigate(['/user-dashboard/chat']);
  }

  openDiary() {
    this.router.navigate(['/user-dashboard/diary']);
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
