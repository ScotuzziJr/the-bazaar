# The Bazaar

[**The Bazaar**](https://the-bazaar.onrender.com) is a collaborative social network for professionals and project creators. It enables users to share projects, connect through likes and comments, invite others to collaborate, and stay updated via notifications.

## 🌟 Features

- User registration and authentication (login/logout)
- Project creation and collaboration requests
- Social interactions (likes and comments)
- Notifications for:
  - New posts from collaborators
  - Comments and likes on your posts
  - Collaboration invitations
- Responsive feed with rich post display
- Profile pages with project summaries
- Admin interface for platform moderation

## 🛠 Tech Stack

- **Backend**: Django 4.x
- **Frontend**: Django Templates + Bootstrap
- **Database**: PostgreSQL (production), SQLite (development)
- **Storage**: Cloudinary (media), WhiteNoise (static files)
- **Deployment**: Render.com
- **Authentication**: Django's built-in system with user roles

## 🚀 Setup & Installation

1. **Clone the repository**

```bash
git clone https://github.com/ScotuzziJr/the-bazaar.git
cd the-bazaar
```

2. **Create a virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file or set the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3  # or your PostgreSQL URI
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

4. **Run migrations and start server**

```bash
python manage.py migrate
python manage.py runserver
```

## 📬 Contributing

Contributions are welcome! Open an issue or submit a pull request with improvements or fixes.

## 📄 License

MIT License.