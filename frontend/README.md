# 🌤️ Météo Express - Frontend Angular

Application météo minimaliste et performante avec Angular 17 et TailwindCSS.

## 🚀 Installation rapide

### Prérequis
- Node.js 18+ et npm
- Backend API en cours d'exécution sur `http://localhost:8000`

### Étapes

```bash
# 1. Installer les dépendances
npm install

# 2. Lancer en développement
ng serve

# 3. Ouvrir dans le navigateur
# http://localhost:4200
```

## 📦 Structure du projet

```
src/app/
├── core/
│   ├── models/          # Interfaces TypeScript
│   └── services/        # Services Angular (HTTP, cache)
├── features/
│   ├── search/          # Composant recherche
│   ├── current-weather/ # Météo actuelle
│   ├── hourly-forecast/ # Prévisions horaires
│   └── daily-forecast/  # Prévisions 3 jours
├── shared/
│   └── utils/           # Utilitaires (favoris, etc.)
└── app.component.ts     # Composant racine
```

## ✨ Fonctionnalités

### ✅ Implémentées
- 🔍 Recherche de ville avec autocomplétion
- 📍 Géolocalisation automatique
- ⭐ Sauvegarde d'une ville favorite (localStorage)
- 🌡️ Affichage météo actuelle détaillée
- 📊 Graphique des prévisions horaires (Chart.js)
- 📅 Prévisions sur 3 jours
- ⚡ Indicateur de cache (données en cache)
- 📱 Design responsive mobile-first
- 🎨 Interface minimaliste TailwindCSS

### 🎯 Expérience utilisateur
- Chargement < 500ms (avec cache backend)
- Animations fluides (fade-in, slide-up)
- Feedback visuel clair (loading, erreurs)
- Aucune publicité ni contenu superflu

## 🎨 Design System

### Couleurs principales
- **Primary Blue**: `#0ea5e9` (Tailwind sky-500)
- **Background**: Gradient `blue-50` to `cyan-50`
- **Text**: Gray 900 pour titres, Gray 600 pour secondaire

### Composants
- **Cards**: Fond blanc, ombres douces, coins arrondis (rounded-2xl)
- **Inputs**: Bordures fines, focus bleu avec ring
- **Buttons**: Transitions 200ms, hover states

## 🔧 Configuration

### Changer l'URL de l'API

Modifier `src/app/core/services/weather.service.ts`:

```typescript
private readonly API_URL = 'http://localhost:8000/api';
// Changer pour votre URL de production
```

Ou utiliser les environments:
- `src/environments/environment.ts` (dev)
- `src/environments/environment.prod.ts` (prod)

### Personnaliser le thème

Modifier `tailwind.config.js` pour ajuster les couleurs:

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

## 📊 Performances

### Métriques cibles
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Lighthouse Score**: > 90

### Optimisations appliquées
- Standalone components (réduction bundle)
- Lazy loading (futures routes)
- OnPush change detection (prêt pour usage)
- Debounce sur recherche (300ms)
- Cache côté service avec RxJS

## 🧪 Tests (à implémenter)

```bash
# Tests unitaires
ng test

# Tests e2e
ng e2e
```

## 🏗️ Build de production

```bash
# Build optimisé
ng build --configuration production

# Les fichiers sont dans dist/weather-app/
```

### Déploiement

**Netlify / Vercel:**
```bash
# Build command
ng build --configuration production

# Publish directory
dist/weather-app
```

**Configuration `netlify.toml` ou `vercel.json`:**
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🔐 Variables d'environnement

Pour la production, créer `.env` ou configurer via votre plateforme:

```bash
API_URL=https://your-backend-api.com/api
```

## 🐛 Debugging

### Problèmes courants

**CORS Error:**
- Vérifier que le backend autorise `http://localhost:4200`
- Voir `CORS_ORIGINS` dans le backend `.env`

**API non accessible:**
- Vérifier que le backend est lancé
- Tester l'endpoint: `curl http://localhost:8000/health`

**Graphique ne s'affiche pas:**
- Vérifier l'installation de Chart.js: `npm list chart.js`
- Vérifier les données dans la console: `console.log(this.hourly)`

## 📈 Prochaines améliorations (post-MVP)

- [ ] Mode sombre (dark mode)
- [ ] Multi-villes favorites (jusqu'à 5)
- [ ] Notifications push
- [ ] PWA (Progressive Web App)
- [ ] Tests unitaires avec Jasmine
- [ ] Animations avancées (GSAP)
- [ ] Graphiques interactifs (ApexCharts)
- [ ] Export données (CSV/PDF)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

MIT License - voir le fichier LICENSE pour plus de détails.

---

**Fait avec ❤️ et Angular 17**