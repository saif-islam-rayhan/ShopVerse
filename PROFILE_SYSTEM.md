# Profile System - Database Migration Guide

## Overview
To support the new profile system, the User model now includes three additional optional fields:
- `full_name` - User's full name
- `address` - User's address
- `profile_picture` - URL to user's profile picture

## Automatic Migration
MongoDB is flexible and allows adding new fields to existing documents on-demand. No manual migration is required.

## Manual MongoDB Update (Optional)
If you want to pre-populate all existing users with the new fields, run this command in MongoDB:

```javascript
// Add null values for new fields to all existing users
db.users.updateMany(
  {},
  {
    $set: {
      full_name: null,
      address: null,
      profile_picture: null
    }
  }
)
```

## Verification
To verify users have the new fields:

```javascript
db.users.findOne({})
```

Should show:
```javascript
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "username": "john_doe",
  "password": "$2b$12$...",
  "auth_provider": "local",
  "provider_id": null,
  "full_name": null,
  "address": null,
  "profile_picture": null,
  "created_at": ISODate("..."),
  "updated_at": ISODate("..."),
  "is_active": true
}
```

## Testing the Profile System

### 1. Get Profile (Protected)
```bash
curl -H "Authorization: Bearer <your_token>" \
  http://localhost:5000/api/v1/auth/profile
```

### 2. Update Profile (Protected)
```bash
curl -X PUT \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "address": "123 Main Street, New York, NY 10001",
    "profile_picture": "https://example.com/profile.jpg"
  }' \
  http://localhost:5000/api/v1/auth/profile
```

## Features Implemented

### Backend
✅ Updated User model with profile fields
✅ Created ProfileResponse schema
✅ Created UpdateProfileRequest schema
✅ Added GET /api/v1/auth/profile endpoint
✅ Added PUT /api/v1/auth/profile endpoint
✅ Added update_profile method to UserService
✅ JWT authentication on all endpoints

### Frontend
✅ Created ProfilePage component
✅ Added profile service functions (getProfile, updateProfile)
✅ Profile page with view/edit modes
✅ Image preview for profile picture URL
✅ Responsive design
✅ Error and success messages
✅ Navigation from dashboard to profile
✅ Professional UI with gradient background

## Features
- **View Profile**: Display all user information
- **Edit Profile**: Update name, address, and profile picture
- **Profile Picture Preview**: Real-time preview when entering URL
- **Form Validation**: Validates input fields
- **Error Handling**: User-friendly error messages
- **Success Feedback**: Confirmation when profile is updated
- **Responsive Design**: Works on all screen sizes
- **JWT Protection**: All endpoints require valid authentication token
