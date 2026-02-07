#!/usr/bin/env python3
"""
Article Generator for Kaynel Blog
Uses DeepSeek API to generate SEO-optimized articles about digital marketing,
web design, app development, SEO strategies, and marketing automation.
"""

import os
import re
import random
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Configuration
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
POSTS_DIR = Path("_posts")
ARTICLES_PER_RUN = 5

# Topics for article generation
TOPICS = [
    # Web Design
    "modern website design trends",
    "responsive web design best practices",
    "landing page optimization",
    "website usability improvements",
    "web design psychology and user experience",
    "minimalist design principles",
    "color theory for websites",
    "typography best practices for web",
    "website loading speed optimization",
    "mobile-first design strategies",
    
    # App Development
    "mobile app development trends",
    "cross-platform app development",
    "progressive web apps benefits",
    "app user onboarding strategies",
    "mobile app monetization",
    "app store optimization ASO",
    "native vs hybrid app development",
    "app performance optimization",
    "mobile app security practices",
    "app analytics and tracking",
    
    # SEO
    "SEO strategies for small business",
    "local SEO optimization tips",
    "technical SEO audit guide",
    "content marketing for SEO",
    "link building strategies",
    "keyword research techniques",
    "on-page SEO optimization",
    "SEO for e-commerce websites",
    "voice search optimization",
    "SEO analytics and reporting",
    
    # Marketing Automation
    "email marketing automation",
    "marketing automation tools comparison",
    "lead nurturing strategies",
    "customer journey automation",
    "chatbot implementation guide",
    "CRM integration best practices",
    "social media automation",
    "marketing workflow optimization",
    "personalization in marketing",
    "A/B testing automation",
    
    # Digital Marketing
    "digital marketing strategy planning",
    "social media marketing tips",
    "content marketing strategies",
    "PPC advertising optimization",
    "conversion rate optimization CRO",
    "brand awareness campaigns",
    "influencer marketing guide",
    "video marketing strategies",
    "customer retention strategies",
    "marketing ROI measurement"
]

CATEGORIES = [
    "Web Design",
    "App Development", 
    "SEO",
    "Marketing Automation",
    "Digital Marketing"
]


def init_client():
    """Initialize DeepSeek API client."""
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    
    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )


def get_category_for_topic(topic: str) -> str:
    """Determine category based on topic keywords."""
    topic_lower = topic.lower()
    
    if any(kw in topic_lower for kw in ["web design", "website", "landing page", "usability", "typography", "color", "minimalist"]):
        return "Web Design"
    elif any(kw in topic_lower for kw in ["app", "mobile", "native", "hybrid", "pwa"]):
        return "App Development"
    elif any(kw in topic_lower for kw in ["seo", "search", "keyword", "link building", "technical seo"]):
        return "SEO"
    elif any(kw in topic_lower for kw in ["automation", "email", "crm", "chatbot", "workflow", "lead"]):
        return "Marketing Automation"
    else:
        return "Digital Marketing"


def generate_article(client: OpenAI, topic: str) -> dict:
    """Generate an SEO-optimized article using DeepSeek API."""
    
    category = get_category_for_topic(topic)
    
    system_prompt = """You are an expert digital marketing writer creating SEO-optimized blog articles for Kaynel, a premium digital marketing agency based in Poland. 

Write comprehensive, valuable, actionable content that:
- Provides real value to business owners and marketing professionals
- Uses clear, professional language
- Includes practical tips and examples
- Is optimized for search engines with natural keyword usage
- Has engaging headers and subheaders
- Is between 1500-2500 words

Format the article in Markdown with proper headings (## for main sections, ### for subsections).

IMPORTANT: Do NOT include the title as an H1 at the beginning - just start with the introduction paragraph.
Do NOT include any frontmatter or metadata - just the article content."""

    user_prompt = f"""Write a comprehensive, SEO-optimized blog article about: {topic}

The article should:
1. Start with an engaging introduction that hooks the reader
2. Have 4-6 main sections with clear headings (use ##)
3. Include practical, actionable advice
4. Use relevant statistics or examples where appropriate
5. End with a compelling conclusion and call-to-action

Target audience: Business owners and marketing professionals looking to improve their digital presence.

Remember: Start directly with the introduction, no H1 title."""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=4000,
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    
    # Generate title
    title_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Generate a compelling, SEO-friendly blog title. Return ONLY the title text, no quotes or extra formatting."},
            {"role": "user", "content": f"Generate a catchy, SEO-optimized title for an article about: {topic}"}
        ],
        max_tokens=100,
        temperature=0.8
    )
    
    title = title_response.choices[0].message.content.strip().strip('"\'')
    
    # Generate meta description
    desc_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Generate a compelling meta description (150-160 characters). Return ONLY the description text."},
            {"role": "user", "content": f"Generate an SEO meta description for an article titled: {title}"}
        ],
        max_tokens=80,
        temperature=0.7
    )
    
    description = desc_response.choices[0].message.content.strip().strip('"\'')[:160]
    
    # Generate keywords
    keywords_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Generate 5-7 relevant SEO keywords, comma-separated. Return ONLY the keywords."},
            {"role": "user", "content": f"Generate SEO keywords for: {title}"}
        ],
        max_tokens=100,
        temperature=0.5
    )
    
    keywords = keywords_response.choices[0].message.content.strip()
    
    return {
        "title": title,
        "content": content,
        "description": description,
        "keywords": keywords,
        "category": category,
        "topic": topic
    }


def create_slug(title: str) -> str:
    """Create a URL-friendly slug from title."""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:60]


def get_existing_slugs() -> set:
    """Get set of existing article slugs to avoid duplicates."""
    POSTS_DIR.mkdir(exist_ok=True)
    slugs = set()
    
    for post_file in POSTS_DIR.glob("*.md"):
        # Extract slug from filename (YYYY-MM-DD-slug.md)
        parts = post_file.stem.split('-', 3)
        if len(parts) >= 4:
            slugs.add(parts[3])
    
    return slugs


def save_article(article: dict) -> str:
    """Save article as Jekyll post."""
    POSTS_DIR.mkdir(exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = create_slug(article["title"])
    filename = f"{date_str}-{slug}.md"
    filepath = POSTS_DIR / filename
    
    # Handle potential filename collision
    counter = 1
    while filepath.exists():
        filename = f"{date_str}-{slug}-{counter}.md"
        filepath = POSTS_DIR / filename
        counter += 1
    
    frontmatter = f"""---
layout: post
title: "{article['title']}"
description: "{article['description']}"
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} +0100
category: {article['category']}
keywords: {article['keywords']}
author: Kaynel Team
---

"""
    
    full_content = frontmatter + article["content"]
    
    filepath.write_text(full_content, encoding="utf-8")
    
    return str(filepath)


def select_topics(count: int, existing_slugs: set) -> list:
    """Select topics that haven't been covered recently."""
    available_topics = []
    
    for topic in TOPICS:
        # Check if similar content exists
        topic_slug_words = set(create_slug(topic).split('-'))
        is_duplicate = False
        
        for existing_slug in existing_slugs:
            existing_words = set(existing_slug.split('-'))
            # If more than 50% of words overlap, consider it duplicate
            if len(topic_slug_words & existing_words) > len(topic_slug_words) * 0.5:
                is_duplicate = True
                break
        
        if not is_duplicate:
            available_topics.append(topic)
    
    # If we've covered most topics, allow some repeats
    if len(available_topics) < count:
        available_topics = TOPICS.copy()
    
    return random.sample(available_topics, min(count, len(available_topics)))


def main():
    """Main function to generate articles."""
    print(f"🚀 Starting article generation - {datetime.now().isoformat()}")
    
    try:
        client = init_client()
        print("✅ DeepSeek API client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return 1
    
    existing_slugs = get_existing_slugs()
    print(f"📚 Found {len(existing_slugs)} existing articles")
    
    topics = select_topics(ARTICLES_PER_RUN, existing_slugs)
    print(f"📝 Selected {len(topics)} topics for generation")
    
    generated = 0
    for i, topic in enumerate(topics, 1):
        print(f"\n--- Article {i}/{len(topics)} ---")
        print(f"📌 Topic: {topic}")
        
        try:
            article = generate_article(client, topic)
            filepath = save_article(article)
            print(f"✅ Generated: {article['title']}")
            print(f"   Category: {article['category']}")
            print(f"   Saved to: {filepath}")
            generated += 1
        except Exception as e:
            print(f"❌ Failed to generate article: {e}")
            continue
    
    print(f"\n🎉 Generation complete! Created {generated}/{len(topics)} articles")
    return 0 if generated > 0 else 1


if __name__ == "__main__":
    exit(main())
