# HeyBuddy Frontend

A futuristic Angular frontend application with a stunning login page and separate dashboards for users and administrators.

## Features

### 1. **Futuristic Login Page**
   - Animated gradient backgrounds with floating blobs
   - Email and password input fields
   - Password visibility toggle
   - Remember me functionality
   - Social login buttons (Google, GitHub)
   - Real-time form validation
   - Loading state with spinner animation
   - Error message display
   - Responsive design

### 2. **User Dashboard**
   - Clean navigation bar
   - User greeting
   - Logout functionality
   - Protected route (redirects to login if not authenticated)

### 3. **Admin Dashboard**
   - Enhanced navigation with admin badge
   - Admin-specific styling
   - Protected route (only accessible to admin users)
   - Role-based access control

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/          # Reusable components
│   │   ├── pages/
│   │   │   ├── login/          # Login page
│   │   │   ├── user-dashboard/ # User dashboard
│   │   │   └── admin-dashboard/# Admin dashboard
│   │   ├── services/
│   │   │   └── auth.service.ts # Authentication service
│   │   ├── app.component.ts    # Root component
│   │   ├── app.routes.ts       # Routing configuration
│   │   └── app.component.css   # Global styles
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── angular.json
├── tsconfig.json
├── tsconfig.app.json
└── package.json
```

## Installation

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn

### Setup

1. **Navigate to the frontend folder:**
   ```bash
   cd c:\Users\neelo\codes\HeyBuddy\frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Running the Application

### Development Server
```bash
npm start
```

The application will be available at `http://localhost:4200`

### Production Build
```bash
npm run build
```

The optimized build will be in the `dist/heybuddy-frontend` directory.

## Authentication Flow

1. **Login Page** (`/login`)
   - User enters email and password
   - Credentials are sent to the backend API
   - On success, JWT token and role are stored in localStorage
   - User is redirected based on role:
     - Admin → `/admin-dashboard`
     - User → `/user-dashboard`

2. **Protected Routes**
   - Both dashboards check authentication status
   - If not authenticated, users are redirected to login
   - Admin dashboard checks for admin role

3. **Logout**
   - Clears token and role from localStorage
   - Redirects to login page

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

### Login Endpoint
```
POST /users/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "jwt_token_here",
  "refresh_token": "refresh_token_here",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "role": "user"
  }
}
```

## Styling & Design

### Color Scheme
- **Primary Gradient**: Cyan (#00ccff) to Green (#00ff88)
- **Secondary Gradient**: Purple (#8338ec) to Pink (#ff006e)
- **Background**: Dark navy (#0a0e27) with gradients
- **Text**: White with subtle gray accents

### Animations
- Floating blob backgrounds
- Glowing text effects
- Form input focus animations
- Button hover effects
- Loading spinner
- Smooth transitions

### Responsive Design
- Mobile-first approach
- Works on all screen sizes
- Adaptive layouts for tablets and desktops

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Tips

### Adding New Pages
1. Create a new folder in `src/app/pages/`
2. Generate component files (`.ts`, `.html`, `.css`)
3. Add route in `app.routes.ts`

### Authentication Service
The `AuthService` provides:
- `login(email, password)` - Login user
- `setToken(token, role)` - Store token and role
- `getToken()` - Retrieve stored token
- `getRole()` - Retrieve user role
- `logout()` - Clear authentication
- `isAuthenticated()` - Check auth status

### API Calls
To make API calls, inject `AuthService` and use its methods or fetch directly with stored token:

```typescript
const token = this.authService.getToken();
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

## Future Enhancements

- [ ] User registration page
- [ ] Password reset functionality
- [ ] Profile management
- [ ] Two-factor authentication
- [ ] Dark/Light mode toggle
- [ ] Multi-language support
- [ ] User management for admins
- [ ] Advanced analytics dashboard

## Troubleshooting

### Port Already in Use
If port 4200 is already in use:
```bash
ng serve --port 4300
```

### Dependencies Issues
Clear node_modules and reinstall:
```bash
rm -r node_modules package-lock.json
npm install
```

### CORS Issues
Make sure the backend is running and configured to accept requests from `http://localhost:4200`

## License
ISC
