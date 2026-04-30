# Frontend (React + Vite + Tailwind)

Install and run:

```bash
cd frontend
npm install
npm run dev
```

Environment:
- `VITE_API_URL` — set to your backend API base, e.g. `http://localhost:5000/api`

Pages:
- `/` Home
- `/predict` Prediction form (connects to backend `/predict`)
- `/dashboard` Dashboard and charts
- `/shap` SHAP explainability
- `/about` Research details

To deploy to Vercel: connect this folder as a Vite app and set build command `npm run build` and output `dist`.
