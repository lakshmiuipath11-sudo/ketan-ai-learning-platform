# KETAN AI — Online Preparation Platform

Starter Flask website with sample quiz, instant scoring, PostgreSQL connectivity check, and a secure-by-default TinyFish integration placeholder.

## GitHub website upload (no CMD)

1. Download and extract the provided ZIP on your laptop.
2. Open your GitHub repository, choose **Add file → Upload files**.
3. Drag the **contents** of the extracted `ketan-ai-learning-platform` folder into the upload area, preserving the `templates/`, `static/`, and `services/` subfolders.
4. Commit to `main`. If README.md already exists, upload the other files and update README separately if GitHub reports a conflict.

**Important:** GitHub's web uploader may not reliably preserve directory structure when selecting individual files. Drag the extracted folder contents or upload nested files using **Add file → Create new file** with names such as `templates/index.html`.

## Railway deployment

1. Railway → New Project → Deploy from GitHub repo → choose this repository.
2. Railway should detect Python and install `requirements.txt`.
3. Add a PostgreSQL service to the same Railway project.
4. In the web service's **Variables**, set `DATABASE_URL` to `${{Postgres.DATABASE_URL}}` using Railway's variable reference picker (the PostgreSQL service may have a different name).
5. Set `TINYFISH_API_KEY` only in Railway Variables, never in GitHub files.
6. Generate a public domain in Railway service settings. Open `/health` to confirm app is running and `/api/db-status` to check database connectivity.

The demo quiz questions are in-memory. Persistent user accounts, stored quiz results, and database migrations are **not yet implemented**.

TinyFish execution is deliberately disabled pending verification of the current API schema and addition of authentication, rate limiting, and outbound URL allowlisting. The key alone does not activate the feature.

## Local execution (optional)

`pip install -r requirements.txt` then `python app.py`.
