import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  userName: string = 'User';
  messages: ChatMessage[] = [];
  inputMessage: string = '';
  loading: boolean = false;
  jokeText: string | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }

    this.messages.push({ role: 'assistant', content: 'Hi — I\'m HeyBuddy. How are you feeling today? You can chat with me or click the "Surprise Me" joke button for a quick mood boost.' });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  async sendMessage(): Promise<void> {
    const text = this.inputMessage?.trim();
    if (!text) return;

    this.messages.push({ role: 'user', content: text });
    this.inputMessage = '';
    this.loading = true;

    const assistantMessageIndex = this.messages.length;
    this.messages.push({ role: 'assistant', content: '' });

    try {
      const token = this.authService.getToken();
      const res = await fetch('http://localhost:8000/chat/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ message: text, history: this.messages.slice(0, -1).map(m => ({ role: m.role, content: m.content })) })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) {
        throw new Error('Response body is not readable');
      }

      const decoder = new TextDecoder();
      let alertFlag = false;
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.trim()) {
            try {
              const chunk = JSON.parse(line);
              if (chunk.text) {
                this.messages[assistantMessageIndex].content += chunk.text;
              }
              if (chunk.done && chunk.alert !== undefined) {
                alertFlag = chunk.alert;
              }
            } catch (parseErr) {
              console.error('Failed to parse chunk:', line, parseErr);
            }
          }
        }
      }

      if (alertFlag) {
        alert('It seems you may need immediate support. Please consider contacting local emergency services or a mental health professional.');
      }
    } catch (err) {
      console.error(err);
      this.messages[assistantMessageIndex].content = 'Sorry, I\'m having trouble reaching the server. Please try again later.';
    } finally {
      this.loading = false;
    }
  }

  async fetchJoke(): Promise<void> {
    this.jokeText = null;
    this.loading = true;
    try {
      const token = this.authService.getToken();
      const res = await fetch('http://localhost:8000/jokes/random', {
        method: 'GET',
        headers: {
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        }
      });
      const data = await res.json();
      if (data.setup && data.punchline) {
        this.jokeText = `${data.setup} — ${data.punchline}`;
      } else if (data.joke) {
        this.jokeText = data.joke;
      } else if (data.error) {
        this.jokeText = 'Could not fetch a joke right now.';
      } else {
        this.jokeText = JSON.stringify(data);
      }
      this.messages.push({ role: 'assistant', content: `Here's a joke: ${this.jokeText}` });
    } catch (err) {
      console.error(err);
      this.jokeText = 'Failed to fetch joke.';
    } finally {
      this.loading = false;
    }
  }
}
