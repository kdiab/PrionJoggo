## Design Document: Twitch Chat Bot for "Hot Potato" Game for Prison Joe

### Requirements and Functionality:
1. **Start Game:**
   - Listen for the channel point redemption "hot potato".
   - Upon redemption, mention one of the top 100 active users in the chat to start the game, give them the "hot potato".

2. **Passing the Potato:**
   - Implement logic to track who currently holds the potato.
   - Users can only pass the potato if they currently hold it.
   - Users must mention the user they want to pass the potato to, only the user holding the potato can pass it.
   - Introduce a configurable 5-second delay since the last pass has been done to prevent rapid passing of the potato.

3. **Game End:**
   - the game ends once the timer set at the start of the game is finished.
   - Upon reaching the end of the game duration, identify the user holding the hot potato.
   - Apply a timeout for the user holding the hot potato at the end of the game, lasting for X amount of time. This timeout prevents the user from participating in chat interactions for the specified duration.

4. **Game Management:**
   - Implement a mechanism to ensure that only one hot potato game can be active at a time within the channel.
   - Upon the start of a new hot potato game, check if there is already an active game in progress.
   - If a game is already active, prevent the start of a new game until the current game has ended.
   - Once the active game has ended, allow the start of a new game upon the next "hot potato" channel point redemption.

7. **Streamer Configuration:**
   - Allow streamer to configure various aspects of the game, such as the number of players required to start the game, the frequency of passing, or the visibility of game-related messages in the chat.

### Twitch Bot Setup:
1. **Authentication:**
   - Implement authentication with Twitch API to allow the bot to interact with the chat.

2. **Join Channel:**
   - Configure the bot to join the Twitch channel where the game will be played.

3. **Redemption Integration:**
   - Integrate with Twitch's Channel Point Redemption API to listen for "hot potato" redemptions.

### User Interaction:
1. **Mentioning Active Users:**
   - Retrieve a list of the top 100 active users in the Twitch chat and randomly select one to mention at the start of the game.

### Game Logic:
1. **Timing:**
   - Decide on the timing mechanics for passing the potato, such as setting a time limit between passes.
   - The game will last for X minutes, and the timer will start after the channel point has been redeemed.

2. **Elimination:**
   - Determine the conditions for eliminating a player (e.g., failing to pass the potato within the time limit).

### Error Handling:
1. **Connection Issues:**
   - Implement error handling for any potential connection issues with the Twitch chat.

2. **Redemption Errors:**
   - Handle errors related to channel point redemptions, such as if the redemption fails to trigger the start of the game.

### Testing:
1. **Unit Testing:**
   - Write unit tests to ensure each component of the bot functions as expected.

2. **Integration Testing:**
   - Test the bot's interaction with Twitch chat in a controlled environment to verify its functionality.

### Deployment:
1. **Hosting:**
   - Deploy the bot on a server to ensure it remains online and operational.

2. **Continuous Monitoring:**
   - Implement monitoring to detect and address any issues that may arise during runtime.

### Documentation:
1. **User Guide:**
   - Create a user guide explaining how to interact with the bot and play the game.

2. **Developer Guide:**
   - Document the bot's codebase and architecture for future maintenance and development.

---

This design document outlines the requirements and specifications for the implementation of the Twitch chat bot for the "hot potato" game for streamer PrisonJoe. 
