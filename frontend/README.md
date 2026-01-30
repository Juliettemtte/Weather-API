# 🌤️ Weather Express - Angular Frontend

Minimalist and performant weather application with Angular 17 and TailwindCSS.

## 🚀 Quick Installation

### Prerequisites
- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Steps

```bash
# 1. Install dependencies
npm install

# 2. Run in development mode
ng serve

# 3. Open in browser
# http://localhost:4200
```

## 📦 Project Structure

```
src/app/
├── core/
│   ├── models/          # TypeScript interfaces
│   └── services/        # Angular services (HTTP, cache)
├── features/
│   ├── search/          # Search component
│   ├── current-weather/ # Current weather
│   ├── hourly-forecast/ # Hourly forecasts
│   └── daily-forecast/  # 3-day forecasts
├── shared/
│   └── utils/           # Utilities (favorites, etc.)
└── app.component.ts     # Root component
```

## ✨ Features

### ✅ Implemented
- 🔍 City search with autocomplete
- 📍 Automatic geolocation
- ⭐ Save favorite city (localStorage)
- 🌡️ Detailed current weather display
- 📊 Hourly forecast chart (Chart.js)
- 📅 3-day forecasts
- ⚡ Cache indicator (cached data)
- 📱 Mobile-first responsive design
- 🎨 Minimalist TailwindCSS interface

### 🎯 User Experience
- Loading < 500ms (with backend cache)
- Smooth animations (fade-in, slide-up)
- Clear visual feedback (loading, errors)
- No ads or unnecessary content

## 🎨 Design System

### Main Colors
- **Primary Blue**: `#0ea5e9` (Tailwind sky-500)
- **Background**: Gradient `blue-50` to `cyan-50`
- **Text**: Gray 900 for titles, Gray 600 for secondary

### Components
- **Cards**: White background, soft shadows, rounded corners (rounded-2xl)
- **Inputs**: Thin borders, blue focus with ring
- **Buttons**: 200ms transitions, hover states

## 🔧 Configuration

### Change API URL

Edit `src/app/core/services/weather.service.ts`:

```typescript
private readonly API_URL = 'http://localhost:8000/api';
// Change to your production URL
```

Or use environments:
- `src/environments/environment.ts` (dev)
- `src/environments/environment.prod.ts` (prod)

### Customize Theme

Edit `tailwind.config.js` to adjust colors:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',
        // ...
      }
    }
  }
}
```

## 📊 Performance

### Target Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Lighthouse Score**: > 90

### Applied Optimizations
- Standalone components (bundle reduction)
- Lazy loading (future routes)
- OnPush change detection (ready for use)
- Search debounce (300ms)
- Service-side cache with RxJS

## 🧪 Testing (to implement)

```bash
# Unit tests
ng test

# E2E tests
ng e2e
```

## 🏗️ Production Build

```bash
# Optimized build
ng build --configuration production

# Files are in dist/weather-app/
```

### Deployment

**Netlify / Vercel:**
```bash
# Build command
ng build --configuration production

# Publish directory
dist/weather-app
```

**`netlify.toml` or `vercel.json` configuration:**
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🔐 Environment Variables

For production, create `.env` or configure via your platform:

```bash
API_URL=https://your-backend-api.com/api
```

## 🐛 Debugging

### Common Issues

**CORS Error:**
- Verify that backend allows `http://localhost:4200`
- Check `CORS_ORIGINS` in backend `.env`

**API not accessible:**
- Verify that backend is running
- Test endpoint: `curl http://localhost:8000/health`

**Chart not displaying:**
- Verify Chart.js installation: `npm list chart.js`
- Check data in console: `console.log(this.hourly)`

## 📈 Future Improvements (post-MVP)

- [ ] Dark mode
- [ ] Multiple favorite cities (up to 5)
- [ ] Push notifications
- [ ] PWA (Progressive Web App)
- [ ] Unit tests with Jasmine
- [ ] Advanced animations (GSAP)
- [ ] Interactive charts (ApexCharts)
- [ ] Data export (CSV/PDF)

## 🤝 Contributing

1. Fork the project
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ and Angular 17**