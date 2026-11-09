# 🚀 Personal Portofolio Project - PBP '26  
This repository will be utilized to document and update my personal project over the course of the semester. Every phase of development, from initial setup to final deployment, will be maintained here.  

### Student Identity
**Name** : Rebecca Love Lianov Simanjuntak  
**NPM** : 2506637110  
**Class** : PBP KI  

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/beccaovels/myportofolio.git
cd myportofolio
```
2. Create and activate a virtual environment
```bash
python -m venv env
source env/bin/activate      # macOS / Linux
env\Scripts\activate         # Windows
```
3. Install the dependencies (Django, Django REST Framework, etc.)
```bash
pip install -r requirements.txt
```
4. Apply the migrations (local development uses SQLite; PostgreSQL is only used when `PRODUCTION=true` is set in `.env`)
```bash
python manage.py migrate
```
5. Create the portfolio owner account, then the roles
```bash
python manage.py createsuperuser
```
   Log in at `/admin/`, create a group named **`Editor`**, and add any account that should be allowed to edit skills.
6. Run the development server and open `http://127.0.0.1:8000/`
```bash
python manage.py runserver
```
7. Run the tests
```bash
python manage.py test main
```
   Use `test main` rather than plain `test`, so only this app's tests are collected.

## Weekly Progress
| Week | Topic | What was added |
|---|---|---|
| Assignment 1 | HTML & CSS | Static "About Me" page: hero/profile and education cards |
| Assignment 2 | Django MVT | `Education` model, views, templates, and unit tests |
| Assignment 3 | Forms & data delivery | New **Skills** section with `ModelForm` create/edit/delete, JSON/XML endpoints |
| Assignment 4 | Auth & roles | Register/login/logout, owner / Editor / user / visitor roles, stars |
| Assignment 5 | AJAX | Fetch-based list, debounced search, add modal, toasts, XSS protection |
| Tutorial 7 | Django REST Framework | Experience API (`/api/v1/experience/`) with serializer, permissions, tests |
| Assignment 6 | Django REST Framework | Skills API (`/api/v1/skills/`) for all four roles, PATCH edit modal, sort control, CSRF tests |

## Assignment 1
### Outline
A single-page "About Me" portfolio built with plain HTML5 and CSS3 (Django template syntax used only for static file loading). The page includes:
 
- **Hero/Profile section** — name, NPM, program, photo, bio, and social links (Email, GitHub, LinkedIn)
- **Education section** — a responsive 3-card grid showcasing academic background, each card featuring a school logo, name, date range, and description, with a scrollable text area for longer descriptions

### Reflective Questions
1. Yes, I used semantic HTML5 elements throughout the page — `<header>`, `<nav>`, `<section>` (for the hero/profile and education sections), `<article>` (for each individual education card), `<figure>` (for the profile photo), and `<dl>`/`<dt>`/`<dd>` for the NPM/program metadata. Using `<section>` and `<article>` made the structure self-documenting: anyone reading the HTML can immediately tell that the education block is a distinct region of content, and that each school entry inside it is an independent, repeatable unit — which also made the CSS easier to write, since I could scope styles to `.education .edu-card` instead of relying on generic `<div>` classes with no inherent meaning. It also improves accessibility, since screen readers and browsers can use these landmarks for navigation.
2. One challenge was keeping the three education cards visually consistent as content length varied — different school names wrapped to different numbers of lines, which pushed the date and description text to different vertical positions across cards. I solved this with a Flexbox column layout (`display: flex; flex-direction: column`) combined with `align-items: stretch` on the grid, plus explicit `<br>` tags to control exactly how each title wraps, so all three cards share the same internal rhythm regardless of viewport width. Another challenge was the navbar: at smaller widths there wasn't enough horizontal room for the logo, the Home and About links, and the "View CV" button without everything cramming together or wrapping awkwardly. I evaluated each nav item by how essential it was versus how much space it demanded — the Home and About links pointed to sections already reachable by scrolling on a single-page site, so on mobile I prioritized keeping the brand logo and the CV button (a primary call-to-action) visible and hid the Home/About links below 480px rather than shrinking everything until it became unreadable. In general, my approach to reprioritizing elements for mobile was to ask which elements were purely navigational convenience versus which were core content or primary actions, and sacrifice the former first when space ran out.
3. Because the site is purely static, it can't store or update actual data — every project, skill, or education entry I want to add or edit requires directly modifying the HTML and pushing a new deploy, which doesn't scale well and isn't practical for content that needs to change often (e.g. a real-time list of projects, or a visitor message form). It also means there's no way to track engagement, receive messages directly through the site, or personalize content per visitor. In the next iteration, I'd most want to add a database-backed CMS layer (using Django's MVT architecture, which the tutorial hints is coming next) so I could manage portfolio content through an admin panel instead of hardcoding it, and add a working contact form that stores submissions rather than just triggering a `mailto:` link.
### AI Disclosure
 
AI tools were used to assist with this assignment. Full transparency below:
 
**Tools used:** Claude Sonnet 5 - Medium (Anthropic) and ChatGPT (OpenAI)
 
**What each tool was used for:**
 
- **Claude** — Used primarily for iterative CSS debugging and refinement of the Education section: fixing inconsistent card heights/alignment across the 3-card grid, implementing a Flexbox-based layout so card content (logo, title, date, description) lines up uniformly regardless of text length, adding responsive breakpoints at 768px and 480px, replacing a Unicode arrow character with a custom SVG icon, fixing a CSS specificity bug where an `<h3>` was inheriting the wrong color instead of `var(--paper)`, and implementing a custom-styled scrollable text area for long descriptions (including cross-browser scrollbar styling for Chrome/Edge/Safari and Firefox).
- **ChatGPT** — Used to debug an issue where the hero section's profile photo wasn't rendering (missing/broken image), and consulted for general design system guidance and UI/UX opinions — such as color palette pairing, typography choices, and layout feedback on the hero section.
**Prompting approach:** I worked iteratively — describing a visual problem (often with screenshots of the rendered page), receiving a proposed fix with an explanation of *why* the issue was happening (e.g. missing `min-height: 0` on a flex child preventing scroll instead of stretch, CSS specificity conflicts), testing it, and refining further based on how close the result was to my intended design. I did not accept AI output blindly — each suggested CSS change was tested in-browser and adjusted based on visual review before being kept.
 
**What I changed or fixed manually:** The decision to hide the Home/About nav links on mobile (rather than shrinking them further or stacking the navbar) was my own trade-off call, based on prioritizing the primary CV call-to-action over secondary same-page navigation. [Fill in any other manual edits — e.g. adjusting specific spacing/padding values to match your exact visual taste, writing your own bio and content copy, choosing your own color palette, any bugs the AI suggestions didn't fully resolve that you fixed yourself.]
 
**Critical reflection on AI limitations:** AI-suggested CSS occasionally required correction — for example, an initial scrollbar-hiding suggestion didn't fully suppress the native browser scroll buttons until `::-webkit-scrollbar-button { display: none }` was added explicitly, which wasn't included the first time. Suggested numeric values (like fixed card heights or breakpoint paddings) were also starting estimates that needed manual tuning to fit my actual content rather than being used as-is. This highlighted that AI is most useful for explaining *why* a CSS/layout bug occurs and proposing a structurally sound approach, but the specific values and final visual polish still required my own judgment and iteration.

## Assignment 2
### Reflective Questions
1. When a user opens the Education page, the browser sends a GET request to
   `/education/`. Django's project-level `urls.py` (in the `myportofolio`
   package) receives the request first and matches the path against its
   `urlpatterns`, which includes `main.urls` via `include()`. The request is
   then handed to the app-level `main/urls.py`, where the path `"education/"`
   is matched to the `show_education` view via `name="show_education"`. The
   `show_education` view function runs: it queries the `Education` model
   with `Education.objects.all()`, retrieving every row from the database
   as a QuerySet, and places that QuerySet into a context dictionary along
   with static values like the page owner's name. The view then calls
   `render(request, "education.html", context)`, which loads the
   `education.html` template and passes it the context. Django's template
   engine evaluates the `{% for education in education_list %}` loop,
   rendering one `<article class="edu-card">` block per Education object
   (or the `{% empty %}` fallback message if the QuerySet is empty), and
   produces a final HTML string. This HTML is wrapped in an `HttpResponse`
   and sent back through the same chain to the browser, which parses and
   displays it.

2. Storing the data in a model instead of hardcoding it in the template
   keeps content and presentation separate. With a model, education
   history lives in the database as structured, typed data (CharField,
   DateField, etc.) with built-in validation, and can be created, updated,
   or removed through the Django admin or shell without touching any HTML.
   If the data were hardcoded, every new entry or edit would require
   modifying the template directly, risking broken markup and making the
   history hard to track in version control. Using a model also means the
   same data can be reused across multiple templates or exposed later
   through an API without duplication, and it scales cleanly — adding a
   filter, sort order, or search feature only requires changing the view's
   query, not rewriting HTML.

3. `makemigrations` inspects the current state of the models and generates
   migration files describing the schema changes needed to match them
   (e.g., new fields, altered types, new models) — it does not touch the
   actual database. `migrate` then applies those generated migration files
   to the real database, executing the SQL needed to bring its schema in
   line with the models. For example, adding a new `gpa = models.FloatField()`
   field to the `Education` model requires running `makemigrations` first
   to generate a migration file recording that a `gpa` column needs to be
   added, and then `migrate` to actually alter the `education` table in
   the database and add that column.

### AI Disclosure
**Tool used:** Claude Sonnet 5 - Medium (Anthropic)

**What it was used for:**
- Drafting the unit test suite (`EducationTest`) for the new Education page,
  covering the three required scenarios: URL/template accessibility, data
  rendering when non-empty, and the empty-state message.
- Structuring the reflective questions above based on my own project code
  (models.py, views.py, urls.py, education.html).

**Prompting strategy:**
I did not ask for a full solution upfront. I first uploaded the assignment
context and asked what files Claude would need to write accurate tests,
then supplied `models.py`, `views.py`, `urls.py`, `tests.py`, and
`education.html` so the generated tests matched my actual field names,
URL names, and template structure rather than generic placeholders. I ran
the generated tests myself locally after each suggestion rather than
assuming they were correct.

**Where AI output was wrong and had to be corrected:**
The first version of `test_empty_education_page_shows_empty_message`
included `self.assertNotContains(response, "Universitas Indonesia")` to
confirm no education record rendered. When I ran it, the test failed —
not because my Django code was broken, but because the site footer
("Fakultas Ilmu Komputer, Universitas Indonesia.") legitimately contains
that same string on every page, empty or not. I pasted the failing
traceback back to Claude, and rather than accepting a fix that changed
my production template just to make the test pass, I pushed back and
asked what the "best case" fix was. Claude's follow-up explained that the
test assertion — not the app — was too broad, and that changing static
site content to accommodate a test would be backwards. The fix was to
assert against `self.education.program` (a value unique to a rendered
education card, e.g. "S1 Ilmu Komputer KKI") instead of a substring that
collides with unrelated static footer text. This is the version I kept.

**What I verified myself:**
- Ran `python manage.py test` after every change and confirmed `OK` with
  9/9 tests passing before accepting any test code.
- Manually checked that the empty-state string returned by the assertion
  (`"No education records have been added yet."`) matches the exact text
  in `education.html`, since a mismatch would cause a false failure.
- Wrote the three reflective-question answers myself in my own words based
  on tracing the actual request flow through my `urls.py`/`views.py`, using
  Claude's draft only as a structural starting point.

**Prompting/chat log:**
Full conversation log available at: https://claude.ai/share/c8908741-3948-4e1d-a41e-3e2f127c3f7a

## Assignment 3
### Outline
Created a new section 'Skills' because I felt that the other sections I had on my website doesn't need a form mechanism and data delivery workflow. The implementation of ModelForm required in assignment-3 is better fit if I implement it in the Skills section as it would be efficient if I have a button that could easily add, delete, and edit skills (in comparison in implementing the mechanism in education, where I felt it would be more efficient if the admin add the data immediately).

### Reflective Questions
1. I used 'ModelForm' because it automatically generates form fields that
matches the model's schema - which saves time because then I don't need
to write repetitive HTML <input> tags and manual validation logic. The
mechanism natively handles data validation, rendering, and saving to the
database, making the development workflow much faster and cleaner. This 
mechanism also allows Django to automatically verify specific inputs, 
such as double-checking that a URL field actually contains a properly 
formatted web address. 

It is required to add {% csrf_token %} to protect the website from 
Cross-Site Request Forgery (CSRF) attack. This will insert a hidden, 
unique cryptographic token into the form, and when the form is submitted, 
Django will check if the token matches. If a malicious site/user tries to 
trick a user's browser into submitting a forged POST request to the 
server, the malicious request will fail because the attacker doesn't have 
the correct token.

2. JSON is preferred over XML because it is more readable to humans, but 
also faster for computers to parse. This is because JSON syntax maps 
directly to native data structures in JavaScript (a programming language 
used by modern websites), it integrates seamlessly into modern frontend 
web development without needing complex parsers. On the other hand, XML 
relies on heavy and verbose opening and closing tags, which increases 
payload sizes and processing time.

3. When a request hits the JSON view (e.g., `get_skills_json`), the view 
queries the database using Django's ORM (e.g., `Skill.objects.all()`) 
which returns a `QuerySet` of complex Python objects. It cannot send
Python objects directly over the internet over HTTP. It must perform 
**serialization** to translate these complex Django model objects into a 
universal text-based format (JSON) that can be transmitted via HTTP and 
understood by any client (like a web browser). Django's `serializers.
serialize("json", data)` converts the QuerySet into a JSON string, which 
is then wrapped in an `HttpResponse` with the `application/json` content 
type and sent back to the client.

### AI Disclosure

**Tool used:** Claude Sonnet 5 - Medium (Anthropic)

**What it was used for:**
- Refactoring the Skills section to use a modern, glassmorphic UI via the native HTML5 Popover API.
- Debugging overlapping/duplicate UI elements (e.g., when the delete modal's button accidentally rendered twice on the grid).
- Investigating why a Google Drive image was displaying a "white grid" background instead of true transparency.
- Unifying CSS font sizing and family inheritance across different HTML elements (`<a>` vs `<button>`).

**Prompting strategy:**
For the initial prompt, I used a highly structured and explicit strategy tailored specifically for Claude:
- **Being explicit and direct:** I avoided vague briefs and treated the AI like a new employee, giving clear constraints (e.g., "strictly HTML5/CSS, no JavaScript allowed").
- **Using XML tags:** I structured the context and rules using XML tags (like `<context>` and `<rules>`), which Claude reads very reliably.
- **Showing few-shot examples:** I provided diverse examples of the exact output format I wanted to prevent Claude from guessing the tone.
- **Breaking tasks into sequential steps:** I used bullet points to guide the AI through the multi-step reasoning for building the UI layout.
- **Setting guardrails:** I explicitly commanded the AI to stick to the rules and prevent hallucinations.
- **Prefilling the response:** I seeded the first few characters to lock in the output format.

This initial structured prompt was highly effective because it immediately locked Claude into the correct architectural constraints (pure HTML/CSS) and prevented it from generating bloated, out-of-scope solutions. From there, I worked iteratively by describing specific layout issues and visual bugs as they occurred in the browser. For instance, when the modal's close button wasn't working, I explained the exact behavior to the AI so it could trace the issue back to CSS positioning and `z-index`.
**What I changed or fixed manually (What advice I took vs rejected):**
The AI initially tried to solve the non-functional close button by adding a JavaScript fallback (`onclick="this.closest('[popover]').hidePopover()"`). I explicitly rejected this advice because the assignment rules strictly forbid JavaScript. I forced the AI to revert to a pure HTML5/CSS solution using the `popovertarget` attribute. I also manually directed the visual design, rejecting the AI's initial portrait-oriented modal and instructing it to restructure the layout into a wider, landscape-oriented rectangle to save vertical space.

**Critical reflection on AI limitations:**
The AI struggled significantly with the new HTML5 Popover API's default browser behaviors. When trying to style the modal, the AI blindly applied `display: flex;` to the `.skill-popover` class. This completely overrode the browser's native `display: none` rule for popovers, causing every single skill modal to render simultaneously on page load and blocking the screen. The AI failed to realize this until I explicitly pointed out that the popups were acting like they were hardcoded open. This highlighted that while AI is great at writing general CSS, it can easily break native browser functionality if it doesn't account for implicit User Agent stylesheets.

**Prompting/chat log:**
Full conversation log available at: https://claude.ai/share/62c55a60-9451-4f12-91ad-75a918078c70

## Assignment 4
### Reflective Questions
[Insert your answers for Assignment 4's reflective questions here]

### AI Disclosure

**Tool used:** Gemini Pro 3.1 - Low (Google)

**What it was used for:**
- Explaining how to manually test server-side access controls (HTTP 403 Forbidden and HTTP 302 Redirects) across four different user roles via the browser.
- Debugging a session state issue where attempting to trigger a 403 Forbidden error incorrectly resulted in a redirect to the `/login/` page.
- Clarifying the process of assigning regular users to the "Editor" group via the Django Admin panel and managing superuser credentials from the CLI.

**Prompting strategy:**
I used a contextual and iterative prompting strategy. Instead of asking the AI to write code for me, I provided the exact code I had already written (`@login_required` decorators, `PermissionDenied` logic, and my `register` view) and asked it to explain *how to test it*. When my manual testing failed (e.g., getting redirected to login instead of hitting a 403 error), I fed the exact behavioral mismatch back to the AI so it could trace the logical flow of the user journey rather than just analyzing the static syntax.

**What I changed or fixed manually (What advice I took vs rejected):**
I took the AI's advice regarding the user session state: it pointed out that my `register` view redirects to the login page but does not actually authenticate the user. I manually tested this by registering a new account and explicitly logging in before trying to access the restricted `skills/add/` URL, which successfully triggered my 403 Forbidden logic. I rejected relying on the AI to manage my database; instead of asking for scripts to assign roles, I manually navigated the Django Admin interface to create the "Editor" group and assign users to it, ensuring I fully understood how Django's built-in `Group` permissions affect the database.

**Critical reflection on AI limitations:**
The debugging process highlighted a key limitation in how AI understands application state versus static code logic. When I was unexpectedly redirected to the login page instead of seeing a 403 error, the root cause wasn't a syntax error in the code—it was a flaw in the user journey (registration not granting an active session cookie). The AI is excellent at reading static decorators and view logic, but it struggles to organically anticipate the sequential session state of a user navigating the frontend unless explicitly prompted about the exact sequence of actions taken in the browser.

**Prompting/chat log:**
Full conversation log available at: https://share.gemini.google/iAA4f3RIwVYO

## Assignment 5
### Reflective Questions
1.Debouncing is a programming practice used to ensure that a function does not fire too frequently. It works by delaying the execution of the function until a certain amount of time has passed since the last time it was invoked. In an AJAX-based search feature, if a user types "Django", an application without debouncing would send a separate network request to the server for every single keystroke ("D", "Dj", "Dja", etc.). This spams the backend database with useless queries and wastes bandwidth. By implementing debouncing (e.g., a 300ms delay), the application waits until the user pauses typing before sending a single, final AJAX request, vastly improving server performance and frontend efficiency.

2. The fetch() API in JavaScript is asynchronous; it starts the network request in the background and allows the rest of your script to keep running while it waits for a response. The purpose of await is to pause the execution of that specific asynchronous function until the Promise resolves (i.e., until the server actually replies with the data). If we did not use await, JavaScript would instantly move to the next line of code before the HTTP request finished. Any variable meant to hold the server's response would instead hold a pending Promise object. Consequently, any subsequent code attempting to parse the JSON or update the UI would fail or throw errors because the data hasn't actually arrived yet.

3. Cross-Site Scripting (XSS) is a security vulnerability where an attacker injects malicious client-side scripts (like JavaScript) into web pages viewed by other users. This usually happens when an application takes untrusted user input (e.g., typing <script>alert('Hacked')</script> into a form) and renders it directly on the page. When other users load that page, their browser executes the malicious script. Data displayed via AJAX/JavaScript is highly vulnerable because developers frequently use DOM properties like innerHTML to dynamically inject the server's JSON response into the page. If that JSON contains malicious scripts and is injected via innerHTML, the browser will execute it. On the other hand, Django templates are safer by default because Django automatically escapes all template variables (converting characters like < into safe HTML entities like &lt;). When using AJAX, we lose Django's built-in frontend escaping, forcing us to manually sanitize the data in JavaScript before rendering it.

### AI Disclosure

**Tool used:** Gemini Pro 3.1 - High(Google)

**What it was used for:**
- Implementing AJAX-based asynchronous form submissions (POST) using the Fetch API to add new skills without page reloads.
- Creating a debounced asynchronous search function (GET) to filter skills in real-time.
- Implementing an HTML5 Popover modal for the skill creation form.
- Adding Toast notifications for successful creations and error handling.
- Securing the inputs against Cross-Site Scripting (XSS) using DOM manipulation (innerHTML vs textContent and manual escaping).

**Prompting strategy:**
For this assignment, I employed a conversational and iterative prompting style. Instead of providing a massive, rigid block of technical requirements upfront, I prefer to start with a broad request (e.g., "help me add an AJAX modal") and then refine the output through back-and-forth dialogue. I communicate with the AI casually, as if talking to a peer, allowing me to quickly relay feedback on visual discrepancies or server errors as I test them in real-time. This iterative approach is highly effective for catching AI hallucinations—such as incorrect Django syntax or mismatched CSS classes—step-by-step. By breaking the development process into smaller, conversational chunks, I can easily pinpoint exactly where the AI lost context of my specific codebase and guide it back on track.

**What I changed or fixed manually (What advice I took vs rejected):**
I accepted the AI's core logic for the JavaScript Fetch API, specifically the implementation of the AbortController for handling race conditions in debounced search requests. However, I manually intervened when the AI generated incorrect Django QuerySet syntax (hallucinating .exist() instead of .exists()) and form validation methods (self.cleaned instead of self.cleaned_data). Additionally, I had to manually fix the UI; the AI assumed the modal used a generic .skill-popover CSS class and provided styling for that, but I had to manually adapt and map those styles to my existing .experience-form-modal class structure to maintain the glassmorphic theme of my site.

**Critical reflection on AI limitations:**
This process heavily exposed the AI's "context blindness" and tendency to hallucinate framework-specific syntax. Because the AI didn't have my entire CSS stylesheet memorized, it invented default user-agent styles (like the beige background on inputs) and guessed incorrect class names, resulting in an unstyled modal. Furthermore, the AI generated slightly inaccurate Django ORM methods (e.g., .exist()), which caused 500 Internal Server Errors on the backend. This proves that while AI can generate structurally sound logic for frontend asynchronous requests, its output cannot be blindly copy-pasted without deep manual verification of framework syntax and CSS inheritance.

**Prompting/chat log:**
Full conversation log available at: https://share.gemini.google/V6flHAC7Mb2p

## Assignment 6 — Django REST Framework (Skills API)

### Outline
Tutorial 7 rebuilt my Experience page on Django REST Framework (DRF). For this assignment I applied the same pattern to **Skills**, the section I built myself in Assignments 3–5, keeping its existing model, data, and the four roles from Assignment 4.

| Layer | File | What it does |
|---|---|---|
| Serializer | `main/serializers.py` → `SkillSerializer` | Explicit `fields` list; `validate_name` / `validate_description` clean input with `strip_tags`; `validate_logo_url` rejects non-http(s) URLs and converts Google Drive links. `star_count`, `is_starred`, `starred_by_names` are read-only computed fields shared with Experience through `StarredModelSerializer`. No email or password data is exposed. |
| Permission | `main/permissions.py` → `IsPortfolioOwnerOrEditorOrReadOnly` | The four roles, checked on the server for every request. |
| API views | `main/api_views.py` → `skill_list`, `skill_detail`, `skill_star` | Function-based `@api_view` views with `SessionAuthentication`. The star endpoint uses `IsAuthenticated` and always takes the account from `request.user`. |
| URLs | `main/api_urls.py` | `/api/v1/skills/`, `/api/v1/skills/<uuid>/`, `/api/v1/skills/<uuid>/star/` (names `api:skill-list`, `api:skill-detail`, `api:skill-star`). |
| Page | `templates/skills.html`, `templates/components/skill_form_modal.html` | Lists, searches, sorts, adds, edits (PATCH), stars, and deletes through the API without reloading. Every write sends `X-CSRFToken`; every text value is escaped before it goes into HTML; 400 and 403 errors appear in a toast. |
| Tests | `main/tests_api.py` → `SkillAPITest`, `main/tests.py` → `SkillsPageTest` | Every role, database state after rejections, validation, stars, ordering, and real session + CSRF checks. |

#### API contract
| Method | Endpoint | Action | Allowed | Success | Common errors |
|---|---|---|---|---|---|
| GET | `/api/v1/skills/?name=&ordering=` | List, search by name, sort | Everyone | 200 (`[]` if nothing matches) | 400 unknown `ordering` |
| POST | `/api/v1/skills/` | Create a skill | Owner | 201 | 400 invalid input, 403 |
| GET | `/api/v1/skills/<uuid>/` | Retrieve one skill | Everyone | 200 | 404 |
| PUT / PATCH | `/api/v1/skills/<uuid>/` | Replace / partially update | Owner, Editor | 200 | 400, 403, 404 |
| DELETE | `/api/v1/skills/<uuid>/` | Delete a skill | Owner | 204 (empty body) | 403, 404 |
| POST | `/api/v1/skills/<uuid>/star/` | Give / remove a star (toggle) | Any logged-in account | 200 | 403 logged out, 405 on GET |

#### Roles
| Role | Read | Star | PUT / PATCH | POST / DELETE |
|---|---|---|---|---|
| Visitor (not logged in) | ✅ | ❌ (403) | ❌ (403) | ❌ (403) |
| Regular user | ✅ | ✅ | ❌ (403) | ❌ (403) |
| Editor (`Editor` group) | ✅ | ✅ | ✅ | ❌ (403) |
| Owner (`is_superuser`) | ✅ | ✅ | ✅ | ✅ |

`is_staff` alone grants nothing; only the `Editor` group or `is_superuser` matter. The older HTML views (`update_skill`, `create_skill`, `delete_skill`) already follow the same rules, so they don't give wider rights than the API.

#### Beyond the checklist
- **Sort control.** A dropdown (Newest first / Name A–Z / Most starred) sends `?ordering=newest|name|stars`. The API only accepts these three values (`SKILL_ORDERINGS` whitelist) and returns **400** for anything else, so a client can never sort by an arbitrary column. Every option has a tie-breaker, so results come back in a stable order.
- **One modal for Add and Edit.** Editing pre-fills the fields through `.value` (never `innerHTML`) and sends `PATCH`.
- **Clear error toasts.** 400 shows "Invalid input" with the field name (e.g. `name: This field may not be blank.`), and 403 shows "Not allowed" with the server's reason.
- **Star in place.** Starring updates only that star button from the API response, so the open skill popover doesn't close.

#### How to see it
1. `python manage.py runserver`, then open `http://127.0.0.1:8000/api/v1/skills/` for the Browsable API (try `?ordering=stars` and `?ordering=bogus`).
2. Open `/skills/` with DevTools → Network as each role and watch the `GET` / `POST` / `PATCH` / `DELETE` requests to `/api/v1/skills/`.
3. `python manage.py test main` runs every test (47).

### Assignment 6
1. **REST** (Representational State Transfer) is an architectural style for web APIs, not a library or a data format. A RESTful API treats data as *resources* with their own URLs (`/api/v1/skills/` for the collection, `/api/v1/skills/<uuid>/` for one skill). It lets the **HTTP method** say what to do (GET reads, POST creates, PUT/PATCH updates, DELETE removes) instead of putting verbs in the URL. Clients exchange *representations* of the data, such as JSON, and the API answers with meaningful status codes (201, 400, 403, 404, 204). Returning JSON alone doesn't make an API RESTful: my Assignment 5 endpoints already returned JSON, but they used action URLs like `/skills/add-ajax/` and deleted through a POST form, so the URL and method didn't describe the action. **PUT** sends a full replacement of the resource, so every required field must be included; a PUT with only `description` fails with 400 because `name` is required. **PATCH** sends only the fields that change and keeps the others. I use PATCH in my edit modal, because an Editor fixing a typo in a skill's description shouldn't have to resend the name and logo. PUT fits when a client really replaces the whole object, for example a sync script uploading the full definition of a skill.

2. A **serializer** is the contract between my models and the outside world, and it works in both directions. For reading, it turns `Skill` objects into plain Python data that DRF renders as JSON. For writing, it takes untrusted `request.data`, validates and cleans it into `validated_data`, and then `.save()` creates or updates the object. Compared with building dictionaries by hand in `JsonResponse` like Tutorial 5, it has several advantages:
   - The field list is declared once, explicitly, so I can't accidentally leak something like an email.
   - Validation lives in one place (`validate_name`, URL validation from the model's `URLField`), and errors come back automatically as `{"field": ["message"]}` with status 400.
   - Computed fields such as `star_count` are read-only, so a client can't forge them.
   - The same serializer handles list, detail, create, PUT, and PATCH (`partial=True`) without repeating code.
   - Removing the hand-written `get_skills_json` / `create_skill_ajax` code made the views much shorter.

3. **Authentication** answers *who is sending this request*: `SessionAuthentication` reads the Django session cookie and sets `request.user` (or treats the visitor as anonymous). **Authorization** answers *is this account allowed to do this*: a permission class such as `IsPortfolioOwnerOrEditorOrReadOnly` runs before the view body and returns 403 if not. DRF keeps the two separate, which is why a logged-in regular user is authenticated but still gets 403 on PATCH. Access rights have to be checked on the server because hiding a button in the template only changes what the page *shows*. Anyone can still send `fetch('/api/v1/skills/<id>/', {method: 'DELETE'})` from the console, use curl, or edit the HTML. My tests send these requests directly, without the page, and check that the database didn't change. That's the only real proof the rules hold.

4. With `SessionAuthentication`, the browser sends the session cookie **automatically** with every request to my site, including requests triggered by a malicious page in another tab. Without a CSRF check, that page could make a logged-in owner's browser delete a skill. The CSRF token proves the request came from my own page: it's read from the `csrftoken` cookie and sent in the `X-CSRFToken` header, and another site can't read it. That's why every write in `skills.html` sends the header, and why the template renders `{% csrf_token %}` to make sure the cookie exists. A test using `force_authenticate` isn't enough, because it skips authentication completely: it bypasses the session and the CSRF check, so a request without a token would still succeed. My tests use `APIClient(enforce_csrf_checks=True)` with `.login()` to create a real session. `test_session_write_without_csrf_is_rejected` and `test_editor_patch_without_csrf_is_rejected` prove that a missing token gives 403 and leaves the data unchanged, and `test_session_write_with_csrf_succeeds` proves a real token is accepted.

### AI Disclosure

**Tool used:** Claude Sonnet 5.5

**What it was used for:**
- Planning: comparing the Tutorial 7 / Assignment 6 checklists against my existing code and mapping the tutorial's `Project` example onto my models (Experience for the tutorial, Skills for the assignment).
- Writing the serializers, permission classes, API views, and URLs, and migrating `experience.html` and `skills.html` to the DRF endpoints.
- Writing the API tests (role coverage, validation, stars, ordering, session + CSRF) and updating my old tests that broke after the AJAX change.
- The extra sort feature (`?ordering=` whitelist and dropdown) and the PATCH edit modal.
- Drafting this README section, which I then reviewed and edited.

**Prompting strategy:** For this assignment, I combined an upfront set of rules with a step-by-step workflow. Instead of asking the AI to write everything at once, I first shared the assignment PDF and asked for a plan before any code was written, stating my constraints from the start: work on a separate branch, use conventional commits, aim for full marks on the rubric, and never let the AI commit, push, or be listed as a co-author. After approving the plan, I worked through it in small chunks. The AI made one change, explained what it did and how I could check it, then stopped so I could review the diff and commit it myself before typing "next". I kept the conversation casual, like talking to a peer, which made it easy to change direction mid-way — for example postponing the README and choosing only the sort control from the extra features it suggested. Working in small, reviewable chunks made it easy to catch the AI's mistakes (like a broken test setup or a corrupted file path) right when they happened, instead of discovering them later in one big batch of code

**What I decided or changed myself (advice taken vs. rejected):**
- I set the rule that every commit and push is mine, with no AI attribution. The whole branch history was committed by me, chunk by chunk.
- I didn't accept every suggestion. From the four extra features the AI proposed (smart edit modal, inline field errors, sort control, starred-only filter), I only kept the sort control, so the scope stayed realistic for the deadline.
- I adjusted commit messages myself, for example shortening `feat(api): add Skill endpoints with Editor permission` to `feat(api): add Skill endpoints`.
- I did the manual browser testing in all four roles, because the AI can't click through the UI. 

**Critical reflection on AI limitations:**
- **It started without context about my project.** The tutorial assumes a `Project` model, which my portfolio doesn't have. The AI had to read my codebase first to learn that my Tutorial 5 work used Experience and my own section was Skills. Without that, tutorial code would have been pasted onto models that don't exist.
- **Its own checks weren't always right the first time.**
  - Its first smoke test failed with `DisallowedHost`, because the Django test client uses the host `testserver`, which isn't in my `ALLOWED_HOSTS`. That was the AI's mistake, not a bug in my code.
  - A shell heredoc used to append tests failed on Windows Git Bash. It had to check that nothing had been half-written and redo the edit another way.
  - It first wrote `replace('_', ' ')` (which replaces only the first underscore) and corrected it to `replaceAll`.
  - It borrowed `timedelta` from `django.utils.timezone` instead of importing it properly, and fixed that too.
  - While generating this README with a Python script, the Windows path `env\Scripts\activate` was silently corrupted: `\a` was read as a "bell" control character, so the line rendered as `env\Scriptsctivate`. It only caught this after inspecting the raw bytes. A reminder that generated text needs to be read, not just produced.
- **Version mismatch.** The tutorial was tested with Django 5.2, but my project runs Django 6.1. The AI couldn't *know* DRF 3.18 works on 6.1; it could only verify it with `manage.py check` and the full test suite. Running tests mattered more than trusting the AI's confidence.
- **It can't see the UI.** It could only render templates in Python and syntax-check the JavaScript with Node, so the interactive behaviour (popovers, the modal, toasts) had to be tested by me in a real browser.
- **What it did well: finding bugs I had missed.**
  - Editors never saw the Edit button because the template read a non-existent `user.is_editor`.
  - `CSRF_TRUSTED_ORIGINS` had a trailing slash that breaks Django's origin check on PWS.
  - 6 of my 9 old tests were already failing.
  - The skill star view redirected to `/login` instead of `/login/`.
  - This README had a duplicated Assignment 3 section.

  It also proved its tests weren't decorative: it temporarily loosened a permission (letting Editors DELETE) and showed the role test failing with `204 != 403`, then restored it.

  My takeaway: the AI is fast at writing the structured parts (serializers, permissions, test matrices), but it still needs a human to own the decisions, run the code, check the UI, and approve every commit.

**Prompting/chat log:** (https://claude.ai/share/adca70e4-fc60-43d4-9ffe-e8c9dd9bdba5)
