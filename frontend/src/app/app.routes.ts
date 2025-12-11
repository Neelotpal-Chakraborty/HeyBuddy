import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { UserDashboardComponent } from './pages/user-dashboard/user-dashboard.component';
import { AdminDashboardComponent } from './pages/admin-dashboard/admin-dashboard.component';
import { UserManagementComponent } from './pages/admin-dashboard/user-management/user-management.component';
import { ChatComponent } from './pages/chat/chat.component';
import { DiaryManagementComponent } from './pages/user-dashboard/diary-management/diary-management.component';
import { ChatWithDiaryComponent } from './pages/user-dashboard/chat-with-diary/chat-with-diary.component';

export const appRoutes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  {
    path: 'user-dashboard', component: UserDashboardComponent, children: [
      { path: 'chat', component: ChatComponent },
      { path: 'diary', component: DiaryManagementComponent },
      { path: 'chat-diary', component: ChatWithDiaryComponent },
      { path: '', redirectTo: 'diary', pathMatch: 'full' }
    ]
  },
  { path: 'admin-dashboard', component: AdminDashboardComponent, children: [
      { path: 'users', component: UserManagementComponent }
    ]
  },
  { path: '**', redirectTo: 'login' }
];
