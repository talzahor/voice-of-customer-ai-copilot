# Voice of Customer AI Copilot — local prototype

This is a desktop-first, interactive Product Manager portfolio prototype. It reads a copy of the validated classified CSV in the browser and does not call an AI API or use a backend.

## Run locally

1. Open Terminal in this folder:

   ```bash
   cd "/Users/talzahor/Documents/Voice of Customer AI Copilot/web-prototype"
   ```

2. Install dependencies once:

   ```bash
   pnpm install
   ```

3. Start the prototype:

   ```bash
   pnpm dev
   ```

4. Open the Local URL printed by Vite, normally <http://localhost:5173>.

If your terminal uses npm instead, `npm install` and `npm run dev` work with the same project.

## Data

`public/customer_feedback_classified.csv` is a read-only copy used by the prototype. The original CSV and Python classification pipeline in the parent project folder remain unchanged.
