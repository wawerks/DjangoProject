# Django Encrypted Real-Time Chat Application

A secure, real-time chat application built with Django, featuring end-to-end encryption and WebSocket communication.
Web app Installation: 

1.	Clone the Repository in this link: https://github.com/wawerks/DjangoProject.git .
2.	Navigate to DjangoProject.
3.	Go to DjangoProject-App1/a_core/settings.py and change the database directory where the DjangoProject-App2 database directory located.
4.	Ensure that python is properly installed on your device.
5.	Open integrated Terminal on DjangoProject-App1 and run pip install requirements.txt.
6.	Run the server on App1, run python manage.py runserver.
7.	Open integrated Terminal on DjangoProject-App2 and run pip install requirements.txt.
8.	Navigate to ab_core.
9.	Run the server on App2, run python manage.py runserver 8081.
10.	Open the browser with the applications URL.
    
## 🌟 Features

- **Real-time Communication**
  - WebSocket-based chat using Django Channels
  - REST API endpoints for secure message transmission
  - Instant message delivery
  - Group chat support

- **Security**
  - End-to-end encryption using Fernet
  - Custom encryption middleware
  - JWT-based authentication
  - CORS protection
  - Secure user authentication
  - Protected WebSocket connections
  - CSRF protection

- **REST API Features**
  - Secure message transmission
  - User management endpoints
  - Group chat operations
  - JWT authentication
  - Rate limiting
  - Request/Response encryption

- **User Management**
  - User registration and authentication
  - Profile management
  - Session handling
  - JWT token management

- **Modern UI/UX**
  - Responsive design with Tailwind CSS
  - Real-time updates with HTMX
  - Dynamic interactions with AlpineJS
  - Dark mode support

## 🏗 Architecture

The application follows a two-app architecture:

### App1 (Frontend)
```bash
DjangoProject-App1/
├── a_core/          # Main project settings
├── a_rtchat/        # Chat application
├── a_users/         # User management
└── a_home/          # Landing pages
```

### App2 (Backend)
```bash
DjangoProject-App2/
└── ab_core/         # Backend API and storage
```

## 🔧 Technical Stack

- **Backend Framework**
  - Django 5.0+
  - Django Channels (WebSocket)
  - Django REST Framework
  - SQLite/PostgreSQL

- **Frontend Technologies**
  - HTML/CSS/JavaScript
  - Tailwind CSS
  - HTMX
  - AlpineJS

- **Security**
  - django-allauth
  - cryptography (Fernet)
  - Django's security middleware

## 📦 Dependencies

```plaintext
Django
django-allauth
django-htmx
django-cleanup
Pillow
channels
cryptography
daphne
```

## 🚀 Installation

1. Clone the repository
```bash
git clone [repository-url]
cd [project-directory]
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
# Create .env file in project root
SECRET_KEY=your_secret_key
DEBUG=True
ENCRYPT_KEY=your_encryption_key
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start the development server
```bash
python manage.py runserver
```

## 🚀 Running the Applications

### Setup App1 (Frontend) and App2 (Backend)

1. **Initial Setup for Both Apps**
```bash
# Clone the repository
git clone [repository-url]

# Create two separate virtual environments
python -m venv DjangoProject-App1/venv
python -m venv DjangoProject-App2/venv
```

2. **Setup App1 (Frontend)**
```bash
# Navigate to App1 directory
cd DjangoProject-App1

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start App1 server (default port 8000)
python manage.py runserver
```

3. **Setup App2 (Backend)**
```bash
# Open a new terminal
# Navigate to App2 directory
cd DjangoProject-App2

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start App2 server on port 8081
python manage.py runserver 8081
```

### Verifying the Setup

1. **Check App1 (Frontend)**
   - Open browser: `http://127.0.0.1:8000`
   - You should see the welcome page
   - Register/Login to access chat features

2. **Check App2 (Backend)**
   - API endpoint: `http://127.0.0.1:8081/api/`
   - Handles message storage and retrieval
   - No direct user interface

### Important Notes

- Both applications must be running simultaneously
- App1 communicates with App2 through API calls
- WebSocket connections are handled by App1
- Message encryption/decryption happens in App1
- Message storage occurs in App2

### Troubleshooting

1. **Port Conflicts**
   ```bash
   # If port 8000 is in use for App1
   python manage.py runserver 8001

   # If port 8081 is in use for App2
   python manage.py runserver 8082
   ```

2. **Cross-Origin Issues**
   - Ensure CORS settings are correct in App2
   - Check App1's settings for correct App2 URL

3. **WebSocket Connection Issues**
   - Verify Daphne is running
   - Check channel layer configuration
   - Ensure Redis is running (if using Redis channel layer)

## 🔗 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details

### Chat Groups
- `GET /api/groups/` - List all chat groups
- `POST /api/groups/` - Create new chat group
- `GET /api/groups/{id}/` - Get group details
- `PUT /api/groups/{id}/` - Update group
- `DELETE /api/groups/{id}/` - Delete group

### Messages
- `GET /api/groups/{id}/messages/` - List group messages
- `POST /api/groups/{id}/messages/` - Send new message
- `GET /api/groups/{id}/messages/{msg_id}/` - Get message details

All API endpoints are protected with:
- JWT authentication
- Request/Response encryption
- Rate limiting
- CORS protection

## 💬 Usage

1. Register a new account or login
2. Navigate to the chat interface
3. Join or create a chat room
4. Start sending encrypted messages

## 🔐 Security Features

### Message Encryption
- All messages are encrypted using Fernet symmetric encryption
- Encryption keys are securely managed
- Messages are encrypted before storage

### WebSocket Security
- Authenticated WebSocket connections
- Secure group management
- Protected chat rooms

### User Authentication
- Secure registration and login
- Session management
- Password reset functionality

## 🛠 Development

### Running Tests
```bash
python manage.py test
```

### Code Style
Follow PEP 8 guidelines for Python code.

## 📝 API Documentation

### WebSocket Endpoints
- `ws/chatroom/<chatroom_name>` - Chat room WebSocket endpoint

### HTTP Endpoints
- `/` - Home page
- `/chat/` - Chat interface
- `/accounts/` - User authentication views

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- [Your Name]

## 🙏 Acknowledgments

- Django Framework
- Django Channels Team
- HTMX and AlpineJS communities
