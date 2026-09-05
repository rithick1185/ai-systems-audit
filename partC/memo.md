# Part C — Recommendation Memo

## Recommendation

Use a prompt-only approach for the three-week launch. This is the lowest-risk option because it requires no model training, no external API, and no additional serving infrastructure. It can be tested immediately on the available A100 80GB GPU and can be revised quickly using reviewer feedback.

## Assumptions

- Launch period: 3 weeks
- GPU: one A100 80GB
- Native reviewer: Hindi and Kannada
- Reviewer availability: 10 hours per week
- Total reviewer time: 3 × 10 = 30 hours
- Average review time: 5 minutes per response
- Reviewer capacity: 60 / 5 = 12 responses per hour
- Total possible reviewed responses: 30 × 12 = 360 responses
- Evaluation languages: English, Hindi, Kannada, and the other supported languages
- No external API is available

## Option comparison

| Option | Advantages | Limitations |
|---|---|---|
| SFT using synthetic casualized pairs | Can permanently change model behavior and may provide stronger consistency | Requires data generation, cleaning, training, validation, and regression testing; synthetic data may introduce errors |
| Inference-time rewriter under 1B parameters | Separates rewriting from the main model and can be served independently | Adds latency, memory usage, deployment complexity, and another model failure mode |
| Prompt-only approach | No training cost, no new model, minimal latency increase, easy rollback, and fastest launch | Improvement may be limited and may depend on prompt following; behavior may be less consistent |

## Arithmetic and feasibility

### Prompt-only approach

```text
Training GPU time = 0 hours
Additional model parameters = 0
Additional training data required = 0
Additional serving model = 0

Additional serving memory = negligible

Additional serving latency = small prompt-processing overhead; must be measured
A day-1 experiment can evaluate 100 prompts using two conditions
Condition A = original prompt
Condition B = original prompt + casual-language instructions
Total model outputs
= 100 prompts × 2 conditions
= 200 outputs
Hindi/Kannada outputs
= 200 × 0.5
= 100 outputs

At 5 minutes per review:

Reviewer time
= 100 × 5 minutes
= 500 minutes
≈ 8.3 hours
Synthetic examples = 10,000 pairs

Filtering time
= 10,000 × 30 seconds
= 300,000 seconds
≈ 83.3 hours
### Inference-time rewriter
Additional model = 1 model
Additional serving memory = model weights + runtime memory
Additional latency = rewriter inference time
Additional deployment work = model loading, routing, monitoring, and rollback

Casualness improvement < 10%
Meaning preservation < 95%
p95 latency increase > 5%
Three-week plan
Day 1

Prepare 100 evaluation prompts.

Run the original and prompt-only versions.

Review Hindi and Kannada outputs.

Record casualness, meaning preservation, factuality, and latency.

Week 1

Expand the evaluation set to 200 prompts.

Revise the prompt using reviewer feedback.

Apply the success thresholds and kill criterion.

Week 2

Run a larger held-out evaluation.

Test different prompt wording.

Measure p50 and p95 latency.

Check for regressions in Hindi and Kannada.

Week 3

Freeze the best-performing prompt.

Run final regression tests.

Document limitations and failure cases.

Prepare rollback to the original prompt.

Launch only if the success thresholds are met.

## Success threshold

The prompt-only approach will be considered successful if:

- Casualness improves by at least 20% compared with the original prompt.
- Meaning preservation remains at least 95%.
- Factuality does not decrease by more than 2 percentage points.
- p95 latency increases by no more than 5%.
- No major degradation occurs in Hindi or Kannada responses.

## Kill criterion

Stop the prompt-only approach by the end of week 1 if:

```text
Casualness improvement < 10%
Meaning preservation < 95%


### 4. Add the missing final decision

```markdown
## Final decision

The prompt-only approach is recommended for the initial launch because it fits the three-week timeline, requires no training or additional model, uses the available reviewer time efficiently, and can be rolled back immediately. SFT should be considered only after prompt-only testing fails or after sufficient reviewed data becomes available. The inference-time rewriter should be deferred because its additional latency and deployment complexity are not justified for the initial launch.
