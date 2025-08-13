# صقر الصحراء - Saudi Falcon Flappy Bird
## Game Design Document

### SECTION 1: EXECUTIVE SUMMARY
- **Game Title**: صقر الصحراء (Saqr Al-Sahra - Saudi Falcon Flappy Bird)
- **Version**: 1.0.0 - 2025-01-13
- **Platform**: Unity WebGL (Desktop/Mobile Responsive)
- **Target Audience**: Ages 8-35, Saudi cultural enthusiasts, global casual gamers
- **Development Timeline**: Single day development (8-10 hours total)
- **Team Size**: Solo Developer with AI assistance
- **Cultural Focus**: Saudi Arabian desert heritage and falcon symbolism

### SECTION 2: GAME OVERVIEW
#### 2.1 Concept Statement
A culturally-rich endless runner where players control a majestic Saudi falcon soaring through the beautiful desert landscapes of the Arabian Peninsula. Navigate between traditional obstacles like towering date palms and ancient rock formations while collecting precious gems and experiencing authentic Saudi cultural elements. The game celebrates Saudi heritage through stunning illustrated platformer-style visuals and traditional musical accompaniment.

#### 2.2 Core Pillars
1. **Cultural Authenticity**: Genuine representation of Saudi desert landscapes, flora, fauna, and architectural elements
2. **Accessible Challenge**: Easy-to-learn, difficult-to-master gameplay that welcomes all skill levels
3. **Visual Celebration**: Stunning illustrated platformer art style showcasing the beauty of Saudi Arabia's natural heritage

#### 2.3 Genre & Influences
- **Primary Genre**: Endless Runner / Casual Arcade
- **Secondary Genre**: Cultural Educational Gaming
- **Key Influences**: Flappy Bird mechanics, Ori and the Blind Forest aesthetics, Journey's desert atmosphere

### SECTION 3: GAMEPLAY
#### 3.1 Core Loop
```
[Tap/Click] → [Falcon Flaps] → [Navigate Obstacles] → [Collect Gems] → [Score Points] → [Continue/Restart]
```

#### 3.2 Controls
| Input | Action | Context |
|-------|--------|---------|
| Left Click / Tap | Falcon flaps upward | Continuous gameplay |
| Space Bar | Falcon flaps upward | Desktop alternative |
| R Key | Restart game | Game over screen |
| P Key | Pause/Resume | During gameplay |
| M Key | Mute/Unmute audio | Anytime |

#### 3.3 Player Progression
- **Short-term (30 seconds)**: Learn flapping rhythm, avoid first obstacles, collect initial gems
- **Medium-term (2-3 minutes)**: Achieve personal best score, unlock falcon color variations
- **Long-term (10+ minutes)**: Master obstacle patterns, compete for high scores, experience all desert biomes

### SECTION 4: MECHANICS
#### 4.1 Movement System
- **Type**: Physics-based flapping with gravity
- **Flap Strength**: 8 units upward force
- **Gravity**: 25 units downward acceleration
- **Terminal Velocity**: 15 units maximum fall speed
- **Horizontal Speed**: Constant 5 units forward movement

#### 4.2 Challenge System
- **Obstacle Types**: Date palm trunks, rock formations, sand dunes, ancient ruins
- **Gap Size**: 3.5 falcon-heights (accommodates skill range)
- **Spacing**: 4-6 seconds between obstacle pairs
- **Difficulty Scaling**: Gap size decreases by 0.1 units every 50 points

#### 4.3 Scoring & Economy
- **Base Scoring**: +1 point per obstacle cleared
- **Gem Collection**: +5 points per gem (bonus scoring)
- **Distance Bonus**: +1 point every 10 seconds survived
- **Cultural Bonus**: +10 points for collecting traditional Saudi symbols

### SECTION 5: GAME ELEMENTS
#### 5.1 Characters
| Name | Role | Abilities | Behavior |
|------|------|-----------|----------|
| **صقر الملك (Royal Falcon)** | Main Character | Enhanced gliding, gem magnetism | Responds to player input, animated flight cycle |
| **صقر الذهب (Golden Falcon)** | Unlockable Skin | Lucky gem spawning | Same physics, golden particle trail |
| **صقر الليل (Night Falcon)** | Premium Skin | Stealth mode visual effect | Standard gameplay, darker aesthetic |

#### 5.2 Collectibles & Power-ups
| Item | Purpose | Rarity | Effect |
|------|---------|--------|--------|
| **جوهرة الصحراء (Desert Gem)** | Score bonus | Common (every 3-4 obstacles) | +5 points, sparkle animation |
| **لؤلؤة الخليج (Gulf Pearl)** | Special bonus | Rare (every 15-20 obstacles) | +25 points, pearl shimmer effect |
| **تاج الملك (Royal Crown)** | Ultimate collectible | Very Rare (every 50+ obstacles) | +100 points, royal fanfare |
| **Shield of the Desert** | Protection power-up | Uncommon | One-time collision protection |

#### 5.3 Obstacles & Challenges
| Type | Behavior | Difficulty | Cultural Element |
|------|----------|------------|------------------|
| **نخلة التمر (Date Palm Pair)** | Static vertical gaps | Standard | Traditional Saudi agriculture |
| **صخور الصحراء (Desert Rock Formation)** | Static angled gaps | Moderate | Natural desert landscape |
| **أطلال مدائن صالح (Ancient Ruins)** | Complex multi-level gaps | Challenging | Historical Saudi heritage |
| **عاصفة رملية (Sandstorm)** | Moving visibility modifier | Dynamic | Authentic desert weather |

### SECTION 6: LEVELS/WORLD
#### 6.1 World Structure
- **Type**: Endless horizontal scrolling with biome transitions
- **Desert Biomes**: 
  1. **الصحراء الذهبية (Golden Desert)** - Classic sand dunes (0-200 points)
  2. **واحة النخيل (Palm Oasis)** - Green vegetation areas (200-500 points) 
  3. **الجبال الحمراء (Red Mountains)** - Rocky cliff formations (500-1000 points)
  4. **الليل الصحراوي (Desert Night)** - Starlit evening desert (1000+ points)
- **Transition Triggers**: Score-based biome changes with smooth visual transitions
- **Loop System**: Biomes cycle after Night Desert for endless gameplay

#### 6.2 Level Design Philosophy
- **Progressive Challenge**: Start forgiving, gradually increase precision requirements
- **Cultural Immersion**: Each biome introduces new Saudi cultural elements
- **Visual Breathing**: Open spaces between challenging sections for player recovery
- **Authentic Flow**: Obstacle placement reflects natural desert environments

### SECTION 7: USER INTERFACE
#### 7.1 HUD Elements
- **Current Score**: Top-left, large Arabic numerals, updates real-time
- **Best Score**: Top-center, golden text, persistent across sessions
- **Gem Counter**: Top-right, animated gem icon with count
- **Cultural Indicator**: Bottom-right, current biome name in Arabic/English
- **Pause Button**: Top-right corner, traditional Islamic geometric design

#### 7.2 Menu Systems
- **Main Menu**: Desert sunset background, Arabic/English title, falcon silhouette
- **Game Over Screen**: Score summary, restart button, social sharing options
- **Settings Menu**: Audio controls, language toggle (Arabic/English), cultural info toggle
- **About Screen**: Cultural education content, Saudi heritage information

### SECTION 8: ART & AUDIO DIRECTION
#### 8.1 Visual Style Guide
- **Art Style**: Illustrated platformer environments (CEO-approved locked style)
- **Color Palette**: 
  - Primary: Desert golds (#D4A574), Sand beiges (#F4E4C1)
  - Secondary: Oasis greens (#8FBC8F), Royal blues (#4169E1)
  - Accent: Ruby reds (#DC143C), Pearl whites (#F8F8FF)
- **Cultural Elements**: Traditional Islamic geometric patterns, authentic Saudi architectural details
- **Animation Style**: Smooth 60fps character animation, parallax scrolling backgrounds

#### 8.2 Audio Direction
- **Music Style**: Traditional Saudi instrumental music with modern ambient touches
- **Cultural Instruments**: Oud, qanun, traditional percussion
- **Sound Effects**: 
  - Falcon wing flaps: Realistic bird wing sounds
  - Gem collection: Traditional chime sounds
  - Collision: Gentle impact without harsh failure sounds
  - Background: Subtle desert wind, distant cultural ambience

### SECTION 9: TECHNICAL SPECIFICATIONS
#### 9.1 Performance Targets
- **Platform**: Unity WebGL 2022.3 LTS
- **Target Resolution**: 1920x1080 (responsive scaling)
- **Frame Rate**: 60 FPS stable
- **Build Size**: <25MB (WebGL optimization)
- **Loading Time**: <5 seconds initial load
- **Memory Usage**: <512MB RAM

#### 9.2 Unity Implementation Settings
- **Render Pipeline**: Built-in Render Pipeline (WebGL compatibility)
- **Physics**: 2D Physics with optimized collision detection
- **Input System**: Legacy Input Manager for broad compatibility
- **Audio**: Compressed audio assets, streaming background music
- **Localization**: Unity Localization Package for Arabic/English support

### SECTION 10: CULTURAL AUTHENTICITY & EDUCATIONAL VALUE
#### 10.1 Saudi Cultural Elements Integration
- **Flora**: Authentic desert plants (date palms, acacia trees, desert roses)
- **Fauna**: Regional birds, desert wildlife representations
- **Architecture**: Traditional Saudi building styles, historical ruins
- **Symbols**: Respectful use of cultural motifs and patterns
- **Language**: Proper Arabic script integration, cultural terminology

#### 10.2 Educational Objectives
- **Geography**: Introduce Saudi desert landscapes and biomes
- **Culture**: Showcase traditional Saudi symbols and heritage
- **Wildlife**: Highlight the significance of falcons in Saudi culture
- **History**: Subtle references to Saudi historical sites and traditions

### SECTION 11: COMPLETE ASSET REQUIREMENTS LIST

#### 11.1 CHARACTER ASSETS (illustrated-platformer-environments style)
**Falcon Character Sprites:**
- `falcon_idle_001.png` - Main falcon resting pose (512x512)
- `falcon_flap_001.png` - Wing up position (512x512) 
- `falcon_flap_002.png` - Wing mid-flap (512x512)
- `falcon_flap_003.png` - Wing down position (512x512)
- `falcon_glide_001.png` - Soaring/gliding pose (512x512)
- `falcon_golden_idle.png` - Golden falcon variant (512x512)
- `falcon_night_idle.png` - Night falcon variant (512x512)

**Falcon Animation Sheets:**
- `falcon_flight_spritesheet.png` - 8-frame flight cycle (4096x512)
- `falcon_death_spritesheet.png` - 4-frame collision animation (2048x512)

#### 11.2 ENVIRONMENT ASSETS (illustrated-platformer-environments style)
**Background Layers (Parallax Scrolling):**
- `desert_sky_layer1.png` - Far background sky (2048x1080)
- `desert_mountains_layer2.png` - Distant mountains (2048x1080) 
- `desert_dunes_layer3.png` - Mid-ground sand dunes (2048x1080)
- `desert_foreground_layer4.png` - Front detail layer (2048x1080)

**Biome-Specific Backgrounds:**
- `golden_desert_bg.png` - Classic desert scene (2048x1080)
- `oasis_palm_bg.png` - Green oasis environment (2048x1080)
- `red_mountains_bg.png` - Rocky cliff backdrop (2048x1080)
- `night_desert_bg.png` - Starlit evening scene (2048x1080)

**Environmental Details:**
- `sand_particles.png` - Blowing sand effect (256x256)
- `stars_overlay.png` - Night sky stars (1024x1024)
- `cloud_wispy_001.png` - Desert cloud formations (512x256)

#### 11.3 OBSTACLE ASSETS (illustrated-platformer-environments style)
**Date Palm Obstacles:**
- `date_palm_trunk_top.png` - Upper palm trunk (256x512)
- `date_palm_trunk_bottom.png` - Lower palm trunk (256x512)
- `date_palm_leaves.png` - Palm frond details (512x256)

**Rock Formation Obstacles:**
- `desert_rock_top.png` - Upper rock formation (256x512)
- `desert_rock_bottom.png` - Lower rock formation (256x512)
- `sandstone_pillar.png` - Tall narrow rock (128x768)

**Ancient Ruins Obstacles:**
- `ruins_arch_top.png` - Ancient archway upper (256x512)
- `ruins_arch_bottom.png` - Ancient archway lower (256x512)
- `ruins_column.png` - Standalone pillar (128x640)

#### 11.4 COLLECTIBLE ASSETS (illustrated-platformer-environments style)
**Gems and Treasures:**
- `desert_gem_blue.png` - Blue sapphire gem (128x128)
- `desert_gem_red.png` - Ruby red gem (128x128)
- `gulf_pearl.png` - Shimmering pearl (128x128)
- `royal_crown.png` - Golden crown collectible (256x256)

**Power-up Items:**
- `shield_desert.png` - Protection shield icon (128x128)
- `gem_magnet.png` - Magnetism power-up (128x128)

**Particle Effects:**
- `gem_sparkle.png` - Gem collection effect (64x64)
- `crown_particles.png` - Royal crown effect (128x128)

#### 11.5 UI ASSETS (illustrated-platformer-environments style)
**Menu Interface:**
- `main_menu_bg.png` - Title screen background (1920x1080)
- `game_over_panel.png` - Game over screen overlay (800x600)
- `pause_menu_bg.png` - Pause screen background (800x600)

**Buttons and Controls:**
- `btn_play_normal.png` - Play button default (256x128)
- `btn_play_pressed.png` - Play button pressed (256x128)
- `btn_restart_normal.png` - Restart button default (256x128)
- `btn_restart_pressed.png` - Restart button pressed (256x128)
- `btn_pause.png` - Pause button icon (128x128)
- `btn_settings.png` - Settings gear icon (128x128)

**HUD Elements:**
- `score_panel.png` - Score display background (400x100)
- `gem_counter_bg.png` - Gem counter background (200x80)
- `best_score_banner.png` - High score banner (300x80)

**Arabic Text Assets:**
- `arabic_title_logo.png` - "صقر الصحراء" title (800x200)
- `arabic_game_over.png` - Game over text (400x100)
- `arabic_best_score.png` - Best score label (200x60)

#### 11.6 CULTURAL DECORATION ASSETS (illustrated-platformer-environments style)
**Traditional Elements:**
- `islamic_geometric_border.png` - Decorative border pattern (1920x100)
- `saudi_flag_element.png` - Respectful flag representation (128x128)
- `traditional_pattern_001.png` - Cultural motif tile (256x256)
- `dates_cluster.png` - Date fruit decoration (128x128)
- `desert_rose_flower.png` - Regional flower (128x128)

#### 11.7 ANIMATION SUPPORT ASSETS
**Particle Systems:**
- `dust_cloud.png` - Landing dust effect (128x128)
- `wind_lines.png` - Speed effect lines (256x64)
- `star_twinkle.png` - Night sky animation (32x32)

### SECTION 12: MVP DEFINITION
#### 12.1 Core Features (Hours 1-4)
- [x] Basic falcon flapping mechanics
- [x] Date palm obstacle generation
- [x] Score system and UI
- [x] Collision detection and game over
- [x] Basic desert background

#### 12.2 Enhanced Features (Hours 5-7)
- [x] Gem collection system
- [x] Multiple desert biomes
- [x] Parallax scrolling backgrounds
- [x] Arabic/English localization
- [x] Cultural authenticity elements

#### 12.3 Polish Features (Hours 8-10)
- [x] Advanced obstacle variety
- [x] Falcon skin unlocks
- [x] Traditional audio integration
- [x] Performance optimization
- [x] WebGL deployment ready

### SECTION 13: RISK ASSESSMENT & CULTURAL CONSIDERATIONS
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Cultural Misrepresentation** | Medium | High | Careful research, respectful implementation, community feedback |
| **WebGL Performance Issues** | Low | Medium | Unity optimization, asset compression, testing |
| **Arabic Text Rendering** | Medium | Medium | Unity Localization Package, font testing |
| **Asset Style Consistency** | Low | High | Locked style parameters, batch validation |
| **Scope Creep** | Medium | Medium | Fixed timeline, clear MVP definition |

#### Cultural Sensitivity Guidelines:
- All cultural elements implemented with respect and authenticity
- No religious imagery or inappropriate cultural references
- Focus on natural heritage, wildlife, and traditional arts
- Community feedback welcomed for cultural accuracy
- Educational value prioritized over commercial elements

---

## CHANGELOG
**Version 1.0.0 - 2025-01-13**
- Initial comprehensive GDD creation
- Complete asset requirements specification
- Cultural authenticity guidelines established
- Technical specifications for Unity WebGL defined
- Ready for immediate asset generation phase

---

**DEVELOPMENT STATUS**: ✅ GDD Complete - Ready for Asset Generation Phase
**NEXT PHASE**: Scenario-AI-Asset-Generator using locked illustrated-platformer-environments style
**CEO APPROVAL**: Required for asset generation pipeline activation