"""
Universal Niche Engine & Topic Search Discovery for Long Video Automation.
Supports all major video niches:
1. History & Ancient Civilizations
2. Science, Space & Cosmos
3. Finance, Wealth & Business Scandals
4. True Crime & Unsolved Mysteries
5. AI, Tech & Future Singularity
6. Philosophy, Stoicism & Psychology
7. Horror, Supernatural & Urban Legends
8. Health, Longevity & Human Biology
9. Geopolitics & World Curiosities
10. Pop Culture, Gaming & Lore
"""

NICHES = {
    "history": {
        "id": "history",
        "name": "History & Ancient Civilizations",
        "icon": "📜",
        "voice": "en-US-ChristopherNeural",
        "visual_style": "Historic 35mm film, volumetric dust, archaeological precision, chiaroscuro lighting, cinematic realism, 8k",
        "bgm_mood": "orchestral, ancient, epic, solemn",
        "hook_formula": "The forgotten event that changed world history in 24 hours.",
        "sample_topics": [
            {
                "title": "The Bronze Age Collapse: When Civilization Vanished",
                "hook": "In less than 50 years, every major superpower of the ancient world fell into smoke and ash. Why did nobody write down who attacked them?",
            },
            {
                "title": "The Library of Alexandria: What We Actually Lost",
                "hook": "We've all heard the myth that centuries of human knowledge burned in a single night. But the real story is much darker.",
            },
            {
                "title": "How Rome's Greatest Emperor Died in Obscurity",
                "hook": "He commanded an empire of 70 million people, yet in his final hours, he died completely alone in a freezing tent.",
            },
        ],
    },
    "space": {
        "id": "space",
        "name": "Science, Cosmos & Deep Universe",
        "icon": "🌌",
        "voice": "en-GB-RyanNeural",
        "visual_style": "Astrophotography, James Webb telescope rendering, cosmic nebulae, deep space void, bioluminescent celestial dust, ultra-wide 8k",
        "bgm_mood": "ambient synth, celestial, wondrous, vast",
        "hook_formula": "The cosmic anomaly that defies the laws of physics.",
        "sample_topics": [
            {
                "title": "The Bo tes Void: The Terrifying Emptiness in Space",
                "hook": "In a universe crowded with trillions of galaxies, astronomers found a hole 330 million light years across with virtually nothing inside.",
            },
            {
                "title": "What Happens If You Fall Into a Supermassive Black Hole?",
                "hook": "You wouldn't be crushed immediately. In fact, if the black hole is large enough, you might not even realize you crossed the point of no return.",
            },
            {
                "title": "The Great Attractor: What Is Pulling the Milky Way?",
                "hook": "Our entire galaxy is racing through space at 2 million kilometers per hour toward something we cannot see.",
            },
        ],
    },
    "finance": {
        "id": "finance",
        "name": "Finance, Corporate Thrillers & Wealth",
        "icon": "💰",
        "voice": "en-US-GuyNeural",
        "visual_style": "Corporate noir, luxury glass towers, Wall Street trading floors in rain, moody amber and obsidian tones, anamorphic lens flare",
        "bgm_mood": "tense, modern electronic, ticking clock, dark pulse",
        "hook_formula": "The secret transaction that triggered a multi-billion dollar collapse.",
        "sample_topics": [
            {
                "title": "How One Trader Destroyed a 233-Year-Old Bank",
                "hook": "Nick Leeson was only 28 years old when his hidden account brought down the oldest merchant bank in Great Britain.",
            },
            {
                "title": "The Untold Story of the $65 Billion Madoff Scheme",
                "hook": "For 40 years, the biggest financial fraud in human history operated in plain sight. Here is the exact spreadsheet trick he used.",
            },
            {
                "title": "How De Beers Convinced the World Diamonds Are Rare",
                "hook": "Diamonds are not rare, and until 1938, almost nobody bought engagement rings. This is the greatest marketing heist in history.",
            },
        ],
    },
    "crime": {
        "id": "crime",
        "name": "True Crime & Cold Cases",
        "icon": "🔍",
        "voice": "en-US-ChristopherNeural",
        "visual_style": "Desaturated crime scene cinematography, foggy midnight streets, rain-streaked windshields, moody tungsten streetlamps, eerie realism",
        "bgm_mood": "dark drone, suspenseful, subtle strings, ominous",
        "hook_formula": "The baffling disappearance where all evidence pointed in opposite directions.",
        "sample_topics": [
            {
                "title": "The Antwerp Diamond Heist: The Impossible Vault",
                "hook": "It was protected by 10 layers of security, seismic sensors, and a vault door with 100 million combinations. And they left without firing a single bullet.",
            },
            {
                "title": "The Mystery of the Mary Celeste: What Did the Crew See?",
                "hook": "In 1872, a ship was discovered sailing perfectly intact in the Atlantic. The breakfast was still on the table, but every single human had vanished.",
            },
            {
                "title": "The Watcher House: Who Was Stalking 657 Boulevard?",
                "hook": "Three days after closing on their dream home, the Broaddus family received an anonymous letter that made them abandon the house forever.",
            },
        ],
    },
    "tech": {
        "id": "tech",
        "name": "AI, Cybersecurity & Tech Futurism",
        "icon": "🤖",
        "voice": "en-US-JennyNeural",
        "visual_style": "Cybernetic neon accents, sleek minimalist server rooms, holographic data visualizations, hyper-modern Tokyo night aesthetic, 8k",
        "bgm_mood": "cyberpunk synthwave, kinetic, digital pulse, futuristic",
        "hook_formula": "The breakthrough technology that will make today's computers obsolete.",
        "sample_topics": [
            {
                "title": "The Day AI Wrote Its Own Language",
                "hook": "In a Facebook AI research lab, two experimental chatbots stopped speaking English and began communicating in a shorthand humans couldn't decode.",
            },
            {
                "title": "Quantum Supremacy: Why Current Encryption Will Break",
                "hook": "Every password, bank account, and nuclear launch code is protected by prime numbers that one new machine will factor in seconds.",
            },
            {
                "title": "Stuxnet: The First Digital Weapon That Caused Physical Destruction",
                "hook": "It was 15,000 lines of invisible code that physically spun uranium centrifuges until they shattered inside an underground bunker.",
            },
        ],
    },
    "psychology": {
        "id": "psychology",
        "name": "Stoicism, Psychology & Mind",
        "icon": "🧘",
        "voice": "en-US-ChristopherNeural",
        "visual_style": "Classical marble statues, dramatic chiaroscuro Rembrandt lighting, moody coastal waves crashing on dark rocks, contemplative warmth, 8k",
        "bgm_mood": "calm piano, deep atmospheric cello, contemplative, serene",
        "hook_formula": "The psychological rule that explains why most people self-sabotage.",
        "sample_topics": [
            {
                "title": "Marcus Aurelius: The Private Diary of Rome's Reluctant Emperor",
                "hook": "He never intended anyone to read his Meditations. These were the raw midnight journal entries of a man trying to survive power and grief.",
            },
            {
                "title": "The Dark Psychology of Influence: How Charisma Is Engineered",
                "hook": "Why do certain people command undivided respect the second they enter a room? Cognitive scientists pinpointed three subtle non-verbal cues.",
            },
            {
                "title": "The 100-Hour Rule: How Elite Performers Learn Anything Fast",
                "hook": "Malcolm Gladwell popularized the 10,000-hour rule, but modern neuroplasticity research proves mastery begins in the first 100 hours.",
            },
        ],
    },
    "horror": {
        "id": "horror",
        "name": "Horror, Folklore & Unsettling Tales",
        "icon": "👻",
        "voice": "en-GB-RyanNeural",
        "visual_style": "Grainy 16mm film horror aesthetic, dark woods shrouded in dense fog, abandoned institutional corridors, high shadow contrast, eerie",
        "bgm_mood": "dissonant strings, haunting wind, heartbeats, low thrums",
        "hook_formula": "The documented local legend that official records tried to cover up.",
        "sample_topics": [
            {
                "title": "The Town That Suffered Mass Hysteria in 1518",
                "hook": "In July 1518, a woman stepped into a Strasbourg street and began dancing uncontrollably. Within a month, hundreds joined her until their hearts gave out.",
            },
            {
                "title": "The Real Story Behind the Chernobyl Phantom Firefighters",
                "hook": "At 1:23 AM, reactor number four exploded. The men dispatched to the roof didn't know the blue beam of air was ionizing radiation tearing through their DNA.",
            },
            {
                "title": "The Mystery of the Silent Village: Anjikuni Lake",
                "hook": "In 1930, a fur trapper entered an Inuit village of 2,000 people. The fires were still smoldering, but every grave was empty and not a soul was found.",
            },
        ],
    },
    "health": {
        "id": "health",
        "name": "Health, Longevity & Biohacking",
        "icon": "🩺",
        "voice": "en-US-JennyNeural",
        "visual_style": "Crisp editorial medical imagery, microscopic cellular photography, sunlit clean natural environments, high key Scandinavian aesthetic",
        "bgm_mood": "uplifting, clear, acoustic, inspiring",
        "hook_formula": "The biological mechanism that accelerates aging without you noticing.",
        "sample_topics": [
            {
                "title": "The Science of Autophagy: How Your Cells Eat Themselves to Heal",
                "hook": "In 2016, a Nobel Prize was awarded for proving that your body can consume its own cellular debris to repair damaged tissues.",
            },
            {
                "title": "Why Modern Bread Is Making Millions Sick (It's Not Gluten)",
                "hook": "People with severe digestive issues in America travel to Italy or France and eat pasta without symptoms. What is really in the grain supply?",
            },
            {
                "title": "Sleep Deprivation: What Happens to the Brain After 48 Hours",
                "hook": "Your brain uses a specialized plumbing system to wash away beta-amyloid plaques while you sleep. Skip two nights, and the wash cycle fails.",
            },
        ],
    },
    "geopolitics": {
        "id": "geopolitics",
        "name": "Geopolitics & World Border Anomalies",
        "icon": "🌍",
        "voice": "en-US-GuyNeural",
        "visual_style": "High-detail satellite terrain mapping, geopolitical cartography, tactical war room graphics, aerial drone perspectives, crisp contrasts",
        "bgm_mood": "suspenseful march, investigative, energetic pulse",
        "hook_formula": "The tiny geographic chokepoint that controls 40% of world trade.",
        "sample_topics": [
            {
                "title": "The Malacca Dilemma: The Chokepoint China Fears Most",
                "hook": "A narrow strait between Malaysia and Indonesia is only 1.5 nautical miles wide, but 80% of China's oil imports pass through it.",
            },
            {
                "title": "Bir Tawil: The Unclaimed Land No Country On Earth Wants",
                "hook": "In an era where wars are fought over inches of dirt, there is an 800-square-mile desert between Egypt and Sudan that neither country will claim.",
            },
            {
                "title": "Why Kaliningrad Is Europe's Most Dangerous Border Enclave",
                "hook": "Deep inside NATO territory sits a heavily fortified Russian missile base that doesn't share a single border with the rest of Russia.",
            },
        ],
    },
    "gaming": {
        "id": "gaming",
        "name": "Gaming Lore & Pop Culture Breakdowns",
        "icon": "🎮",
        "voice": "en-US-GuyNeural",
        "visual_style": "Vibrant cinematic game renders, Unreal Engine 5 aesthetic, dynamic action framing, volumetric lens glows, hyper-detailed",
        "bgm_mood": "synthwave, epic orchestral gaming themes, electronic drive",
        "hook_formula": "The secret backstory hidden in the game files for 10 years.",
        "sample_topics": [
            {
                "title": "The Elden Ring Lore Nobody Understood On First Playthrough",
                "hook": "George R.R. Martin and Miyazaki hid the entire shattering of the Golden Order inside the flavor text of five forgotten weapons.",
            },
            {
                "title": "How One Glitch Almost Destroyed World of Warcraft in 2005",
                "hook": "The Corrupted Blood incident spread through virtual cities like a genuine biological plague, forcing CDC epidemiologists to study player behavior.",
            },
            {
                "title": "The Tragedy of Half-Life 2: What Actually Happened to Episode 3",
                "hook": "It was the most anticipated sequel in PC gaming history. Behind closed doors at Valve, a radical internal philosophy quietly killed it.",
            },
        ],
    },
}


def search_niche_ideas(keyword: str) -> list:
    """
    Intelligent Search & Topic Generator.
    Given any keyword or niche query, returns 4-6 viral video ideas with pre-engineered hooks.
    """
    keyword_clean = keyword.strip().lower()
    results = []

    # 1. Check direct niche matches
    for k, niche in NICHES.items():
        if (
            keyword_clean in k
            or keyword_clean in niche["name"].lower()
            or any(keyword_clean in t["title"].lower() for t in niche["sample_topics"])
        ):
            for t in niche["sample_topics"]:
                results.append(
                    {
                        "niche_id": k,
                        "niche_name": niche["name"],
                        "icon": niche["icon"],
                        "title": t["title"],
                        "hook": t["hook"],
                        "voice": niche["voice"],
                        "duration": 5,
                    }
                )

    # 2. Dynamic generation if generic keyword or no direct match
    if len(results) < 3:
        words = keyword.strip().title()
        results.extend(
            [
                {
                    "niche_id": "history",
                    "niche_name": "History & Lore",
                    "icon": "📜",
                    "title": f"The Untold Origin Story of {words}",
                    "hook": f"What most people believe about the beginning of {words} is completely backwards. The truth began in a forgotten controversy.",
                    "voice": "en-US-ChristopherNeural",
                    "duration": 5,
                },
                {
                    "niche_id": "finance",
                    "niche_name": "Business & Mystery",
                    "icon": "💰",
                    "title": f"The Dark Economics Behind {words}",
                    "hook": f"Behind {words} lies a multi-billion dollar mechanism that quiet insiders have guarded for decades.",
                    "voice": "en-US-GuyNeural",
                    "duration": 10,
                },
                {
                    "niche_id": "space",
                    "niche_name": "Deep Explainer",
                    "icon": "🌌",
                    "title": f"The Shocking Science of {words} Explained",
                    "hook": f"Recent discoveries about {words} just shattered a long-held scientific assumption. Here is what we found.",
                    "voice": "en-GB-RyanNeural",
                    "duration": 5,
                },
                {
                    "niche_id": "psychology",
                    "niche_name": "Psychology & Secrets",
                    "icon": "🧘",
                    "title": f"Why Everyone Misunderstands {words}",
                    "hook": f"Psychologists discovered that how you view {words} reveals a hidden cognitive blind spot shared by 90% of people.",
                    "voice": "en-US-JennyNeural",
                    "duration": 5,
                },
            ]
        )

    return results[:6]
