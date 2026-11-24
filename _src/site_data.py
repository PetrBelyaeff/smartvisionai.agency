"""Site-wide settings and the page registry.

Every page of the site is listed here once. The registry drives the build,
navigation, breadcrumbs, sitemap.xml and llms.txt. To add a page: add a
template under templates/pages/ and a row below.
"""

SITE = {
    "name": "Smart Vision AI",
    "url": "https://smartvisionai.agency",
    "email": "petr@smartvisionai.agency",
    "booking": "https://calendar.google.com/calendar/appointments/schedules/AcZssZ1QaeAtBbRm9E6dCOqYcLi57awQORRnsjI7x1G6maX2-XyD0c8wLhdUrsz5z5yCTS_GYiABaUnU",
    "founder": "Petr Belyaev",
    "city": "Querétaro",
    "country": "MX",
    "og_image": "/og-v2.jpg",
    "year": 2026,
}

# Navigation in the header, in order
NAV = [
    ("/services/", "nav_services"),
    ("/clickup-partner/", "nav_clickup"),
    ("/cases/", "nav_cases"),
    ("/blog/", "nav_blog"),
    ("/contact/", "nav_contact"),
]
SITE["nav"] = NAV

UPDATED = "2026-11-24"

SERVICES = [
    {
        "url": "/services/ai-sales-agents/",
        "template": "pages/services/ai-sales-agents.html",
        "nav": "AI sales & support agents",
        "title": "AI sales & support agents · Smart Vision AI",
        "description": "AI agents that answer, qualify and follow up leads in WhatsApp, Telegram, Instagram and on your website, write to your CRM and hand the conversation to a person at the right moment.",
        "summary": "Agents that answer, qualify and follow up leads in messengers and on your website, and hand the conversation to your team when a person is needed.",
        "kind": "service",
    },
    {
        "url": "/services/clickup-implementation/",
        "template": "pages/services/clickup-implementation.html",
        "nav": "ClickUp implementation",
        "title": "ClickUp implementation for service businesses · Smart Vision AI",
        "description": "ClickUp workspace design and setup for delivery and client operations: structure, statuses, custom fields, automations, dashboards, time tracking and team onboarding.",
        "summary": "Workspace structure, processes, statuses and automations for delivery and client operations, designed around how your team actually works.",
        "kind": "service",
    },
    {
        "url": "/services/crm-messenger-integrations/",
        "template": "pages/services/crm-messenger-integrations.html",
        "nav": "CRM & messenger integrations",
        "title": "CRM & messenger integrations with n8n · Smart Vision AI",
        "description": "Kommo/amoCRM, Bitrix24, Shopify, WhatsApp, Telegram and ClickUp connected into one workflow with n8n and Make: lead routing, order follow-ups, notifications and reporting.",
        "summary": "Kommo/amoCRM, Bitrix24, Shopify, WhatsApp and Telegram connected to each other and to ClickUp through n8n and Make.",
        "kind": "service",
    },
    {
        "url": "/services/ai-search-visibility/",
        "template": "pages/services/ai-search-visibility.html",
        "nav": "AI search visibility",
        "title": "AI search visibility: does ChatGPT recommend your business? · Smart Vision AI",
        "description": "Regular checks of whether ChatGPT, Claude and Perplexity mention your brand when buyers ask about your niche, which competitors they name instead, and how this changes over time.",
        "summary": "Regular checks of whether ChatGPT, Claude and Perplexity mention your brand when buyers ask about your niche — and who they recommend instead.",
        "kind": "service",
    },
    {
        "url": "/services/managed-services/",
        "template": "pages/services/managed-services.html",
        "nav": "Managed services",
        "title": "Managed services after launch · Smart Vision AI",
        "description": "Ongoing support for AI agents, automations and ClickUp after launch: monitoring, fixes, weekly improvements, transparent time reports and new automations as the business grows.",
        "summary": "Monitoring, weekly improvements, reporting and new automations as your business grows.",
        "kind": "service",
    },
]

CASES = [
    {
        "url": "/cases/immigration-agency-ai-agents/",
        "template": "pages/cases/immigration-agency-ai-agents.html",
        "nav": "Immigration agency",
        "industry": "Immigration & citizenship services",
        "title": "Case: AI agents and lead flow for an immigration agency · Smart Vision AI",
        "description": "How I run AI agents, Bitrix24 lead handling, two websites and n8n automations for an immigration and citizenship agency with leads from ads, TikTok and messengers.",
        "summary": "AI agents on Bitrix24 open lines and a two-line TikTok setup in Kommo, lead routing to managers, two websites and n8n automations under ongoing support.",
        "stack": ["Bitrix24", "Kommo", "Suvvy AI agents", "n8n", "WhatsApp", "TikTok", "WordPress"],
        "kind": "case",
    },
    {
        "url": "/cases/ecommerce-unpaid-order-follow-up/",
        "template": "pages/cases/ecommerce-unpaid-order-follow-up.html",
        "nav": "E-commerce store",
        "industry": "E-commerce, Latin America",
        "title": "Case: automatic follow-up of unpaid orders for an online store · Smart Vision AI",
        "description": "Shopify, Kommo, n8n and WhatsApp Cloud API connected so that every unpaid order gets a timely WhatsApp follow-up and lands in the CRM pipeline.",
        "summary": "Shopify → Kommo → n8n → WhatsApp: every unpaid order gets a follow-up message without a manager remembering to send it.",
        "stack": ["Shopify", "Kommo", "n8n", "WhatsApp Cloud API", "Suvvy AI agent"],
        "kind": "case",
    },
    {
        "url": "/cases/tour-operator-ai-sales-agent/",
        "template": "pages/cases/tour-operator-ai-sales-agent.html",
        "nav": "Tour operator",
        "industry": "Travel & tourism",
        "title": "Case: 24/7 AI sales agent for a tour operator · Smart Vision AI",
        "description": "An AI sales agent with a knowledge base of tours and accommodation that answers on the website and in messengers, qualifies leads in amoCRM and hands them to managers.",
        "summary": "An AI sales agent that knows about 30 tours and 100 accommodation options, answers 24/7 and passes qualified leads to managers in amoCRM.",
        "stack": ["amoCRM", "Suvvy AI agents", "n8n", "WhatsApp", "Telegram", "Website chat"],
        "kind": "case",
    },
    {
        "url": "/cases/barbershop-franchise-clickup-platform/",
        "template": "pages/cases/barbershop-franchise-clickup-platform.html",
        "nav": "Barbershop franchise",
        "industry": "Franchising, beauty services",
        "title": "Case: franchise platform and AI assistant in ClickUp for a barbershop chain · Smart Vision AI",
        "description": "A franchise operations platform in ClickUp with standards, team rules and an AI assistant that answers franchisees from the same knowledge base.",
        "summary": "Franchise standards, team rules and marketing guides in ClickUp, plus an AI assistant that answers franchisees from the same knowledge base.",
        "stack": ["ClickUp", "ClickUp Docs", "AI assistant", "Google Drive"],
        "kind": "case",
    },
]

POSTS = [
    {
        "url": "/blog/is-your-business-visible-in-chatgpt/",
        "template": "pages/blog/is-your-business-visible-in-chatgpt.html",
        "nav": "Is your business visible in ChatGPT?",
        "title": "Is your business visible in ChatGPT? How I measure it · Smart Vision AI",
        "description": "A practical method to check whether ChatGPT, Claude and Perplexity mention your brand, which competitors they name instead, and what the numbers can and cannot tell you.",
        "summary": "A practical method to check whether AI assistants mention your brand — and what the numbers can and cannot tell you.",
        "date": "2026-11-24",
        "date_label": "November 24, 2026",
        "read": "7 min read",
        "kind": "post",
    },
    {
        "url": "/blog/ai-sales-agent-human-handoff/",
        "template": "pages/blog/ai-sales-agent-human-handoff.html",
        "nav": "When an AI sales agent should hand over to a person",
        "title": "When an AI sales agent should hand over to a person · Smart Vision AI",
        "description": "The handoff is where most AI sales agents lose deals. Here is how I design the moment an agent passes a conversation to a manager — triggers, context and what the client sees.",
        "summary": "The handoff is where most AI sales agents lose deals. How I design the moment an agent passes a lead to a manager.",
        "date": "2026-11-24",
        "date_label": "November 24, 2026",
        "read": "6 min read",
        "kind": "post",
    },
]

PAGES = (
    [
        {
            "url": "/",
            "template": "pages/index.html",
            "nav": "Home",
            "title": "Petr Belyaev · Smart Vision AI — AI sales agents and ClickUp systems",
            "description": "Smart Vision AI is a one-person AI implementation studio run by Petr Belyaev. AI sales and support agents, ClickUp implementation, CRM and messenger integrations through n8n, AI search visibility and managed services after launch.",
            "kind": "home",
        },
        {
            "url": "/services/",
            "template": "pages/services/index.html",
            "nav": "Services",
            "title": "Services · Smart Vision AI",
            "description": "AI sales and support agents, ClickUp implementation, CRM and messenger integrations, AI search visibility and managed services for small and mid-sized service businesses.",
            "kind": "section",
        },
    ]
    + SERVICES
    + [
        {
            "url": "/clickup-partner/",
            "template": "pages/clickup-partner.html",
            "nav": "ClickUp partner",
            "summary": "Workspace audit, plan selection, migration, onboarding and paid ClickUp plans through a Verified Service Partner.",
            "title": "ClickUp Verified Service Partner · Smart Vision AI",
            "description": "Smart Vision AI is a ClickUp Verified Service Partner. Workspace audit, implementation, migration from other tools, team onboarding and paid ClickUp plans for small and mid-sized businesses.",
            "kind": "section",
        },
        {
            "url": "/cases/",
            "template": "pages/cases/index.html",
            "nav": "Cases",
            "title": "Cases · Smart Vision AI",
            "description": "Examples of AI agents, CRM integrations and ClickUp systems I built for service businesses. Client names are not disclosed.",
            "kind": "section",
        },
    ]
    + CASES
    + [
        {
            "url": "/blog/",
            "template": "pages/blog/index.html",
            "nav": "Blog",
            "title": "Blog · Smart Vision AI",
            "description": "Notes on AI agents in sales, ClickUp, automation and AI search visibility from hands-on client work.",
            "kind": "section",
        },
    ]
    + POSTS
    + [
        {
            "url": "/contact/",
            "template": "pages/contact.html",
            "nav": "Contact",
            "title": "Contact · Smart Vision AI",
            "description": "Book a 30-minute call with Petr Belyaev or write to petr@smartvisionai.agency.",
            "kind": "section",
        },
    ]
)

for _p in PAGES:
    _p.setdefault("updated", UPDATED)
