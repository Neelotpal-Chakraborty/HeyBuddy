import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class UserService {
  private apiUrl = 'http://localhost:8000/users';

  getAllUsers() {
    return fetch(`${this.apiUrl}/users`).then(res => res.json());
  }

  getUserById(id: number) {
    return fetch(`${this.apiUrl}/users/${id}`).then(res => res.json());
  }

  createUser(user: any) {
    return fetch(`${this.apiUrl}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user)
    }).then(res => res.json());
  }

  updateUser(id: number, user: any) {
    return fetch(`${this.apiUrl}/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user)
    }).then(res => res.json());
  }

  deleteUser(id: number) {
    return fetch(`${this.apiUrl}/users/${id}`, {
      method: 'DELETE' });
  }
}
