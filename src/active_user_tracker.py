import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import settings
import heapq

class ActiveUserTracker:
    def __init__(self):
        self.user_activity = [] # Min heap based on activity
        self.user_map = {} # Maps username to (activity, username, user_id) tuple in the heap

    def update_activity(self, username, user_id, activity):
        if username in self.user_map:
            # Remove old entry if user exists
            self.user_activity.remove(self.user_map[username])
            heapq.heapify(self.user_activity)
        elif len(self.user_activity) >= 100:
            # Remove least active user
            heapq.heappop(self.user_activity)
        
        # Add or update user activity
        if username not in settings.IGNORE_USERS:
            new_entry = (activity, username, user_id)
            heapq.heappush(self.user_activity, new_entry)
            self.user_map[username] = new_entry

    def get_top_users(self):
        # Return usernames sorted by activity
       return [(username, user_id) for _, username, user_id in sorted(self.user_activity, reverse=True)] 
   
    def get_user_id(self, username):
        if username in self.user_map:
            _, _, user_id = self.user_map[username]
            return user_id
        return None
    
    def get_usernames(self):
        return list(self.user_map.keys())
