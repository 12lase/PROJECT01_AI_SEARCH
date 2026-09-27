# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** Tio Oguntade
- **UID (netID):** togun9
- **UIN:** 670893152

---

## Section 1: Selected City Region
- **Selected Region:** Chicago Area, IL

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 35
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://project01-ai-search.onrender.com
- **Video Presentation Link:** [Provide an accessible link to your 5–7 minute video presentation]

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** UCS - Uniform Cost Search, since it guarantees the optimal path every time without needing any heuristic set up, and on a graph this small the extra nodes it expands compared to A* isn't really a big deal

- **Search Efficiency (Nodes expanded/time taken comparison):**

  Test route: Elgin, IL → Champaign, IL

  Greedy & DFS have the least number of nodes expanded as expected but had relatively high costs with DFS being the most at 346.86

  BFS & IDS costed more than greedy and also expanded more with IDS having the most as expected of 32, since it basically redoes the shallow layers over and over again every time it bumps the depth limit up

  A* & UCS work the best in this map scenario with moderate Node expansion and the lowest cost of 176.51

  A* works the best since there is a good Heuristic function it's using but UCS is the safest bet for a guarantee

  The time taken in this scenario has a lot more variables factoring in so it is not a good reflection of any efficiency differences between them

  | Algorithm | Cost (mi) | Nodes Expanded | Time Taken (ms) | Path |
  |---|---|---|---|---|
  | BFS | 279.33 | 13 | 0.039 | Elgin, IL → Rockford, IL → Peoria, IL → Bloomington, IL → Champaign, IL |
  | DFS | 346.86 | 6 | 0.026 | Elgin, IL → Rockford, IL → Peoria, IL → Springfield, IL → Decatur, IL → Champaign, IL |
  | UCS | 176.51 | 19 | 0.045 | Elgin, IL → Schaumburg, IL → Naperville, IL → Bolingbrook, IL → Joliet, IL → Kankakee, IL → Champaign, IL |
  | IDS | 279.33 | 32 | 0.033 | Elgin, IL → Rockford, IL → Peoria, IL → Bloomington, IL → Champaign, IL |
  | Greedy | 234.39 | 6 | 0.076 | Elgin, IL → DeKalb, IL → Aurora, IL → Joliet, IL → Bloomington, IL → Champaign, IL |
  | A* | 176.51 | 13 | 0.128 | Elgin, IL → Schaumburg, IL → Naperville, IL → Bolingbrook, IL → Joliet, IL → Kankakee, IL → Champaign, IL |

- **Link the idea of search algorithm to today Generative AI.** It matters a lot today cause of the massive amounts of data these large LLMs use - especially Neural Networks which are mapped in a graph like data structure where time and space complexities can exponentially rise. It is really important to use the right algorithm on data and a structure that uses it to maximize time, space and overall efficiency gains. A good real example is how LLMs generate text - greedy decoding just picks whatever next token looks best in the moment kind of like Greedy Best-First Search, while something like beam search keeps a few possible paths open at once instead of committing right away, which is closer to how A* balances cost so far against what looks promising instead of only going with what looks best right now
