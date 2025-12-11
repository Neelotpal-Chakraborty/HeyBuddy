import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';

interface ChatMessage { role: 'user' | 'assistant' | 'system'; content: string }

@Component({
  selector: 'app-chat-with-diary',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-with-diary.component.html',
  styleUrls: ['./chat-with-diary.component.css']
})
export class ChatWithDiaryComponent implements OnInit {
  messages: ChatMessage[] = [];
  inputMessage: string = '';
  loading = false;

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.messages.push({ role: 'assistant', content: 'Ask me anything about your diary entries. I will only use your diary entries to answer.' });
  }

  getUserId(): string | null { return localStorage.getItem('user_id'); }

  async send(): Promise<void> {
    const userId = this.getUserId();
    const q = this.inputMessage?.trim();
    if (!userId || !q) return;
    this.messages.push({ role: 'user', content: q });
    this.inputMessage = '';
    this.loading = true;
    try {
      const res = await fetch('http://localhost:8000/rag/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: Number(userId), question: q, top_k: 5 })
      });
      const data = await res.json();
      if (res.ok) {
        this.messages.push({ role: 'assistant', content: data.answer });
      } else {
        this.messages.push({ role: 'assistant', content: data.detail || 'Failed to get answer' });
      }
    } catch (err) {
      console.error(err);
      this.messages.push({ role: 'assistant', content: 'Error contacting server.' });
    } finally {
      this.loading = false;
    }
  }
}
