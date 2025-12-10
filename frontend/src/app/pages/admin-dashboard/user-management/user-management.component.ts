import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-user-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-management.component.html',
  styleUrls: ['./user-management.component.css']
})
export class UserManagementComponent implements OnInit {
  users: any[] = [];
  selectedUser: any = null;
  newUser: any = { name: '', email: '', password: '', age: '', role: 'user' };
  showCreateForm = false;
  error = '';
  loading = false;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.fetchUsers();
  }

  fetchUsers() {
    this.loading = true;
    this.userService.getAllUsers().then(users => {
      this.users = users;
      this.loading = false;
    });
  }

  selectUser(user: any) {
    this.selectedUser = { ...user };
    this.showCreateForm = false;
  }

  saveUser() {
    if (!this.selectedUser.id) return;
    this.userService.updateUser(this.selectedUser.id, this.selectedUser).then(() => {
      this.selectedUser = null;
      this.fetchUsers();
    });
  }

  deleteUser(id: number) {
    if (!confirm('Delete this user?')) return;
    this.userService.deleteUser(id).then(() => this.fetchUsers());
  }

  showCreateUserForm() {
    this.showCreateForm = true;
    this.selectedUser = null;
    this.newUser = { name: '', email: '', password: '', age: '', role: 'user' };
  }

  createUser() {
    if (!this.newUser.name || !this.newUser.email || !this.newUser.password) {
      this.error = 'Name, email, and password are required.';
      return;
    }
    this.userService.createUser(this.newUser).then(res => {
      if (res.id) {
        this.showCreateForm = false;
        this.fetchUsers();
      } else {
        this.error = res.detail || 'Failed to create user.';
      }
    });
  }

  cancel() {
    this.selectedUser = null;
    this.showCreateForm = false;
    this.error = '';
  }
}
