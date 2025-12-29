# Ambassador Verification Pipeline (Target: 250 verified)

## Objective
Verify 250 Ambassadors with proof-of-humanity, social footprint, and contribution staking.

## Stages
1. **Application Intake**: form submission → JSON record.
2. **Identity Proof**: liveness + government ID or web-of-trust 3 signatures.
3. **Footprint Check**: link Twitter/X, LinkedIn, GitHub; minimum age 6 months.
4. **Contribution Stake**: micro-stake in ASCENSION or attestations from 2 verified Ambassadors.
5. **Review Queue**: two reviewers + automated risk score.
6. **Onboarding**: wallet binding, role NFT mint, referral code.
7. **Ongoing Health**: quarterly activity check or stake decay.

## Data Model (JSON)
- id, name, email, wallet
- socials: { twitter, linkedin, github }
- proofs: { liveness_hash, id_hash, web_of_trust: [sig...] }
- scores: { risk, trust, activity }
- status: [applied|review|verified|rejected]
- timestamps

## SLA
- Median time to verify: < 48h.
- False accept rate < 1%. False reject < 3%.

## Ops Dashboard
- Queues by status
- Weekly throughput
- Risk distribution
