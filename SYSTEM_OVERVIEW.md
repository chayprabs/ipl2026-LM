# System Overview

## 1. Prediction Targets

The system produces post-toss, pre-match predictions for three separate targets. Each target is modeled independently because the statistical structure and error tolerance are different.

### 1.1 Match Win Probability

Definition:
- Probability that each team wins the match once venue, toss result, toss decision, likely playing context, weather snapshot, and market state are known.

Output format:
- `{"team_a_win_probability": 0.58, "team_b_win_probability": 0.42}`
- Values should be calibrated and sum to 1.0.

### 1.2 First Innings Total

Definition:
- Expected scoring range for the team batting first.

Output format:
- `{"lower": 168, "upper": 184, "confidence_band": "central"}`

Implementation note:
- This can be produced via quantile regression, interval regression, or bucketed ordinal prediction. The contract exposed by the system is a range, not a single run total.

### 1.3 Powerplay Runs

Definition:
- Expected scoring range in overs 1 to 6.
- Intended for both batting contexts, not just the first innings.

Output format:
- `{"innings": 1, "lower": 42, "upper": 55}`
- `{"innings": 2, "lower": 39, "upper": 52}`

## 2. Data Architecture

The system is built on layered cricket datasets rather than a single flat training table.

### 2.1 Core Dataset Levels

- Match-level data:
  team identities, venue, date, toss result, toss decision, outcome, innings totals, result margin
- Innings-level data:
  first-innings score, chase context, wickets remaining, overs summary, phase splits
- Ball-level data:
  batter, bowler, runs, dismissals, extras, over number, phase, handedness and role interactions where available

### 2.2 Data Flow

Raw to processed flow:

1. `data/raw`
   source extracts, API pulls, and external reference tables
2. `data/interim`
   cleaned and standardized tables with consistent schema and identifiers
3. `data/processed`
   modeling-ready datasets with resolved joins, aligned time windows, and derived labels
4. `src/features`
   feature generation over processed entities
5. `src/feature_selection`
   enforcement of pre-match feasibility and validity constraints

### 2.3 Why Multiple Granularities Exist

- Match-level data is required for broad team and venue context.
- Ball-level data is required for phase-specific scoring, wicket, and matchup signals.
- Player-level aggregation depends on both long-term summary tables and ball-level event history.
- Some targets, such as powerplay ranges, are poorly represented by coarse match averages alone.

## 3. Feature Universe

The feature space is intentionally broad before filtering. Candidate features span multiple categories because IPL outcomes are driven by interactions, not isolated variables.

### 3.1 Team-Level Features

- recent win rate
- season net run rate
- chasing and defending success rates
- powerplay scoring rate
- death-overs scoring rate
- wicket-loss rates by phase
- rest days
- lineup continuity proxies

### 3.2 Player-Level Features

- opener form and powerplay strike rate
- finisher death-over scoring profile
- lead pacer powerplay wickets
- spinner middle-over economy
- batter role projection
- player-vs-opposition summaries
- recent form composites
- injury or availability flags

### 3.3 Venue Features

- average first-innings score
- venue chasing bias
- spin versus pace wicket split
- phase scoring tendencies
- boundary dimensions or boundary-size proxy

### 3.4 Weather Features

- temperature
- humidity
- rain interruption risk
- wind speed
- dew probability

### 3.5 Toss Features

- toss winner
- elected decision
- historical success rate for the chosen decision
- venue-specific toss impact proxies

### 3.6 Odds Features

- latest bookmaker odds
- implied probability gap
- market overround
- short-horizon odds movement before match start

### 3.7 Matchup Features

- batting-hand versus bowling-type matchups
- bowler dot-ball profile versus likely top order
- batter scoring profile versus pace and spin combinations
- opposition-specific performance windows

## 4. Feature Filtering System

The system does not assume that every candidate feature should be used. Feature generation is intentionally broader than feature eligibility.

### 4.1 Feasibility Filter

Purpose:
- Reject features that depend on data sources not available in the current environment.

Typical checks:
- required data feed exists
- required entity mappings exist
- upstream preprocessing for that source completed successfully

Example:
- a venue feature requiring a dedicated venue metadata table is infeasible if that table is absent
- an odds drift feature is infeasible if the odds API is unavailable for the current match

### 4.2 Validity Filter

Purpose:
- Reject features that violate the pre-match prediction contract.

Rules:
- feature must be computable before match start
- toss-dependent features are allowed only because toss information is known pre-match
- features must not depend on in-match or post-match information
- features must not leak target labels or future game state

Examples of invalid features:
- first-innings score progression after 10 overs
- live required run rate
- post-match award market updates

### 4.3 Why This Layer Exists

- It protects the system from accidental leakage.
- It keeps training and inference aligned.
- It allows the feature universe to evolve without silently degrading the prediction contract.
- It makes it possible to run the same code in environments with different data availability.

## 5. Feature Engineering Logic

Feature engineering is time-aware by design. Every training row must represent only what would have been known at prediction time for that historical match.

### 5.1 Time-Aware Computation

- rolling windows are computed strictly from prior matches
- season aggregates are snapshot-based, not end-of-season summaries
- player form excludes the current match
- odds features use the last available pre-match market state, not closing information from after play starts

### 5.2 Rolling Statistics

Common patterns:
- last 5 and last 10 match windows
- phase-based run rates
- wicket rates by over segment
- opponent-specific windows where sample size is defensible

### 5.3 Aggregation Logic

The system frequently aggregates from player-level context to team-level summaries.

Examples:
- projected top-order batting strength from individual batter indicators
- projected bowling attack quality from role-based bowler summaries
- team-level matchup pressure from combined batter-bowler interactions

Aggregation is necessary because match outcomes are team-level targets, but many drivers live at the player or ball level.

## 6. Modeling Strategy

Each target is handled by a separate model family or model instance.

### 6.1 Separate Models

- match win probability model
- first-innings total range model
- powerplay range model

Rationale:
- classification and interval-style regression have different objectives
- feature importance is target-dependent
- calibration requirements differ by output type

### 6.2 Why Gradient Boosting Is Preferred

Gradient boosting is the default tabular baseline because it performs well on mixed, nonlinear, moderately sparse feature spaces.

Practical advantages:
- strong performance on structured data without heavy feature scaling requirements
- robust handling of nonlinear interactions
- works well with heterogeneous feature types
- interpretable enough for feature diagnostics compared with deep end-to-end alternatives

Candidate implementations:
- XGBoost
- LightGBM style boosting if introduced later
- quantile boosting or separate lower and upper bound regressors for range outputs

### 6.3 Role of Bookmaker Odds

Odds are treated as a predictive input, not a label and not a source of truth.

Reasoning:
- markets encode information the model may not fully observe
- markets also contain bias, vig, liquidity effects, and reaction lag
- copying odds is not the objective; combining them with cricket-specific context is

## 7. Inference Pipeline

The inference path is centered on the post-toss match snapshot.

### 7.1 Input State

Expected inputs include:
- teams
- venue
- scheduled date and start time
- toss winner
- toss decision
- available player context
- weather snapshot
- bookmaker odds snapshot

### 7.2 Inference Steps

1. Validate input completeness.
2. Load the feature registry.
3. Apply feasibility and validity filters for the current environment.
4. Build features for the current match state.
5. Score each target-specific model.
6. Format outputs into a structured response.

### 7.3 Output Contract

Expected response structure:
- match win probabilities for both teams
- first-innings total range
- powerplay run range output for relevant innings contexts
- optional metadata such as model version, prediction timestamp, and feature snapshot identifier

## 8. Key Assumptions

- T20 is highly variant, so even strong models will have noisy match-level outcomes.
- Many player-level samples are small and must be regularized implicitly or explicitly.
- IPL rosters change materially across auctions, injuries, and tactical role changes.
- Venue and weather effects matter, but are not perfectly observed.
- Toss information is considered valid input because predictions are explicitly post-toss.

## 9. Known Challenges

- Data sparsity for fringe players and new combinations
- Noisy player performance over small windows
- Difficulty projecting playing elevens before official confirmation
- Dynamic pitch and weather conditions that shift close to start time
- Odds feed quality and timing consistency
- Distribution shift across seasons due to roster churn and tactical evolution

## 10. Future Improvements

- simulation layer for converting range and win models into richer scenario outputs
- player embeddings to capture style similarity beyond hand-built aggregates
- live-updating models for in-match forecasting once the system expands beyond pre-match scope
- better uncertainty calibration for interval outputs
- explicit playing-XI probability modeling
- automated feature audits and drift monitoring

## Repository Mapping

The current repository layout maps directly to the design:

- `src/data`
  ingestion and dataset preparation
- `src/features`
  feature construction logic
- `src/feature_selection`
  registry and feature-eligibility rules
- `src/models`
  target-specific model training entrypoints
- `src/inference`
  prediction assembly
- `src/evaluation`
  offline validation and metrics
- `api`
  service interface

This separation is intentional. The system is easier to reason about when the data contract, feature contract, modeling contract, and inference contract are explicit rather than blended together in one training script.
