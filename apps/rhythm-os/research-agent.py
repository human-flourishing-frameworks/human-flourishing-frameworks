#!/usr/bin/env python3
"""
RHYTHM OS RESEARCH AGENT — Autonomous Learning Loop
Continuously: search → learn → accumulate → recommend work items
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import anthropic

# Configuration
RESEARCH_DIR = Path.home() / '.lantern' / 'research'
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

KNOWLEDGE_FILE = RESEARCH_DIR / 'knowledge-base.jsonl'
RECOMMENDATIONS_FILE = RESEARCH_DIR / 'work-items.json'
SEARCH_HISTORY_FILE = RESEARCH_DIR / 'searches.jsonl'

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

class ResearchAgent:
    def __init__(self):
        self.knowledge = self.load_knowledge()
        self.searches_performed = self.load_search_history()

    def load_knowledge(self):
        """Load accumulated knowledge base"""
        knowledge = []
        if KNOWLEDGE_FILE.exists():
            with open(KNOWLEDGE_FILE, 'r') as f:
                for line in f:
                    if line.strip():
                        knowledge.append(json.loads(line))
        return knowledge

    def load_search_history(self):
        """Load previous searches to avoid repeats"""
        searches = set()
        if SEARCH_HISTORY_FILE.exists():
            with open(SEARCH_HISTORY_FILE, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        searches.add(data.get('query', '').lower())
        return searches

    def save_knowledge(self, item):
        """Save discovered knowledge"""
        with open(KNOWLEDGE_FILE, 'a') as f:
            f.write(json.dumps(item) + '\n')

    def save_search(self, query, results):
        """Log search for reference"""
        with open(SEARCH_HISTORY_FILE, 'a') as f:
            f.write(json.dumps({
                'timestamp': datetime.utcnow().isoformat(),
                'query': query,
                'results_count': len(results)
            }) + '\n')

    async def generate_research_queries(self):
        """Use Claude to generate smart research queries"""

        context = f"""
You are a research agent for an AI-powered music + learning system (Rhythm OS).
You have already conducted {len(self.searches_performed)} searches.
You have accumulated {len(self.knowledge)} pieces of knowledge.

Current knowledge domains covered:
{self._summarize_knowledge()}

Generate 5 NEW research queries that would:
1. Fill gaps in knowledge about music curation, AI orchestration, privacy, or Starlink optimization
2. Discover emerging technologies relevant to the Lantern OS (music + AI + privacy)
3. Identify new market opportunities (van-life, intentional communities, accessibility)
4. Learn about competing solutions (what's out there)
5. Understand regulatory/patent landscape

Format as JSON array of strings.
"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": context
            }]
        )

        try:
            response_text = message.content[0].text
            # Extract JSON from response
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            queries = json.loads(response_text[start:end])
            return queries
        except:
            return [
                "privacy-first music streaming for offline communities",
                "Starlink latency optimization techniques",
                "AI agent orchestration frameworks",
                "van-life family technology needs",
                "cryptocurrency consensus mechanisms for local networks"
            ]

    def _summarize_knowledge(self):
        """Summarize what we already know"""
        domains = defaultdict(int)
        for item in self.knowledge:
            domain = item.get('domain', 'unknown')
            domains[domain] += 1

        summary = []
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            summary.append(f"  • {domain}: {count} items")

        return '\n'.join(summary) if summary else "  (no knowledge yet)"

    async def search_and_learn(self, query):
        """Search web and extract knowledge"""

        # Skip if already searched
        if query.lower() in self.searches_performed:
            print(f"[~] Already searched: {query}")
            return None

        print(f"[+] Searching: {query}")

        # Use Claude's web browsing capability
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Search the web for: "{query}"

Extract and summarize:
1. Key findings (3-5 bullets)
2. Relevant sources/links
3. Credibility assessment
4. How this relates to music curation, AI orchestration, privacy, or Starlink
5. Actionable insights for work planning

Format as JSON with these fields:
- query
- findings (array of strings)
- sources (array of URLs)
- credibility (low/medium/high)
- domain (what area of knowledge)
- actionable_insights (array of strings)
- relevance_score (0-100)
"""
            }]
        )

        try:
            response_text = message.content[0].text
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            knowledge_item = json.loads(response_text[start:end])

            # Add metadata
            knowledge_item['timestamp'] = datetime.utcnow().isoformat()
            knowledge_item['agent_version'] = '0.1'

            self.save_knowledge(knowledge_item)
            self.save_search(query, knowledge_item.get('findings', []))
            self.searches_performed.add(query.lower())

            return knowledge_item
        except Exception as e:
            print(f"[-] Error processing search: {e}")
            return None

    async def synthesize_recommendations(self):
        """Use Claude to analyze knowledge and recommend next work items"""

        if len(self.knowledge) < 3:
            print("[~] Need more knowledge before making recommendations (minimum 3 items)")
            return []

        # Prepare knowledge summary
        knowledge_summary = json.dumps(self.knowledge[-10:], indent=2)  # Last 10 items

        synthesis_prompt = f"""
You are analyzing research findings to recommend high-impact work items.

Recent research findings:
{knowledge_summary}

Based on these findings, recommend 5 concrete work items that would:
1. Address gaps discovered in research
2. Leverage emerging opportunities
3. Improve Rhythm OS (music + AI + privacy system)
4. Have measurable impact
5. Be achievable in 1-2 weeks

Format as JSON array with:
{{
  "title": "Short title",
  "description": "1-2 sentence description",
  "impact": "high/medium/low",
  "effort": "days needed",
  "related_research": ["query1", "query2"],
  "success_criteria": ["criterion1", "criterion2"],
  "revenue_impact": "optional estimate"
}}
"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": synthesis_prompt
            }]
        )

        try:
            response_text = message.content[0].text
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            recommendations = json.loads(response_text[start:end])

            # Save recommendations
            with open(RECOMMENDATIONS_FILE, 'w') as f:
                json.dump({
                    'timestamp': datetime.utcnow().isoformat(),
                    'items': recommendations,
                    'total_knowledge_items': len(self.knowledge),
                    'searches_performed': len(self.searches_performed)
                }, f, indent=2)

            return recommendations
        except Exception as e:
            print(f"[-] Error synthesizing recommendations: {e}")
            return []

    async def run_research_cycle(self, num_searches=5):
        """Execute full research cycle: generate → search → learn → recommend"""

        print("")
        print("="*70)
        print("RHYTHM OS RESEARCH AGENT — AUTONOMOUS LEARNING CYCLE")
        print("="*70)
        print("")

        # Step 1: Generate research queries
        print("[1/3] Generating research queries...")
        queries = await self.generate_research_queries()
        print(f"[+] Generated {len(queries)} research queries")

        # Step 2: Search and learn
        print(f"\n[2/3] Searching and learning ({num_searches} searches)...")
        for i, query in enumerate(queries[:num_searches], 1):
            result = await self.search_and_learn(query)
            if result:
                score = result.get('relevance_score', 0)
                domain = result.get('domain', 'unknown')
                print(f"    [{i}/{num_searches}] {domain} (relevance: {score}/100)")
            await asyncio.sleep(1)  # Rate limiting

        # Step 3: Synthesize recommendations
        print(f"\n[3/3] Synthesizing work recommendations...")
        recommendations = await self.synthesize_recommendations()

        # Display recommendations
        print(f"\n[+] Generated {len(recommendations)} work items for review:\n")

        for i, item in enumerate(recommendations, 1):
            print(f"{i}. {item.get('title', 'Untitled')}")
            print(f"   Impact: {item.get('impact', '?')} | Effort: {item.get('effort', '?')}")
            print(f"   {item.get('description', '')}")
            print("")

        return {
            'queries_generated': len(queries),
            'searches_completed': len([q for q in queries[:num_searches] if q.lower() not in self.searches_performed]),
            'recommendations': recommendations,
            'total_knowledge': len(self.knowledge)
        }

async def main():
    agent = ResearchAgent()

    # Run research cycle
    results = await agent.run_research_cycle(num_searches=3)

    # Save cycle summary
    summary_file = RESEARCH_DIR / 'cycle-summary.json'
    with open(summary_file, 'w') as f:
        json.dump({
            'timestamp': datetime.utcnow().isoformat(),
            'cycle_results': results
        }, f, indent=2)

    print("="*70)
    print("Research cycle complete. Recommendations saved to:")
    print(f"  {RECOMMENDATIONS_FILE}")
    print("="*70)

if __name__ == '__main__':
    asyncio.run(main())
