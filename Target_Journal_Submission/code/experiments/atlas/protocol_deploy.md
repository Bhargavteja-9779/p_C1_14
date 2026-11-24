# Protocol v3b - label-free burn-in self-calibration (written 2026-11-24 BEFORE running it on any cohort)

## Method (BURN)
At a new site, score the first N people tested (no labels). With an assumed upper bound pi_max on disease prevalence among
them, set t = the k-th smallest burn-in score, k = ceil((N+1)(1 - beta)), beta = alpha (1 - pi_max).
Guarantee (exchangeable burn-in and later people, continuous scores): P_mix(S >= t) <= beta, and since
P_mix(S >= t) = (1-pi) FPR + pi TPR >= (1-pi) FPR, E[FPR] <= beta/(1-pi) <= alpha for any pi <= pi_max.
If k > N the rule is infeasible (flag nobody). High-confidence variant BURN-PAC: smallest k with
P(Beta(N+1-k, k) > beta) <= delta = 0.05 (order-statistic tolerance bound), giving P(FPR > alpha) <= 0.05 when pi=0.

## Comparators
SRC (training-control threshold), ATLAS (pooled healthy atlas of all OTHER populations in the same split), LAB(n):
conformal on n labelled local controls (= BURN with pi_max=0 on controls).

## Evaluation
(a) Healthy populations of the LOCKED atlas split (n >= N+20). R = 200 random burn-in/evaluation splits per population;
    N in {25, 50, 100, 200}. Endpoints: mean |FPR - 0.10|, P(FPR > 0.15), P(FPR > 0.10), per population then averaged
    over populations (each population weight 1). Exact predicted P(FPR > 0.15) from the Beta law is compared with observed.
(b) Contaminated pools: locked case-control cohorts (CRC: YachidaS_2019, YuJ_2015 with classifier trained on the 8 dev
    CRC cohorts; IBD/T2D leave-one-cohort-out). Burn-in = N people drawn with case fraction pi in {0.01, 0.05, 0.10},
    pi_max = pi (and a mis-specified pi_max = 0.01 when pi = 0.05). Evaluation = remaining controls/cases. Endpoints as (a)
    plus sensitivity.
Success criterion (pre-stated): in (a) BURN(N=100) has mean P(FPR>0.15) <= 0.10 averaged over locked populations and
mean |FPR-0.10| at least 50% lower than SRC; BURN-PAC(N=100) has P(FPR>0.10) <= 0.07 on average.
DEV atlas populations are used once first to check the code (no method changes allowed after that except bug fixes, logged).
