# AMANI - Game Design Document
**Version 1.0 | August 11, 2025**

---

## SECTION 1: EXECUTIVE SUMMARY

- **Game Title**: Amani (أماني - "Wishes" in Arabic)
- **Version**: 1.0 (August 11, 2025)
- **Platform**: WebGL (Desktop/Mobile Browser)
- **Target Audience**: Primary: Ages 13-35 casual gamers | Secondary: Arabic learners
- **Development Timeline**: 4-6 weeks MVP to market
- **Team Size**: Solo Developer with AI assistance

**Elevator Pitch**: Amani is a culturally-rich endless flyer that combines addictive Flappy Bird mechanics with stunning Saudi Arabian aesthetics. Players navigate a magical falcon through traditional architectural landscapes, collecting Arabic letters that unlock cultural rewards and boost scores.

---

## SECTION 2: GAME OVERVIEW

### 2.1 Concept Statement
Amani transforms the proven Flappy Bird formula into a celebration of Saudi heritage. Players control a majestic falcon soaring through iconic landscapes—from ancient Diriyah ruins to modern Riyadh skylines—while naturally learning Arabic letters through rewarding collection mechanics that enhance gameplay rather than interrupt it.

### 2.2 Core Pillars
1. **Addictive Simplicity**: One-touch gameplay that's instantly accessible but endlessly challenging
2. **Cultural Celebration**: Authentic Saudi aesthetics that educate through immersion, not instruction
3. **Social Competition**: Leaderboards and achievements that drive retention and viral sharing

### 2.3 Genre & Influences
- **Primary Genre**: Endless Runner/Flyer
- **Secondary Genre**: Casual Arcade with Cultural Elements
- **Key Influences**: 
  - Flappy Bird (core mechanics)
  - Alto's Adventure (aesthetic beauty)
  - Jetpack Joyride (power-ups and progression)
  - Monument Valley (cultural design inspiration)

---

## SECTION 3: GAMEPLAY

### 3.1 Core Loop
```
[Tap to Flap] → [Navigate Obstacles] → [Collect Letters] → [Score Points] → [Unlock Rewards] → [Compare with Friends] → [Retry for Higher Score]
```

**Session Goals:**
- 30 seconds: Beat previous high score
- 2 minutes: Unlock new cultural element
- 5 minutes: Complete daily challenge
- 15 minutes: Master new landscape theme

### 3.2 Controls
| Input | Action | Context |
|-------|--------|---------|
| Tap/Space | Falcon flaps upward | Always available |
| Hold | Extended glide (power-up) | When glide boost active |
| Swipe Up | Emergency dodge (limited) | When dodge power-up collected |

### 3.3 Player Progression
- **Short-term (30 seconds)**: Score points, collect letters, avoid obstacles
- **Medium-term (2 minutes)**: Chain letter collections for multipliers, activate power-ups
- **Long-term (15 minutes)**: Unlock new landscapes, complete cultural collections, achieve mastery ranks

---

## SECTION 4: MECHANICS

### 4.1 Movement System
- **Type**: Physics-based flapping with gravity
- **Speed**: Constant horizontal velocity (adjustable by difficulty)
- **Flap Force**: Consistent upward impulse on tap
- **Special Abilities**: 
  - Glide Boost: Reduces gravity temporarily
  - Swift Flight: Increases horizontal speed
  - Letter Magnet: Attracts nearby Arabic letters

### 4.2 Obstacle System
**Traditional Architecture Obstacles:**
- **Minaret Towers**: Vertical gaps requiring precise timing
- **Palm Fronds**: Swaying obstacles with dynamic hitboxes  
- **Desert Winds**: Invisible force affecting falcon trajectory
- **Sand Dunes**: Rolling terrain obstacles
- **Market Banners**: Horizontal obstacles requiring ducking

**Difficulty Scaling:**
- Gap size decreases every 10 points
- Obstacle frequency increases every 25 points
- Wind effects intensify at score milestones

### 4.3 Collection & Scoring System
**Arabic Letters (28 total)**
- **Common Letters** (ا، ل، م): 1 point, spawn frequently
- **Uncommon Letters** (ص، ض، ط): 3 points, moderate spawn rate
- **Rare Letters** (ظ، غ، خ): 5 points, rare spawns with special effects

**Scoring Mechanics:**
- Base obstacle: 1 point
- Letter collection: Variable points + multiplier building
- Perfect runs (no collisions for 10 obstacles): 2x multiplier
- Cultural combo (collecting letters spelling a word): 10x multiplier burst

**Cultural Word System:**
- Common words: سلام (Salam - Peace), حب (Hubb - Love)
- Moderate words: صديق (Sadiq - Friend), عائلة (Aila - Family)  
- Rare words: أماني (Amani - Wishes), وطن (Watan - Homeland)

---

## SECTION 5: GAME ELEMENTS

### 5.1 Characters
| Name | Role | Abilities | Cultural Significance |
|------|------|-----------|----------------------|
| Amani the Falcon | Player Character | Flight, Collection, Power-up usage | National bird of Saudi Arabia |
| Desert Wind Spirit | Environmental Guide | Provides hints through wind patterns | Traditional folklore element |

### 5.2 Power-ups & Collectibles
| Item | Purpose | Duration | Cultural Design |
|------|---------|----------|-----------------|
| Golden Dates | Shield from one collision | Single use | Traditional hospitality symbol |
| Incense Smoke | Slows time briefly | 3 seconds | Religious and cultural practice |
| Falcon Feather | Extra life | Single use | Connection to player character |
| Magic Carpet | Glide boost | 5 seconds | Arabian folklore reference |
| Arabic Coffee | Speed boost | 4 seconds | Cultural hospitality symbol |

### 5.3 Environmental Elements
| Element | Behavior | Challenge Level | Cultural Context |
|---------|----------|----------------|------------------|
| Minaret Spires | Static vertical obstacles | Medium | Islamic architecture |
| Palm Trees | Swaying with wind patterns | Easy-Medium | Desert oasis imagery |
| Market Stalls | Horizontal moving obstacles | Medium-Hard | Traditional souks |
| Sand Storms | Screen obscuring effect | Hard | Desert environment |
| Geometric Patterns | Background aesthetic elements | Visual only | Islamic art tradition |

---

## SECTION 6: LEVELS/WORLD

### 6.1 World Structure
- **Progression Type**: Seamless endless world with thematic biome transitions
- **Total Biomes**: 5 unlockable landscapes
- **Unlock Conditions**: Score thresholds and cultural collection milestones

**Biome Progression:**
1. **Desert Oasis** (0-100 points): Tutorial area with palm trees and simple gaps
2. **Ancient Diriyah** (100-300 points): Historic mud-brick architecture and narrow passages
3. **Modern Riyadh** (300-600 points): Glass towers and contemporary obstacles
4. **Red Sea Coast** (600-1000 points): Coastal cliffs and maritime elements  
5. **Empty Quarter** (1000+ points): Extreme desert with rare letter spawns

### 6.2 Level Design Philosophy
**Progressive Difficulty Curve:**
- **Tutorial Integration**: First 30 seconds teach through environmental design
- **Skill Building**: Gradual introduction of new obstacle types
- **Mastery Testing**: High-score runs require perfect execution of all learned skills
- **Cultural Discovery**: Each biome introduces new Arabic letters and cultural elements naturally

**Pacing Strategy:**
- 10 seconds: Player comfort zone establishment
- 30 seconds: First challenge introduction
- 60 seconds: Skill combination requirements
- 120+ seconds: Mastery-level precision demands

---

## SECTION 7: USER INTERFACE

### 7.1 HUD Elements
- **Score Counter**: Top center, large Arabic numerals with English translation, updates immediately
- **Cultural Progress**: Top left, shows current letter collection streak and multiplier
- **Lives/Shields**: Top right, visual representation of protective power-ups
- **Letter Collection Display**: Bottom center, shows recently collected letters with brief Arabic pronunciation

### 7.2 Menu Systems
**Main Menu:**
- Play button (primary action)
- Cultural Gallery (unlocked content showcase)
- Leaderboards (social comparison)
- Settings (audio, graphics, language)
- Daily Challenges (retention feature)

**Pause Menu:**
- Resume (large, center)
- Restart (medium)
- Main Menu (small)
- Cultural Tip (contextual learning moment)

**End Game Screen:**
- Final Score (prominent display)
- New Letters Learned (cultural progress)
- Best Score Comparison
- Share Achievement (social features)
- Play Again (primary action)
- View Gallery (secondary action)

### 7.3 Mobile Optimization
- Minimum touch target: 44px × 44px
- Swipe gestures for menu navigation
- Haptic feedback for collisions and collections
- Adaptive UI scaling for different screen ratios
- Portrait orientation lock for consistent experience

---

## SECTION 8: ART & AUDIO

### 8.1 Visual Style Guide
**Art Direction**: Traditional Saudi Heritage with Modern Polish
- **Color Palette**: 
  - Primary: Desert gold (#D4AF37), Sky blue (#87CEEB)
  - Secondary: Sunset orange (#FF6B35), Palm green (#228B22)
  - Accent: Royal purple (#6B46C1), Warm sand (#F4E4BC)
- **Visual Elements**:
  - Geometric Islamic patterns as background textures
  - Authentic architectural silhouettes
  - Flowing Arabic calligraphy for UI elements
  - Particle effects inspired by sand and incense smoke

**Asset Requirements for Scenario AI Generator:**
- Detailed falcon character with cultural decoration
- Authentic Saudi architectural obstacle sets
- Traditional pattern overlays and backgrounds
- Arabic letter collectibles with golden highlights
- Power-up items styled as cultural artifacts

### 8.2 Audio Direction
**Music Style**: Traditional Arabic instruments with modern ambient layers
- **Oud and Qanun**: Melodic leads creating emotional connection
- **Ambient Layers**: Desert winds, distant calls to prayer (respectful)
- **Adaptive Music**: Intensity increases with score milestones

**SFX Categories:**
- **Gameplay**: Satisfying flap sounds, collision feedback, collection chimes
- **Cultural**: Subtle Arabic pronunciation on letter collection
- **Environmental**: Wind ambience, architectural echo effects
- **UI**: Traditional instrument stingers for menu interactions

**Audio Implementation Priority:**
1. Core gameplay feedback (flap, collision, collection)
2. Ambient environmental soundscape
3. Cultural audio elements (pronunciation guides)
4. Musical score and adaptive systems

---

## SECTION 9: TECHNICAL SPECIFICATIONS

### 9.1 Performance Targets
- **Platform**: Unity WebGL 2021.3 LTS
- **Resolution**: 1920×1080 desktop, responsive mobile scaling
- **Target FPS**: 60 FPS consistent
- **Build Size**: <25MB compressed for web delivery
- **Load Time**: <10 seconds initial load, <2 seconds restart

### 9.2 Unity Configuration
**Render Pipeline**: Universal Render Pipeline (URP) for mobile optimization
- Post-processing: Minimal bloom and color grading only
- Shadows: Disabled for performance
- Anti-aliasing: FXAA for quality/performance balance

**Physics Settings**:
- 2D Physics only
- Collision layers: Player, Obstacles, Collectibles, Ground
- Continuous collision detection for player character
- Physics timestep: Fixed at 0.02 (50Hz)

**Input System**: New Input System with touch and keyboard support
- Touch input with gesture recognition
- Keyboard fallback for desktop testing
- Haptic feedback integration for mobile devices

**Audio System**: Unity Audio with spatial audio disabled for performance
- Compressed audio assets (OGG Vorbis)
- Audio source pooling for SFX management
- Dynamic music system with seamless loops

### 9.3 Optimization Strategies
**Memory Management:**
- Object pooling for all recyclable elements (obstacles, collectibles, particles)
- Texture atlasing for UI and small objects
- Mesh compression for 3D architectural elements
- Audio compression optimized for mobile bandwidth

**Rendering Optimization:**
- UI Canvas optimization with render mode considerations
- Particle system limits and LOD implementation
- Culling for off-screen obstacle management
- Batching for repeated architectural elements

---

## SECTION 10: MONETIZATION & ANALYTICS

### 10.1 Business Model
**Primary**: Free-to-play with ethical monetization
- **Cultural Content Packs**: Premium biomes and themes ($1.99 each)
- **Cosmetic Falcon Skins**: Traditional patterns and colors ($0.99-2.99)
- **Progress Boosters**: Letter collection multipliers (earn or purchase)
- **Ad Integration**: Rewarded video ads for extra lives and bonuses

**Retention Strategy:**
- Daily challenges with cultural themes
- Weekly cultural learning milestones
- Social leaderboards with friend comparisons
- Seasonal events celebrating Saudi holidays

### 10.2 Analytics Implementation
**Key Performance Indicators:**
- Day 1, 7, 30 retention rates
- Average session length and frequency
- High score distribution analysis
- Cultural content engagement metrics
- Social sharing and viral coefficient

**Critical Events Tracking:**
- `session_start`: Game launch with device/platform data
- `obstacle_collision`: Failure analysis for difficulty balancing
- `letter_collected`: Cultural engagement and learning progress
- `power_up_used`: Player strategy and monetization opportunities
- `high_score_achieved`: Progression milestones and retention correlation
- `cultural_word_completed`: Educational outcome measurement
- `social_share`: Viral growth tracking
- `iap_conversion`: Monetization funnel analysis

**Funnel Analysis:**
1. Game Discovery → Install (external marketing)
2. Install → First Play (onboarding effectiveness)
3. First Play → First Score >10 (core engagement)
4. First Score >10 → Day 2 Return (initial retention)
5. Day 2 Return → Week 1 Active (medium-term engagement)
6. Week 1 Active → First Purchase (monetization conversion)

---

## SECTION 11: MVP DEFINITION

### 11.1 Core Features (Week 1-2)
**Essential Gameplay:**
- [ ] Flappy Bird core mechanics with responsive controls
- [ ] Physics-based falcon flight with satisfying feedback
- [ ] Basic obstacle generation (minarets and palm trees)
- [ ] Score system with persistent high score storage
- [ ] Arabic letter collection with point values

**Visual Foundation:**
- [ ] Desert Oasis biome (first environment)
- [ ] Basic falcon character with animation
- [ ] Essential UI (score, basic menu system)
- [ ] Core audio (flap sounds, collection chimes, basic music)

**Technical Infrastructure:**
- [ ] WebGL build optimization and deployment
- [ ] Mobile touch input implementation
- [ ] Basic analytics integration (session tracking)
- [ ] Save system for high scores and progress

### 11.2 Enhanced Features (Week 3-4)
**Expanded Gameplay:**
- [ ] Power-up system (3 core power-ups minimum)
- [ ] Cultural word recognition and bonus system
- [ ] Ancient Diriyah biome (second environment)
- [ ] Difficulty scaling and challenge progression

**Polish & Engagement:**
- [ ] Particle effects and visual polish
- [ ] Enhanced audio design with cultural elements
- [ ] Social features (basic leaderboard)
- [ ] Daily challenge system foundation

**Cultural Integration:**
- [ ] Arabic letter pronunciation audio
- [ ] Cultural gallery for unlocked content
- [ ] Traditional Saudi visual elements integration
- [ ] Contextual cultural information delivery

### 11.3 Advanced Features (Week 5-6)
**Complete Experience:**
- [ ] All 5 biomes implemented and balanced
- [ ] Complete Arabic letter collection system (28 letters)
- [ ] Advanced power-up combinations and strategies
- [ ] Comprehensive cultural word database
- [ ] Social sharing and viral features

**Monetization Integration:**
- [ ] Ethical IAP system implementation
- [ ] Rewarded video ad integration
- [ ] Premium content unlock system
- [ ] Analytics dashboard for performance monitoring

### 11.4 Post-Launch Features (Future Phases)
**Feature Candidates for Version 2.0:**
- Multiplayer racing modes: Real-time competition with friends
- Seasonal events: Ramadan themes, National Day celebrations
- Advanced cultural education: Mini-games for Arabic writing practice
- User-generated content: Custom obstacle course sharing
- Expanded regions: Other GCC countries and Middle Eastern themes

**Cut Features (Moved to Future):**
- Complex Arabic writing mechanics: Too educationally focused for Game-First approach
- Multiple character options: Resource-intensive for MVP timeline
- Voice-over narration: Localization complexity exceeds current scope
- Advanced social features: Friend systems and chat functionality

---

## SECTION 12: RISK ASSESSMENT

| Risk Category | Probability | Impact Level | Mitigation Strategy |
|---------------|-------------|--------------|-------------------|
| **Performance Issues on Mobile WebGL** | High | Critical | Early mobile testing, aggressive optimization, fallback quality settings |
| **Cultural Sensitivity Concerns** | Medium | High | Cultural consultant review, community feedback integration, respectful representation |
| **Monetization Balance** | Medium | High | A/B testing for pricing, player feedback analysis, ethical monetization guidelines |
| **Arabic Letter Recognition Difficulty** | Medium | Medium | Progressive difficulty curve, visual clarity testing, optional tutorial modes |
| **Market Saturation (Endless Runners)** | High | Medium | Strong cultural differentiation, superior polish, authentic representation |
| **Technical Scope Creep** | Medium | Medium | Strict MVP definition, feature prioritization matrix, weekly scope reviews |
| **Asset Generation Timeline** | Low | Medium | Early Scenario AI integration, batch processing, asset pipeline testing |
| **Cross-Platform Compatibility** | Low | Low | Unity WebGL standard deployment, comprehensive device testing |

**Mitigation Priorities:**
1. **Performance First**: Establish mobile benchmarks in week 1
2. **Cultural Authenticity**: Engage Saudi cultural advisors early
3. **Scope Management**: Weekly feature review and prioritization
4. **Technical Validation**: Prototype core mechanics before asset production

---

## SECTION 13: APPENDICES

### 13.1 Asset Requirements for Scenario AI Generator

**CHARACTER ASSETS:**
```
PRIMARY CHARACTER:
- Falcon "Amani" - Majestic Saudi falcon with cultural decorations
- Wing positions: Neutral, flapping up, flapping down, gliding
- Cultural details: Traditional Saudi patterns on wings, golden accents
- Expression variants: Focused, determined, celebratory
- Size variants: Normal gameplay, victory pose, menu display

STYLE REFERENCE: "Traditional Saudi falcon with geometric Islamic patterns, desert gold and royal blue color scheme, side-scrolling game character"
```

**ENVIRONMENT ASSETS:**
```
DESERT OASIS BIOME:
- Palm trees with swaying fronds (obstacle variations)
- Traditional water wells with decorative elements  
- Sand dune backgrounds with heat shimmer effects
- Oasis pools with reflection effects
- Desert flowers and vegetation clusters

ANCIENT DIRIYAH BIOME:
- Mud-brick minaret towers (various heights for obstacles)
- Traditional doorway arches and geometric windows
- Ancient wall fragments with weathering details
- Historical architectural elements as background layers
- Stone courtyard elements and traditional patterns

MODERN RIYADH BIOME:
- Glass skyscraper silhouettes with Islamic geometric overlays
- Contemporary minaret designs blending traditional and modern
- Urban palm tree arrangements
- Modern Arabic calligraphy building decorations
- City skyline background with cultural architectural elements

RED SEA COAST BIOME:
- Coral reef formations as underwater obstacles
- Traditional dhow boat silhouettes
- Coastal cliff formations with Arabic patterns
- Lighthouse structures with Islamic architectural details
- Seashell and marine life decorative elements

EMPTY QUARTER BIOME:
- Massive sand dune formations
- Desert wind visualization effects
- Rare oasis mirages and atmospheric effects
- Ancient caravan route markers
- Minimalist desert landscape with golden hour lighting

STYLE REFERENCE: "Saudi Arabian landscape environments, warm desert colors, traditional architecture mixed with natural elements, side-scrolling game backgrounds"
```

**COLLECTIBLE ASSETS:**
```
ARABIC LETTERS (28 unique):
- Each Arabic letter as golden, glowing collectible
- Traditional calligraphy styling with 3D depth
- Particle trail effects for rare letters
- Size hierarchy: Common (small), Uncommon (medium), Rare (large with special effects)
- Cultural pattern backgrounds for letter display

POWER-UP ITEMS:
- Golden dates (shield power-up) - realistic but stylized
- Incense burner with smoke effects (slow-time power-up)
- Falcon feather with golden shine (extra life)
- Magic carpet miniature (glide boost) with traditional patterns
- Arabic coffee pot (dallah) with steam effects (speed boost)

STYLE REFERENCE: "Traditional Saudi cultural items rendered as game collectibles, golden highlights, particle effects, game-ready 2D sprites"
```

**UI ELEMENTS:**
```
INTERFACE COMPONENTS:
- Arabic-English number displays with traditional styling
- Menu backgrounds with Islamic geometric patterns
- Button designs incorporating traditional Saudi motifs
- Progress bars styled as traditional architectural elements
- Cultural achievement badges with regional symbols

PARTICLE EFFECTS:
- Sand particle systems for collisions and movement
- Golden sparkle effects for letter collection
- Incense smoke simulation for power-ups
- Desert wind visualization with sand grain details
- Victory celebration effects with cultural symbols

STYLE REFERENCE: "Traditional Saudi Arabian UI design, geometric Islamic patterns, desert gold and blue color scheme, game interface elements"
```

### 13.2 Cultural Authenticity Guidelines

**Representation Standards:**
- All Arabic text reviewed by native speakers
- Cultural elements presented respectfully without stereotypes
- Historical accuracy for architectural references
- Islamic artistic principles respected in geometric patterns
- Avoid religious symbolism in gameplay mechanics

**Community Engagement Strategy:**
- Saudi cultural advisors for content review
- Regional beta testing with local players
- Feedback integration from Middle Eastern gaming community
- Educational partnership opportunities with cultural institutions

### 13.3 Technical Implementation Checklist

**Unity Project Setup:**
- [ ] Unity 2021.3 LTS with Universal Render Pipeline
- [ ] WebGL build settings optimized for mobile
- [ ] Input System configured for touch and keyboard
- [ ] Analytics SDK integration (Unity Analytics/custom)
- [ ] Audio system configured for compressed assets

**Performance Optimization:**
- [ ] Object pooling system for obstacles and collectibles
- [ ] Texture atlasing for UI and small objects
- [ ] Particle system LOD implementation
- [ ] Mobile-specific quality settings configuration
- [ ] Memory profiler integration for development

**Deployment Pipeline:**
- [ ] Automated build system for WebGL
- [ ] Asset compression and optimization scripts
- [ ] Version control integration with development workflow
- [ ] Testing pipeline for multiple devices and browsers
- [ ] Analytics integration for live performance monitoring

---

**Document Status**: Ready for Development
**Next Steps**: 
1. Asset generation via Scenario AI using provided specifications
2. Unity project initialization with technical requirements
3. Core gameplay prototype development
4. Cultural consultant engagement for authenticity review

*This living document will be updated weekly throughout development to reflect discoveries, scope changes, and community feedback integration.*