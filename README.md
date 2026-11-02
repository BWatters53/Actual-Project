# 🏹 Bobbin Dud

*A 2D medieval-themed platformer developed in Python using Pygame.*

## 📖 About the Project

**Bobbin Dud** is a 2D platformer being developed as part of my Computer Science A-Level project.

Inspired by games such as *Celeste* and *Donkey Kong Country Returns HD*, the game aims to combine challenging platforming mechanics, puzzle-solving elements and a retro medieval setting.

The player takes control of **Bobbin Dud**, a hero who must navigate increasingly difficult levels, defeat King John's guards, collect coins and overcome challenging enemies.

The game is being developed using **Python** and **Pygame**.

### 🎮 Inspirations & Resources

- **Celeste** – Inspiration for the movement mechanics and challenging platforming.
- **Donkey Kong Country Returns HD** – Inspiration for the level design, environments and visual style.
- **DaFluffyPotato** – Pygame tutorials and development inspiration. An absolute legend! https://www.youtube.com/@DaFluffyPotato

---

## 🚀 Success Criteria & Development Roadmap

The following success criteria outline the planned development of the game, from the initial physics prototype through to the completed game.

### Phase 1 – Core Gameplay & Physics

- [ ] **1. Basic Physics**
  - Implement gravity and collision detection.
  - Begin development with a single, simple test level.
  - Use Pygame rectangles to represent the player and environmental objects.
  - Create basic blocks and platforms to test the physics system.

- [ ] **2. Basic Motion & Moving Platforms**
  - Implement player movement and jumping.
  - Introduce special movement mechanics, including:
    - Wall-jumping.
    - Swinging.
    - Climbing.
  - Introduce interactive platforming objects, including:
    - Moving platforms.
    - Springs.
    - Collapsing roads.
  - Use differently coloured rectangles to distinguish special blocks during development.

### Phase 2 – Level Design & Progression

- [ ] **3. Level Editor & Scrolling Tilemap**
  - Develop a separate level editor.
  - Implement a tile-based map system.
  - Introduce scrolling functionality.
  - Allow levels to be designed and modified independently of the main game.

- [ ] **4. Multiple Levels**
  - Introduce multiple levels with progressively increasing difficulty.
  - Implement horizontal and vertical scrolling.
  - Create a camera system that follows the player.
  - Use the level editor to design maps and position start and end points.
  - Implement transitions between levels.

### Phase 3 – Enemies & Player Health

- [ ] **5. Basic Enemies**
  - Introduce basic enemies represented by red rectangles.
  - Implement periodic movement patterns.
  - Introduce melee and collision-based attacks.

- [ ] **6. Lives, HP & Banners**
  - Implement a player health (HP) system.
  - Display player health using an on-screen HP bar.
  - Allow enemy attacks to reduce player health.
  - Introduce a lives system.
  - Lives are lost when the player:
    - Falls off the map.
    - Loses all HP.
  - Display remaining lives using a banner in the top-left corner.
  - Reset the level when all lives are lost.

### Phase 4 – Graphics & World Design

- [ ] **7. Graphics Overhaul**
  - Replace the initial rectangle-based prototype graphics with fully designed sprites.
  - Introduce a retro medieval visual style.
  - Transform enemies into King John's guards.
  - Introduce the main character, Bobbin Dud.
  - Develop a consistent visual identity for the game.

- [ ] **8. Setting Overhaul**
  - Introduce parallax scrolling.
  - Add decorative and off-grid environmental components.
  - Expand the visual design of each level.
  - Allow environmental elements to be edited through the level editor.
  - Introduce environmental features such as:
    - Trees.
    - Clouds.
    - Bushes.
    - Villages.
  - Develop unique backgrounds and settings for different levels.

### Phase 5 – Combat & Rewards

- [ ] **9. Attacks for Bobbin Dud**

  Introduce two main combat systems:

  **Ranged Combat**
  - Bow and arrow.

  **Melee Combat**
  - Sword-fighting.

  - Implement appropriate attack mechanics and interactions with enemies.

- [ ] **10. Stealing from the Rich...**
  - Award points in the form of coins for defeating enemies.
  - Give greater coin rewards for defeating more difficult enemies.
  - Introduce a coin counter/banner at the top of the screen.
  - Use collected coins as the primary currency for the shop.

- [ ] **11. Animation**
  - Introduce character and enemy animations.
  - Add visual indicators when special abilities are being used.
  - Animate attacks and other important gameplay interactions.
  - Improve the overall fluidity of character movement.

- [ ] **12. Music & Sound Effects**
  - Introduce background music.
  - Add sound effects for movement, jumping, attacking and other gameplay events.
  - Introduce audio feedback for important interactions and events.

- [ ] **13. The Olde Shoppe**
  - Introduce a shop at the end of each level.
  - The shopkeeper will be a character inspired by Friar Tuck.
  - Allow players to exchange collected coins for power-ups.
  - Introduce purchasable upgrades, including:
    - Armour.
    - Strength boosts.
    - Speed boosts.

### Phase 6 – Advanced Enemies & Game Systems

- [ ] **14. New, Intelligent Enemies**
  - Introduce more complex and challenging enemies.
  - Develop larger enemies to act as bosses or particularly difficult opponents.
  - Implement a heuristics-operated King who fights Bobbin Dud.
  - Introduce proximity-activated knights on horseback.
  - Develop more advanced enemy behaviours and decision-making systems.

- [ ] **15. Accounts & Leaderboards**
  - Introduce player accounts.
  - Store player progress in local files.
  - Implement a graphical user interface (GUI) for account management.
  - Develop leaderboards to compare player statistics, including:
    - Highest level reached.
    - Number of jumps completed.
    - Fewest deaths.
    - Fastest completion time.

- [ ] **16. GUI Overhaul**
  - Develop a dedicated start screen featuring the game's title.
  - Introduce menu options for:
    - Playing the game.
    - Accessing the level editor.
    - Viewing leaderboards.
    - Accessing player accounts.
  - Introduce medieval-themed sword, shield and bow iconography.
  - Integrate the level editor directly into the main game.

### Phase 7 – Polish & Additional Features

- [ ] **17. Tutorials**
  - Introduce tutorials to teach new players the game's mechanics.
  - Use a side character, such as an animal or another Merry Man, to provide instructions.
  - Display instructions using signs held by the tutorial character.
  - Make tutorials passive or optional through the menu after the player has completed them for the first time.

- [ ] **18. Particles & Screenshake**
  - Introduce particle effects around the player during:
    - Spawning.
    - Movement.
    - Attacking.
    - Death.
  - Implement screenshake to emphasise important gameplay events.
  - Use visual effects to improve the overall responsiveness and immersion of the game.

- [ ] **19. ...Giving to the Poor**
  - Introduce opportunities for players to give collected money to the poor throughout levels.
  - Implement random reward chances when money is donated.
  - Allow donations to unlock different bonuses and power-ups.
  - Introduce an additional risk/reward mechanic that encourages exploration and interaction with the environment.

---
The bulk of this README.md was beautified via ChatGPT
