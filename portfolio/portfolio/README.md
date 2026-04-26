# Art Portfolio — Setup Guide

## Folder Structure
```
portfolio/
├── app.py
├── requirements.txt
├── Procfile
├── templates/
│   └── index.html
└── static/
    └── images/
        ├── drawing1.jpg   ← your drawings go here
        ├── drawing2.jpg
        └── drawing3.jpg
```

---

## Step 1 — Add Your Drawings

1. Create the folder `static/images/` inside the project
2. Copy your drawing files (JPG, PNG, WEBP) into it
3. Open `templates/index.html`
4. Find the section marked "EXAMPLE SLIDES"
5. Change each `src="/static/images/drawing1.jpg"` to your actual filenames
6. Add or remove `<div class="slide">` blocks to match how many drawings you have

---

## Step 2 — MongoDB Atlas (Free)

1. Go to https://mongodb.com/atlas and create a free account
2. Create a free M0 cluster
3. Under **Database Access** → Add a user with password
4. Under **Network Access** → Allow access from anywhere (0.0.0.0/0)
5. Click **Connect** → **Drivers** → Copy the connection string
   - Looks like: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`

---

## Step 3 — Deploy on Render (Free)

1. Push this entire folder to a **private** GitHub repo
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set these values:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** *(auto-detected from Procfile)*
5. Under **Environment Variables**, add:
   - Key: `MONGO_URI`
   - Value: *(paste your MongoDB connection string)*
6. Click **Deploy**
7. Render gives you a URL like `https://your-name.onrender.com`

---

## Step 4 — Instagram Bio

Put your Render URL in your Instagram bio.

---

## Checking Analytics (MongoDB Atlas)

1. Log into MongoDB Atlas
2. Go to **Browse Collections**
3. Open database `art_portfolio` → collection `profile_visits`
4. Each document looks like:
```json
{
  "timestamp": "2026-04-26T18:45:00Z",
  "ip": "103.x.x.x",
  "device": "iPhone",
  "referrer": "https://www.instagram.com/",
  "city": "Hyderabad",
  "region": "Telangana",
  "country": "India",
  "isp": "Jio Fiber"
}
```
