import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube(token_file='token.pickle'):
    """Authenticate and return the YouTube API service."""
    creds = None
    # The file stores the user's access and refresh tokens.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secret.json'):
                raise FileNotFoundError("Missing 'client_secret.json'. Please download it from Google Cloud Console and place it in the root directory.")
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
            
    return build('youtube', 'v3', credentials=creds)

def upload_video(video_path: str, title: str, description: str, tags: list = None, privacy_status: str = "private", token_file: str = "token.pickle"):
    """Uploads a video to YouTube."""
    print("\n--- AUTHENTICATING WITH YOUTUBE ---")
    youtube = authenticate_youtube(token_file)
    
    print(f"Uploading '{title}' to YouTube...")
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or ['Shorts', 'AI', 'Automation'],
            'categoryId': '22' # 22 = People & Blogs (Change as needed)
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
            
    print(f"\n✅ Video Uploaded Successfully! Video ID: {response['id']}")
    print(f"Link: https://youtu.be/{response['id']}")
    return response['id']