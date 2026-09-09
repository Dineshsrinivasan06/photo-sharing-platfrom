# Photo Sharing Platform

A full-stack photo sharing platform built for the TrizenAI Full-Stack
Internship Challenge.

## Features

- Admin registration/login
- Team member authentication
- Role-based access control
- Event creation
- Team member assignment
- Multiple photo uploads
- Photo selection
- Gallery creation
- Gallery publishing
- PIN-protected customer galleries
- Customer photo browsing
- Secure photo access

## Tech Stack

### Frontend
- React
- Vite
- React Router
- Axios

### Backend
- Python
- FastAPI
- SQLAlchemy
- JWT
- bcrypt

### Database
- MySQL

### Storage
- Cloudinary

### Deployment
- Frontend: TBD
- Backend: TBD
- Database: TBD

## Architecture

The application follows a client-server architecture.

React
  |
  | HTTP / REST API
  |
FastAPI
  |
  +---- MySQL
  |
  +---- Cloudinary

  ### Frontend

The React application provides separate interfaces for:

- Admin
- Team Member
- Customer

### Backend

FastAPI exposes REST APIs for:

- Authentication
- Events
- Photos
- Galleries
- Customer gallery access

### Database

MySQL stores application metadata including users, events,
event memberships, photos, galleries and gallery-photo relationships.

### Object Storage

Uploaded images are stored in Cloudinary.

The database stores the image URL and related metadata rather than
the actual image binary.

## Database Structure

### Users

- id
- name
- email
- password_hash
- role
- created_at

### Events

- id
- name
- description
- created_by
- created_at

### EventMembers

- id
- event_id
- user_id

### Photos

- id
- event_id
- uploaded_by
- filename
- storage_location
- cloudinary_public_id
- file_size
- is_selected
- created_at

### Galleries

- id
- event_id
- gallery_token
- pin_hash
- is_published
- created_at

### GalleryPhotos

- id
- gallery_id
- photo_id
## Application Workflow

Admin
  |
  +-- Create Event
  |
  +-- Add Team Members
          |
          v
      Team Member
          |
          +-- Upload Photos
                  |
                  v
               Admin
                  |
                  +-- Review Photos
                  |
                  +-- Select Photos
                  |
                  +-- Create Gallery
                  |
                  +-- Set PIN
                  |
                  +-- Publish
                          |
                          v
                       Customer
                          |
                          +-- Open Gallery Link
                          |
                          +-- Enter PIN
                          |
                          +-- Browse Photos

## Local Setup

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt       