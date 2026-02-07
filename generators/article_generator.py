#!/usr/bin/env python3
"""
Article Generator for Kaynel Blog (Polish Language)
Uses DeepSeek API to generate SEO-optimized articles in Polish about digital marketing,
web design, app development, SEO strategies, and marketing automation.
Optimized for Polish market keywords and search trends.
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

# High-traffic Polish keywords and topics for better ranking
TOPICS = [
    # Strony internetowe (Web Design) - High volume Polish keywords
    "jak stworzyć stronę internetową dla firmy",
    "nowoczesne trendy w projektowaniu stron www 2026",
    "responsywna strona internetowa dlaczego jest ważna",
    "optymalizacja landing page zwiększenie konwersji",
    "UX design najlepsze praktyki dla polskich firm",
    "ile kosztuje strona internetowa w Polsce",
    "wordpress vs dedykowana strona internetowa",
    "szybkość ładowania strony jak poprawić",
    "certyfikat SSL dlaczego jest niezbędny",
    "strona internetowa dla małej firmy poradnik",
    
    # Aplikacje mobilne (App Development) - Trending Polish searches
    "jak stworzyć aplikację mobilną dla biznesu",
    "ile kosztuje aplikacja mobilna w Polsce 2026",
    "aplikacja natywna vs hybrydowa co wybrać",
    "PWA progressive web app korzyści dla firmy",
    "jak wypromować aplikację w App Store i Google Play",
    "trendy w tworzeniu aplikacji mobilnych",
    "flutter vs react native porównanie",
    "bezpieczeństwo aplikacji mobilnych najlepsze praktyki",
    "monetyzacja aplikacji mobilnej strategie",
    "UX w aplikacjach mobilnych jak zwiększyć retencję",
    
    # SEO - Top Polish SEO keywords
    "pozycjonowanie stron internetowych poradnik",
    "SEO lokalne dla firm w Polsce",
    "jak wypozycjonować stronę w Google",
    "słowa kluczowe jak je dobierać",
    "link building strategie 2026",
    "audyt SEO co sprawdzić",
    "content marketing a pozycjonowanie",
    "SEO dla sklepów internetowych ecommerce",
    "Google Analytics jak analizować ruch",
    "pozycjonowanie długi ogon long tail",
    "optymalizacja treści pod SEO",
    "indeksowanie strony w Google problemy i rozwiązania",
    
    # Marketing automation - Polish business keywords
    "automatyzacja marketingu dla małych firm",
    "email marketing jak zwiększyć open rate",
    "CRM dla małej firmy jaki wybrać",
    "chatbot na stronie internetowej korzyści",
    "lead nurturing automatyzacja lejka sprzedażowego",
    "marketing automation narzędzia porównanie",
    "personalizacja w marketingu online",
    "remarketing jak odzyskać klientów",
    "automatyzacja social media narzędzia",
    "newsletter jak budować listę mailingową",
    
    # Digital Marketing - High search volume Polish terms
    "marketing internetowy dla początkujących",
    "jak reklamować firmę w internecie",
    "reklama Google Ads poradnik",
    "marketing w social media strategia",
    "Facebook Ads vs Google Ads co wybrać",
    "influencer marketing w Polsce",
    "content marketing strategia dla firmy",
    "video marketing trendy 2026",
    "budowanie marki online",
    "analityka marketingowa KPI które śledzić",
    "konwersja na stronie jak zwiększyć sprzedaż",
    "customer journey mapowanie ścieżki klienta"
]

CATEGORIES = {
    "pl": ["Strony WWW", "Aplikacje", "SEO", "Automatyzacja", "Marketing"]
}


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
    
    if any(kw in topic_lower for kw in ["stron", "www", "landing", "wordpress", "ssl", "ładowania", "responsyw"]):
        return "Strony WWW"
    elif any(kw in topic_lower for kw in ["aplikacj", "mobiln", "app", "flutter", "react native", "pwa"]):
        return "Aplikacje"
    elif any(kw in topic_lower for kw in ["seo", "pozycjonow", "google", "słowa kluczowe", "link building", "indeksow"]):
        return "SEO"
    elif any(kw in topic_lower for kw in ["automatyzacj", "email", "crm", "chatbot", "newsletter", "lead"]):
        return "Automatyzacja"
    else:
        return "Marketing"


def generate_article(client: OpenAI, topic: str) -> dict:
    """Generate an SEO-optimized article in Polish using DeepSeek API."""
    
    category = get_category_for_topic(topic)
    
    system_prompt = """Jesteś ekspertem od marketingu cyfrowego piszącym artykuły SEO w języku polskim dla Kaynel - agencji marketingowej premium z Polski.

Twórz wartościowe, kompleksowe treści, które:
- Są napisane płynną, profesjonalną polszczyzną
- Zawierają praktyczne porady i przykłady z polskiego rynku
- Są zoptymalizowane pod SEO z naturalnym użyciem słów kluczowych
- Mają angażujące nagłówki i podnagłówki
- Liczą 1500-2500 słów
- Odpowiadają na pytania polskich przedsiębiorców

Formatuj artykuł w Markdown z poprawnymi nagłówkami (## dla głównych sekcji, ### dla podsekcji).

WAŻNE: NIE dodawaj tytułu jako H1 na początku - zacznij od wstępu.
NIE dodawaj frontmatter ani metadanych - tylko treść artykułu.

Używaj słów kluczowych naturalnie w tekście, nagłówkach i pierwszych akapitach."""

    user_prompt = f"""Napisz kompleksowy artykuł SEO w języku polskim na temat: {topic}

Artykuł powinien:
1. Zaczynać się od angażującego wstępu z głównym słowem kluczowym
2. Mieć 4-6 głównych sekcji z jasnymi nagłówkami (użyj ##)
3. Zawierać praktyczne, działające porady
4. Używać statystyk i przykładów z polskiego rynku
5. Kończyć się przekonującym podsumowaniem i wezwaniem do działania

Grupa docelowa: Polscy przedsiębiorcy i specjaliści marketingu szukający sposobów na rozwój firmy online.

Pamiętaj: Zacznij bezpośrednio od wstępu, bez tytułu H1."""

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
    
    # Generate Polish title
    title_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Wygeneruj chwytliwy tytuł artykułu SEO w języku polskim. Zwróć TYLKO tekst tytułu, bez cudzysłowów. Tytuł powinien zawierać główne słowo kluczowe i zachęcać do kliknięcia."},
            {"role": "user", "content": f"Wygeneruj tytuł SEO dla artykułu o: {topic}"}
        ],
        max_tokens=100,
        temperature=0.8
    )
    
    title = title_response.choices[0].message.content.strip().strip('"\'')
    
    # Generate Polish meta description
    desc_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Wygeneruj meta description (150-160 znaków) w języku polskim. Zwróć TYLKO opis. Użyj słowa kluczowego i zachęć do kliknięcia."},
            {"role": "user", "content": f"Wygeneruj meta description SEO dla artykułu zatytułowanego: {title}"}
        ],
        max_tokens=80,
        temperature=0.7
    )
    
    description = desc_response.choices[0].message.content.strip().strip('"\'')[:160]
    
    # Generate Polish keywords
    keywords_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Wygeneruj 5-7 słów kluczowych SEO po polsku, oddzielonych przecinkami. Zwróć TYLKO słowa kluczowe. Uwzględnij główne frazy i long-tail keywords."},
            {"role": "user", "content": f"Wygeneruj słowa kluczowe SEO dla: {title}"}
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
