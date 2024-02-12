# HOT POTATO
### Game Duration:
1. **Game Length:**
   - Define the duration of the game in minutes (X minutes). The timer will start automatically after the "hot potato" channel point redemption has been successfully redeemed.

### Passing Mechanism:
1. **Emote-Based Passing:**
   - Specify a list of specific emotes that users must use to pass the potato. Only mentions accompanied by these emotes will be considered valid passes.

2. **Hot Potato Ownership:**
   - Implement logic to ensure that users must possess the hot potato to pass it. Users without the hot potato cannot initiate a pass.

### Timeout:
1. **User Timeout:**
   - Define the duration (X minutes) for which the user holding the hot potato at the end of the game will be timed out. This timeout should prevent the user from participating in chat interactions for the specified duration.

### Twitch Bot Behavior:
1. **Game Start Timer:**
   - Implement a timer that starts counting down the game duration immediately after the "hot potato" channel point redemption occurs.

2. **Emote Validation:**
   - Validate user mentions for passing the potato to ensure they include one of the specified emotes from the allowed list.

3. **Potato Ownership Check:**
   - Check if the user attempting to pass the potato actually possesses it. If not, notify them that they need to obtain the potato first.

4. **End of Game Handling:**
   - Upon reaching the end of the game duration, identify the user holding the hot potato and apply the specified timeout.

### User Experience:
1. **Notification:**
   - Notify users when they successfully pass the potato or when they attempt an invalid pass (e.g., without the required emote or without possessing the potato).

2. **Timeout Notice:**
   - Inform the user who receives the hot potato timeout about the reason for their timeout and its duration.

### Testing and Documentation:
1. **Testing for Timeout:**
   - Include testing scenarios to ensure that the user holding the potato at the end of the game receives the correct timeout.

2. **Documentation Update:**
   - Update the user guide and developer guide to reflect the new features and rules introduced by the additional requirements.
