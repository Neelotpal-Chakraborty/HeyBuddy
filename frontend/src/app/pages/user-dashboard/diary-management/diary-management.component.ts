import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';

interface DiaryDate { date: string }

@Component({
  selector: 'app-diary-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './diary-management.component.html',
  styleUrls: ['./diary-management.component.css']
})
export class DiaryManagementComponent implements OnInit {
  selectedDate: string = new Date().toISOString().slice(0,10);
  content: string = '';
  dates: string[] = [];
  entryId: number | null = null;
  loading: boolean = false;

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.loadDates();
  }

  getUserId(): string | null {
    return localStorage.getItem('user_id');
  }

  async loadDates() {
    const userId = this.getUserId();
    if (!userId) return;
    try {
      const res = await fetch(`http://localhost:8000/diary/dates/${userId}`);
      if (!res.ok) throw new Error('Failed to load dates');
      const data = await res.json();
      this.dates = data.dates || [];
    } catch (err) {
      console.error(err);
    }
  }

  async loadEntryForDate() {
    const userId = this.getUserId();
    if (!userId) return;
    this.loading = true;
    try {
      const res = await fetch(`http://localhost:8000/diary/${userId}/${this.selectedDate}`);
      if (res.status === 404) {
        this.content = '';
        this.entryId = null;
        this.loading = false;
        return;
      }
      if (!res.ok) throw new Error('Failed to load entry');
      const data = await res.json();
      this.content = data.content || '';
      this.entryId = data.id || null;
    } catch (err) {
      console.error(err);
    } finally {
      this.loading = false;
    }
  }

  async saveEntry() {
    const userId = this.getUserId();
    if (!userId) return alert('User not found');

    const payload = { user_id: Number(userId), date: this.selectedDate, content: this.content };
    try {
      let res;
      if (this.entryId) {
        res = await fetch(`http://localhost:8000/diary/${this.entryId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: this.content })
        });
      } else {
        res = await fetch(`http://localhost:8000/diary/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      }

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Save failed');
      }

      const data = await res.json();
      this.entryId = data.id;
      await this.loadDates();
      alert('Saved');
    } catch (err) {
      console.error(err);
      alert('Failed to save entry');
    }
  }

  selectDate(d: string) {
    this.selectedDate = d;
    this.loadEntryForDate();
  }

  selectToday() {
    const today = new Date().toISOString().slice(0,10);
    this.selectedDate = today;
    this.loadEntryForDate();
  }
}
