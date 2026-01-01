# Reel Requests

Create a new reel request by copying `_template.json` and editing it.

## How to use

1. Copy `_template.json` to a new file (e.g., `bio-06-topic.json`)
2. Edit the file with your reel details
3. Commit and push to trigger the pipeline
4. Watch GitHub Actions create your reel

## Request Format

```json
{
  "reel_id": "bio-06-topic-name",
  "subject": "biology",
  "topic": "What is the topic about?",
  "hook": "The attention-grabbing opening question",
  "key_fact": "The main scientific fact to teach",
  "why_it_matters": "Why students should care",
  "exam_relevance": "How this appears in JEE/NEET",
  "cta": "Follow for more!"
}
```

## Pipeline Steps

Each step runs as a **FRESH, ISOLATED Claude instance** with no memory of other steps:

| Step | Role | Input | Output |
|------|------|-------|--------|
| 1. SCRIPT | Write segment scripts | Request JSON | segments.json |
| 2. AUDIO | Generate TTS audio | segments.json | audio/*.mp3 |
| 3. VIDEO | Render Manim animation | audio/timings.json | video.mp4 |
| 4. COMBINE | Merge audio + video | video.mp4 + audio.mp3 | final.mp4 |
| 5. VALIDATE | Run all QA checks | final.mp4 | validation report |
| 6. POST | Post to platforms | final.mp4 | post IDs |

The chain is enforced cryptographically. If any step fails, the pipeline stops.
