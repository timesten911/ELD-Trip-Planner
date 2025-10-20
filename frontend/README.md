# ELD Trip Planner - Frontend

React frontend for the ELD Trip Planner application with modern UI/UX.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create .env file:
```bash
copy .env.example .env
```

3. Start development server:
```bash
npm start
```

4. Build for production:
```bash
npm run build
```

## Features

- **Modern UI**: Built with React and TailwindCSS
- **Interactive Maps**: Leaflet with OpenStreetMap
- **Responsive Design**: Works on desktop and mobile
- **Component Library**: shadcn/ui components
- **Icons**: Lucide React icons

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # React components
│   │   ├── ui/         # UI components (shadcn/ui)
│   │   ├── TripForm.jsx
│   │   ├── RouteMap.jsx
│   │   ├── TripSummary.jsx
│   │   └── ELDLogViewer.jsx
│   ├── lib/            # Utilities
│   ├── App.jsx         # Main app component
│   ├── index.js        # Entry point
│   └── index.css       # Global styles
├── package.json        # Dependencies
└── tailwind.config.js  # Tailwind configuration
```

## Components

### TripForm
Input form for trip details with validation.

### RouteMap
Interactive map showing route with markers and polylines.

### TripSummary
Statistics and segment breakdown for the trip.

### ELDLogViewer
Display and download daily ELD log sheets.

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000/api)

## Technologies

- React 18.2
- TailwindCSS 3.3
- Leaflet 1.9
- Axios 1.6
- Lucide React (icons)
- Radix UI (accessible components)

## Deployment

### Vercel
1. Push to GitHub
2. Import project in Vercel
3. Set environment variable: `REACT_APP_API_URL`
4. Deploy

### Netlify
1. Build: `npm run build`
2. Publish directory: `build`
3. Set environment variable: `REACT_APP_API_URL`
