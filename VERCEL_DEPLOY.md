# 🚀 Hosting on Vercel

Your project is now configured for Vercel deployment! Follow these steps to get it live.

## ⚠️ Important Limitations
- **Database**: Vercel is serverless and ephemeral. The default SQLite database will be **reset** on every deployment and potentially every request if the lambda cold starts.
  - **Impact**: User sessions and uploaded data might be lost frequently.
  - **Solution**: For a real production app, connect a remote database like **Neon (Postgres)** or **Supabase**.
- **Media Files**: Vercel does not support persistent file uploads to the filesystem.
  - **Impact**: Uploaded CSVs are stored in `/tmp` which is also ephemeral.
  - **Solution**: This demo uses session storage for small dataframes, which works but verify the memory limits.

## 📋 Deployment Steps

### 1. Push to GitHub
If you haven't already, push your code to a GitHub repository:
```bash
git add .
git commit -m "Configure for Vercel deployment"
# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/dashbot.git
git branch -M main
git push -u origin main
```

### 2. Import to Vercel
1.  Go to [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Select your `dashbot` repository from GitHub.

### 3. Configure Project
Vercel should automatically detect it's a Python/Django project.
- **Framework Preset**: Other (or default)
- **Root Directory**: `./` (default)
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput` (optional, Vercel often handles this)
- **Output Directory**: `staticfiles` (if asked)

### 4. Environment Variables 🔑
**Crucial Step**: You must add your environment variables in the Vercel dashboard:
1.  Expand the **"Environment Variables"** section.
2.  Add the following:
    - `GOOGLE_API_KEY`: Your Gemini API Key (copy from your `.env`)
    - `DJANGO_SECRET_KEY`: (Optional) Generate a random string or use the one in `settings.py` for now.
    - `DEBUG`: `False` (Recommended for production)

### 5. Deploy
Click **"Deploy"**. Vercel will build your app, install dependencies, and launch it.

### 6. Verify
Once deployed, click the URL provided by Vercel (e.g., `https://dashbot.vercel.app`).
- Try uploading a sample CSV.
- **Note**: If `DEBUG=False`, make sure your static files are loading correctly. If not, check "Logs".

## 🛠 Troubleshooting

- **Static Files 404**: Ensure `whitenoise` is in `MIDDLEWARE` and `STATIC_ROOT` is set (we did this!).
- **Upload Failures**: If CSVs are too large, the serverless function might time out or run out of memory.
- **CSRF Verification Failed**: Ensure `ALLOWED_HOSTS` includes `.vercel.app` (we did this!).

---

**Enjoy your live AI Dashboard!** 🚀
