# 🚀 Personal Portofolio Project - PBP '26  
This repository will be utilized to document and update my personal project over the course of the semester. Every phase of development, from initial setup to final deployment, will be maintained here.  

### Student Identity
**Name** : Rebecca Love Lianov Simanjuntak  
**NPM** : 2506637110  
**Class** : PBP KI  

## Setup Instructions
 
1. Clone the repository
```bash
   git clone <repo-url>
   cd <repo-folder>
```
2. Create and activate a virtual environment (optional but recommended)
```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
```
3. Install dependencies
```bash
   pip install django
```
4. Run the development server
```bash
   python manage.py runserver
```
5. Open `http://127.0.0.1:8000/` in your browser



### Assignment 1
## Outline
A single-page "About Me" portfolio built with plain HTML5 and CSS3 (Django template syntax used only for static file loading). The page includes:
 
- **Hero/Profile section** — name, NPM, program, photo, bio, and social links (Email, GitHub, LinkedIn)
- **Education section** — a responsive 3-card grid showcasing academic background, each card featuring a school logo, name, date range, and description, with a scrollable text area for longer descriptions

## Reflective Questions
1. Yes, I used semantic HTML5 elements throughout the page — `<header>`, `<nav>`, `<section>` (for the hero/profile and education sections), `<article>` (for each individual education card), `<figure>` (for the profile photo), and `<dl>`/`<dt>`/`<dd>` for the NPM/program metadata. Using `<section>` and `<article>` made the structure self-documenting: anyone reading the HTML can immediately tell that the education block is a distinct region of content, and that each school entry inside it is an independent, repeatable unit — which also made the CSS easier to write, since I could scope styles to `.education .edu-card` instead of relying on generic `<div>` classes with no inherent meaning. It also improves accessibility, since screen readers and browsers can use these landmarks for navigation.
2. One challenge was keeping the three education cards visually consistent as content length varied — different school names wrapped to different numbers of lines, which pushed the date and description text to different vertical positions across cards. I solved this with a Flexbox column layout (`display: flex; flex-direction: column`) combined with `align-items: stretch` on the grid, plus explicit `<br>` tags to control exactly how each title wraps, so all three cards share the same internal rhythm regardless of viewport width. Another challenge was the navbar: at smaller widths there wasn't enough horizontal room for the logo, the Home and About links, and the "View CV" button without everything cramming together or wrapping awkwardly. I evaluated each nav item by how essential it was versus how much space it demanded — the Home and About links pointed to sections already reachable by scrolling on a single-page site, so on mobile I prioritized keeping the brand logo and the CV button (a primary call-to-action) visible and hid the Home/About links below 480px rather than shrinking everything until it became unreadable. In general, my approach to reprioritizing elements for mobile was to ask which elements were purely navigational convenience versus which were core content or primary actions, and sacrifice the former first when space ran out.
3. Because the site is purely static, it can't store or update actual data — every project, skill, or education entry I want to add or edit requires directly modifying the HTML and pushing a new deploy, which doesn't scale well and isn't practical for content that needs to change often (e.g. a real-time list of projects, or a visitor message form). It also means there's no way to track engagement, receive messages directly through the site, or personalize content per visitor. In the next iteration, I'd most want to add a database-backed CMS layer (using Django's MVT architecture, which the tutorial hints is coming next) so I could manage portfolio content through an admin panel instead of hardcoding it, and add a working contact form that stores submissions rather than just triggering a `mailto:` link.
## AI Disclosure
 
AI tools were used to assist with this assignment. Full transparency below:
 
**Tools used:** Claude (Anthropic) and ChatGPT (OpenAI)
 
**What each tool was used for:**
 
- **Claude** — Used primarily for iterative CSS debugging and refinement of the Education section: fixing inconsistent card heights/alignment across the 3-card grid, implementing a Flexbox-based layout so card content (logo, title, date, description) lines up uniformly regardless of text length, adding responsive breakpoints at 768px and 480px, replacing a Unicode arrow character with a custom SVG icon, fixing a CSS specificity bug where an `<h3>` was inheriting the wrong color instead of `var(--paper)`, and implementing a custom-styled scrollable text area for long descriptions (including cross-browser scrollbar styling for Chrome/Edge/Safari and Firefox).
- **ChatGPT** — Used to debug an issue where the hero section's profile photo wasn't rendering (missing/broken image), and consulted for general design system guidance and UI/UX opinions — such as color palette pairing, typography choices, and layout feedback on the hero section.
**Prompting approach:** I worked iteratively — describing a visual problem (often with screenshots of the rendered page), receiving a proposed fix with an explanation of *why* the issue was happening (e.g. missing `min-height: 0` on a flex child preventing scroll instead of stretch, CSS specificity conflicts), testing it, and refining further based on how close the result was to my intended design. I did not accept AI output blindly — each suggested CSS change was tested in-browser and adjusted based on visual review before being kept.
 
**What I changed or fixed manually:** The decision to hide the Home/About nav links on mobile (rather than shrinking them further or stacking the navbar) was my own trade-off call, based on prioritizing the primary CV call-to-action over secondary same-page navigation. [Fill in any other manual edits — e.g. adjusting specific spacing/padding values to match your exact visual taste, writing your own bio and content copy, choosing your own color palette, any bugs the AI suggestions didn't fully resolve that you fixed yourself.]
 
**Critical reflection on AI limitations:** AI-suggested CSS occasionally required correction — for example, an initial scrollbar-hiding suggestion didn't fully suppress the native browser scroll buttons until `::-webkit-scrollbar-button { display: none }` was added explicitly, which wasn't included the first time. Suggested numeric values (like fixed card heights or breakpoint paddings) were also starting estimates that needed manual tuning to fit my actual content rather than being used as-is. This highlighted that AI is most useful for explaining *why* a CSS/layout bug occurs and proposing a structurally sound approach, but the specific values and final visual polish still required my own judgment and iteration.