instruction = """Address a question-answering task by interleaving Thought, Action, and Observation steps. 
Thought should evaluate the current context, while Action encompasses three types: 
(1) Search[entity]: Conduct a targeted search for the specified entity on Wikipedia and return the first paragraph if available; if not, suggest related entities for further exploration. 
(2) Finish[answer]: Provide the final answer and conclude the task. 
(3) Subtask[question]: Decompose the current task into simpler, parallel sub-tasks that can be executed independently to achieve results, without increasing the overall complexity. 
Additionally, utilize alternative actions as necessary.
Here are some examples.
{examples}

Question: {question}
Thought 1: 
"""

webthink_example = """
Question: Which is longer, the Yangtze River or the Yellow River?
Thought 1: To determine which river is longer, I need to gather information about the lengths of both the Yangtze River and the Yellow River.
Actions 1: ["Subtask[How long is the Yangtze River]", "Subtask[How long is the Yellow River]"]
Observation 1: Yangtze River is 6,300 km long Yellow River is 5,464 km long.
Thought 1: I have found the lengths of both rivers. The Yangtze River is 6,300 km long, while the Yellow River is 5,464 km long.
Actions 1: ["Finish[Yangtze River]"]

Quesiton: How long is the Yangtze River?
Thought 1: To determine the length of the Yangtze River, I need to search for information about its length.
Actions 1: ["Search[Yangtze River]"]
Observation 1: Yangtze or Yangzi (English:  /ˈjæŋtsi/ or /ˈjɑːŋtsi/ simplified Chinese: 长江; traditional Chinese: 長江; pinyin: Cháng Jiāng; lit. 'long river') is the longest river in Eurasia and the third-longest in the world. It rises at Jari Hill in the Tanggula Mountains of the Tibetan Plateau and flows 6,300 km (3,915 mi) in a generally easterly direction to the East China Sea.[8] It is the fifth-largest primary river by discharge volume in the world. Its drainage basin comprises one-fifth of the land area of China, and is home to nearly one-third of the country's population.[9]. The Yangtze has played a major role in the history, culture, and economy of China.
Thought 2: I have found the length of the Yangtze River. It is 6,300 km long.
Actions 2: ["Finish[Yangtze River is 6,300 km long]"]

Question: How long is the Yellow River?
Thought 1 To determine the length of the Yellow River, I need to search for information about its length.
Actions 1: ["Search[Yellow River]"]
Observation 1: The Yellow River[a] is the second-longest river in China and the sixth-longest river system on Earth, with an estimated length of 5,464 km (3,395 mi) and a watershed of 795,000 km2 (307,000 sq mi). Beginning in the Bayan Har Mountains, the river flows generally eastwards before entering the 1,500 km (930 mi) long Ordos Loop, which runs northeast at Gansu through the Ordos Plateau and turns east in Inner Mongolia. The river then turns sharply southwards to form the border between Shanxi and Shaanxi, turns eastwards at its confluence with the Wei River, and flows across the North China Plain before emptying into the Bohai Sea. The river is named for the yellow color of its water, which comes from the large amount of sediment discharged into the water as the river flows through the Loess Plateau.[1]. The Yellow River basin was the birthplace of ancient Chinese civilization.
Thought 2: I have found the length of the Yellow River. It is 5,464 km long.
Actions 2: ["Finish[Yellow River is 5,464 km long]"]


Question: Whether Genshin Impact and Black Myth: Wukong belong to the same country?
Thought 1: To determine if Genshin Impact and Black Myth: Wukong are from the same country, I need to find information about their origins and developers.
Actions 1: ["Subtask[What Genshin Impact belongs to]", "Subtask[What Black Myth: Wukong belongs to]"]
Observation 1: Genshin Impact is a Chinese game Black Myth: Wukong is a Chinese game.
Thought 2: I have found that both games, Genshin Impact and Black Myth: Wukong, are developed by companies based in China.
Actions 2: ["Finish[yes]"]

Question: What Genshin Impact belongs to?
Thought 1: To determine the origin of Genshin Impact, I need to search for information about the game.
Actions 1: ["Search[Genshin Impact]"]
Observation 1: Genshin Impact [a] is an action role-playing game developed and published by miHoYo (with publishing outside mainland China under Cognosphere, d/b/a HoYoverse). It was released for Android, iOS, PlayStation 4, and Windows in 2020, and for PlayStation 5 in 2021, with an Xbox Series X/S version coming in November 2024. The game features an anime-style open world environment and an action-based battle system using elemental magic and character-switching. A free-to-play game monetized through gacha game mechanics, Genshin Impact is updated regularly using the games as a service model.. Genshin Impact takes place in the fantasy world of Teyvat, home to seven nations, each of which is tied to a different element and ruled by a different god (archon).
Thought 2: I have established that miHoYo is a well-known Chinese game developer.
Actions 2: ["Finish[Genshin Impact is a Chinese game]"]

Question: What Black Myth: Wukong belongs to?
Thought 1: To determine the origin of Black Myth: Wukong, I need to search for information about the game.
Actions 1: ["Search[Black Myth: Wukong]"]
Observation 1: Black Myth: Wukong[a] is a 2024 action role-playing game developed and published by Game Science. The game is inspired by the classical Chinese novel Journey to the West and follows an anthropomorphic monkey based on Sun Wukong from the novel.. Black Myth: Wukong was released for PlayStation 5 and Windows on August 20, 2024, with an Xbox Series X/S version and an expansion planned for release. The game received generally favorable reviews from critics. It sold 18 million units within two weeks, making it one of the fastest-selling games of all time..
Thought 2: I have established that Black Myth: Wukong is developed by Game Science, now I need to confirm the background of Game Science.
Actions 2: ["Search[Game Science]"]
Observation 2: Game Science Interactive Technology Co., Ltd. (Chinese: 游戏科学; pinyin: Yóuxì Kēxué) is a Chinese video game development and publishing company known for its first internationally released premium game Black Myth: Wukong (2024). It is headquartered in Shenzhen with an additional office in Hangzhou.. In 2014, Game Science was founded in Shenzhen by seven ex-Tencent Games employees. They had previously worked on a free-to-play MMORPG called Asura Online which was based on The Legend of Wukong, an online novel adapted from Journey to the West.[1][2][3].
Thought 3: I have confirmed that Game Science is a Chinese company.
Actions 3: ["Finish[Black Myth: Wukong is a Chinese game]"]


Question: Were Scott Derrickson and Ed Wood of the same nationality?
Thought 1: To determine the nationality of Scott Derrickson and Ed Wood, I need to look into their backgrounds and find information about their origins.
Action 1: ['Subtask[What nationality is Scott Derrickson]', 'Subtask[What nationality is Ed Wood]']
Observation 1: Scott Derrickson is an American filmmaker Ed Wood is an American filmmaker.
Thought 2: I have found information on Scott Derrickson and Ed Wood's backgrounds and careers. Both of them are born in the United States.
Action 2: ['Finish[yes]']

Question: What nationality is Scott Derrickson?
Action 1: ['Search[Scott Derrickson]']
Observation 1: Scott Derrickson (born July 16, 1966) is an American filmmaker. He is best known for his work in the horror genre, directing films such as The Exorcism of Emily Rose (2005), Sinister (2012), and The Black Phone (2021). He is also known for the superhero film Doctor Strange (2016), based on the Marvel Comics character.. Scott Derrickson grew up in Denver, Colorado. He graduated from Biola University with a B.A.
Thought 2: I have found information on Scott Derrickson. He is an American filmmaker.
Action 2: ['Finish[Scoot Derrickson is an American filmmaker]']

Question: What nationality is Ed Wood?
Action 1: ['Search[Ed Wood]']
Observation 1: Edward Davis Wood Jr. (October 10, 1924 – December 10, 1978) was an American filmmaker, actor, and pulp novelist.. In the 1950s, Wood directed several low-budget science fiction, crime and horror films that later became cult classics, notably Glen or Glenda (1953), Jail Bait (1954), Bride of the Monster (1955), Plan 9 from Outer Space (1957) and Night of the Ghouls (1959).[1] In the 1960s and 1970s, he moved towards sexploitation and pornographic films such as The Sinister Urge (1960), Orgy of the Dead (1965) and Necromania (1971), and wrote over 80 lurid pulp crime and sex novels.. Notable for their campy aesthetics, technical errors, unsophisticated special effects, use of poorly-matched stock footage, eccentric casts, idiosyncratic stories and non sequitur dialogue, Wood's films remained largely obscure until he was posthumously awarded a Golden Turkey Award for Worst Director of All Time in 1980, renewing public interest in his life and work.[2]. Following the publication of Rudolph Grey's 1992 oral biography Nightmare of Ecstasy: The Life and Art of Edward D.
Thought 2: I have found information on Ed Wood. He is an American filmmaker.
Action 2: ['Finish[Ed Wood is an American filmmaker]']

Question: Are Giuseppe Verdi and Ambroise Thomas both Opera composers?
Thought 1: To determine if Giuseppe Verdi and Ambroise Thomas are both Opera composers, I need to know are they Opera composers respectively.
Actions 1: ['Subtask[Is Giuseppe Verdi an Opera composer]', 'Subtask[Is Ambroise Thomas an Opera composer]']
Observation 1: Giuseppe Verdi is an Italian composer Ambroise Thomas is a French composer.
Thought 2: I have found information on Giuseppe Verdi and Ambroise Thomas. They are both Opera composers respectively.

Question: Are Giuseppe Verdi Opera composer?
Thought 1: To determine if Giuseppe Verdi is an Opera composer, I need to search for information about him.
Action 1: ['Search[Giuseppe Verdi]']
Observation 1: Giuseppe Verdi was an Italian composer known for his operas, including La Traviata, Rigoletto, and Aida. He was born in 1813 and died in 1901.
Thought 2: I have found information on Giuseppe Verdi. He is an Opera composer.
Action 2: ['Finish[yes]']

Question: Are Ambroise Thomas Opera composer?
Thought 1: To determine if Ambroise Thomas is an Opera composer, I need to search for information about him.
Action 1: ['Search[Ambroise Thomas]']
Observation 1: Ambroise Thomas was a French composer known for his operas, including Mignon and Hamlet. He was born in 1811 and died in 1896.
Thought 2: I have found information on Ambroise Thomas. He is an Opera composer.
Action 2: ['Finish[yes]']
"""