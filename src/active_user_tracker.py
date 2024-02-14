import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import settings
import heapq

class ActiveUserTracker:
    def __init__(self):
        self.user_activity = [] # Min heap based on activity
        self.user_map = {} # Maps username to (activity, username) tuple in the heap

    def update_activity(self, username, activity):
        if username in self.user_map:
            # Remove old entry if user exists
            self.user_activity.remove(self.user_map[username])
            heapq.heapify(self.user_activity)
        elif len(self.user_activity) >= 100:
            # Remove least active user
            heapq.heappop(self.user_activity)
        
        # Add or update user activity
        if username not in settings.IGNORE_USERS:
            new_entry = (activity, username)
            heapq.heappush(self.user_activity, new_entry)
            self.user_map[username] = new_entry

    def get_top_users(self):
        # Return usernames sorted by activity
        return [username for _, username in sorted(self.user_activity, reverse=True)]
 
