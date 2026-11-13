You are helping me prepare a short client-facing page. Create a single, very simple HTML page that contains only two sections: the Problem Statement and the Proposed Solution. Use only the context below. Do not invent facts, numbers, dates, prices or names.

# Context

I am designing a "content writing agent" for a client. The client's goal is to produce consistent thought-leadership posts on LinkedIn for an audience of technology and business leaders in North America who are interested in a set of themes the client chooses. Today this is done by hand.

The client has answered my scoping questions as follows:
- The agent should work in two ways: (1) the owner gives it a topic, or (2) the owner gives it themes and the agent researches what is currently trending within those themes and proposes topics.
- The owner will provide and maintain the list of themes and topics, and the list of data sources the agent may use.
- The owner wants several options per request, so they can compare tone and contrast.
- Only public or low-sensitivity material will be used at this stage.
- The destination is LinkedIn for now, and a blog post eventually. The scope for now is LinkedIn only.
- The owner will review and approve every draft to start with. A Google Doc or a Confluence page is proposed as the review place, and the client is open to suggestions. My recommendation is Google Docs for the evaluation, with Confluence possible if the owner's team already works there.
- An API key from the Claude Platform is available.

The solution I am proposing is built on Claude Managed Agents. In plain terms, Anthropic hosts the workplace where the AI agent runs (the agent loop, a locked-down workspace, a schedule, memory and a second AI reviewer that checks the work against a checklist), and we add one small tool of our own for starting requests, checking results and creating review documents.

How it works:
1. The owner starts a request in one of two ways. Either they give a topic, or they give themes only. When they give themes only, the agent searches only the approved data sources for what is trending, and proposes four topics, each with why it matters now, a suggested angle and sources. The owner picks one, and the same run continues.
2. The agent writes three drafts for LinkedIn, each in a different named tone (for example analytical, conversational, bold, story-led), with a short note on how each draft differs and a comparison with a suggested pick.
3. Every factual claim in a draft is tied to a source, with a link and an exact quote. A separate AI reviewer checks the drafts against a checklist (audience fit, tone, length, sources, no banned phrases). Our own code then opens each source and confirms the quote really exists, and checks the length and format.
4. The results are put into a review document (Google Doc recommended). The owner reads, compares and comments, chooses a draft, and posts it to LinkedIn by hand.
5. The owner tells the system which draft they chose and why, and this is saved so later drafts get closer to their preferences.
6. A weekly schedule can also produce topic proposals automatically, so they are waiting for the owner. Drafting happens on demand.

What the owner provides and controls: the themes and topics list, the approved data sources, the tone definitions, optional example posts, and the final decision on every post.

Safeguards: the agent can only read the approved sites; only public or low-sensitivity material is used; nothing is posted automatically, so no posting credentials exist; every post is approved by a person; every quote is verified by code; there is a spending limit on every run and a stop switch.

Planned approach: build and evaluate with the owner for about two weeks on LinkedIn, then decide next steps such as a blog format.

# What I want you to produce

One complete HTML file, with the following requirements.

Content:
- A page title and a one-line subtitle only.
- Section 1, "Problem statement": 3 to 5 short sentences, then a short list of 3 to 4 specific pain points (finding timely topics, researching and checking sources, keeping a consistent voice, trying different tones, time to review). Add a one-sentence statement of what success looks like.
- Section 2, "Proposed solution": a one-paragraph overview, then a very simple left-to-right flow of 4 or 5 boxes showing: Owner gives a topic or themes, Agent researches and writes three drafts in different tones, Checks (sources and quality), Review document, Owner chooses and posts. Then three short lists: "What the owner provides", "What the owner gets", "How we keep it safe". End with one sentence on scope: LinkedIn first, evaluated for about two weeks, blog later.
- Nothing else. No cost, no timeline, no risks, no technical steps, no code, no scenarios, no comparison with other products.

Language:
- Plain, simple English for a general business audience. No jargon. If a technical word is unavoidable, explain it in a few words.
- Do not mention any internal job titles, seniority levels or individuals' names.
- Do not mention any competing cloud platform or product.
- Mention Claude Managed Agents once, in plain words.
- Keep the total text under 450 words.

Design:
- One self-contained HTML file with inline CSS. No external libraries, fonts, images or JavaScript.
- A single centered column about 720px wide, generous spacing, readable system font stack, clear heading sizes.
- Works well on a phone: no horizontal scrolling, at least 16px side padding.
- Support light and dark mode with CSS variables and prefers-color-scheme. Set an explicit page background.
- The flow diagram is made with simple HTML and CSS boxes and arrows. On narrow screens the boxes stack vertically.
- Calm, professional look. One accent color. No decorative effects.

Output:
- Return the complete HTML in a single code block, ready to save as problem-and-solution.html.
- After the code block, give a two-line summary of what the page says. Do not add any other commentary.
