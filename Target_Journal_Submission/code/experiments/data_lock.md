# Data lock (written 2026-11-23, BEFORE any method exploration)

Only the pilot (motivating experiment, fixed standard models, no method choice) has touched all CRC cohorts.

## Development cohorts (method design, idea selection, hyper-parameter choice)
CRC: FengQ_2015, GuptaA_2019, HanniganGD_2017, ThomasAM_2018a, ThomasAM_2018b, VogtmannE_2016, WirbelJ_2018, ZellerG_2014
(nested leave-one-cohort-out inside these 8 only).

## LOCKED final test (touched once per final candidate, after the protocol is frozen)
- CRC external cohorts: YachidaS_2019, YuJ_2015, ThomasAM_2019_c (models trained on the 8 development cohorts).
- Other diseases (entire disease untouched during development): IBD (HMP_2019_ibdmdb, HallAB_2017, IjazUZ_2017,
  NielsenHB_2014), T2D (KarlssonFH_2013, MetaCardis_2020_a, QinJ_2012, SankaranarayananK_2015 [+HMP_2019_t2d if T2D
  labels present]), adenoma vs control (FengQ_2015, HanniganGD_2017, ThomasAM_2018a, YachidaS_2019, ZellerG_2014).
  For these diseases the full leave-one-cohort-out protocol is run once with the frozen method.

Every idea tried during development is logged in experiments/novelty_escalation_log.md.
