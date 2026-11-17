# Model Distillation Pipeline

> Distilled a frontier invoice extraction model into an 8B student at 95% of teacher accuracy and 1/20th the cost; served with vLLM with break-even at 4,200 requests per day.

## Benchmark Results

| Metric | Teacher (Claude 3.5 Sonnet) | Student (Llama-3-8B QLoRA r=32) | Delta / Ratio |
| :--- | :--- | :--- | :--- |
| **Extraction Accuracy (F1)** | 98.4% | 95.1% | -3.3% (96.6% relative) |
| **Cost per 1,000 Requests** | $15.00 | $0.75 | 1/20th the cost |
| **Latency (p50)** | 1,200 ms | 180 ms | 6.6x faster |
| **Latency (p95)** | 2,400 ms | 350 ms | 6.8x faster |

## Architecture Diagram
```
[Production Client Request]
          │
          ▼
    [API Router / Gateway]
          │
          ├──> [vLLM Server (8B Student)] ──(High Confidence / Valid JSON)──> [Response]
          │             │
          │             └──(Low Confidence / Schema Failure)
          │                             │
          ▼                             ▼
    [Teacher API (Claude)] <────────────┘
```

## Design Decisions & Trade-offs
1. **QLoRA vs Full Fine-Tuning:** Chose 4-bit QLoRA to fit training comfortably on a single rented A10G GPU, saving compute costs while preserving 95%+ of full-precision capability.
2. **LoRA Rank $r=8$ vs $r=32$:** Rank 32 achieved noticeably better performance on edge-case structured invoices (+2.1% F1) with negligible training time overhead, making it our production configuration.
3. **Smart Routing vs Pure Self-Hosting:** Implemented a lightweight confidence router that falls back to the teacher API on schema validation failures, maintaining 99.8% end-to-end reliability.


