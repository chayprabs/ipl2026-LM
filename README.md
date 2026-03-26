# IPL Prediction System

## Overview

This project is a backend-oriented machine learning system for pre-match IPL prediction after the toss is known but before the first ball is bowled. It is designed to turn historical cricket data, player and team context, venue and weather signals, and bookmaker market information into structured predictions that are useful for downstream products, analytics workflows, or decision-support systems.

The system focuses on three questions:

- What is each team's probability of winning from the known post-toss match state?
- What first-innings total is most plausible, expressed as a range rather than a single brittle point estimate?
- What powerplay scoring range is likely for each team under the expected conditions?

## Why This Problem Is Hard

IPL prediction is a noisy forecasting problem. T20 cricket compresses the game into a small number of events, which makes outcomes highly sensitive to short bursts of performance, matchup effects, toss decisions, and changing conditions. A strong model cannot rely on raw averages alone because:

- small samples can dominate player-level statistics
- team compositions change frequently across seasons and auctions
- venue behavior is not stable across all phases of an innings
- weather and dew can alter second-innings conditions materially
- bookmaker markets are informative, but not sufficient on their own

The system is therefore built around disciplined feature construction, explicit filtering rules, and prediction outputs that reflect uncertainty rather than pretending it does not exist.

## Prediction Outputs

The prediction layer is split by target instead of forcing a single model to solve every task.

- Match win probability: calibrated probability distribution across the two teams in the post-toss, pre-match state
- First-innings total: predicted run band for the team batting first
- Powerplay runs: predicted run band for the first six overs for both innings contexts

Using probabilities and ranges is deliberate. In cricket, especially T20, overconfident point forecasts often hide the true uncertainty of the game state.

## How The System Works

At a high level, the system follows a staged backend pipeline:

1. Historical and real-time data is ingested from multiple sources.
2. Candidate features are generated across team, player, venue, weather, toss, matchup, and market dimensions.
3. A feature filtering layer removes features that are unavailable, invalid, or time-inconsistent for pre-match use.
4. Separate models are trained for each prediction target.
5. An inference pipeline assembles the current post-toss match state and returns structured outputs.

This separation matters. Data ingestion, feature engineering, filtering, modeling, and inference have different failure modes and evolve at different speeds. Treating them as distinct layers makes the system easier to audit and extend.

## Data Sources And Feature Types

The modeling stack is built on a mix of historical and real-time signals:

- historical match-level and ball-level cricket data
- team form and opponent-specific performance trends
- player-level batting, bowling, and role-based aggregates
- venue scoring patterns and phase-of-innings behavior
- weather signals such as temperature, humidity, rain risk, and dew likelihood
- toss-dependent context
- bookmaker odds and market-implied probabilities

The feature space includes both direct signals and derived context features, such as rolling form, venue-adjusted scoring rates, lineup stability proxies, matchup indicators, and market-based priors.

## Architecture

The repository is organized as a backend ML system rather than a notebook-first experiment:

- `src/data`: ingestion and dataset preparation
- `src/features`: feature construction logic
- `src/feature_selection`: feature registry and filtering rules
- `src/models`: target-specific training entrypoints
- `src/inference`: prediction assembly and output formatting
- `src/evaluation`: validation and quality measurement
- `api`: service-facing inference interface

The architecture is intentionally modular so new targets, features, or data feeds can be added without collapsing everything into one training script.

## Design Principles

Several design rules drive the system:

- Time-aware features only: every feature must correspond to information available before match start.
- No leakage: in-match or post-match information is excluded from training and inference for pre-match targets.
- Post-toss prediction logic: toss winner and decision are treated as legitimate inputs because they are known before the match begins.
- Probability-based outputs: the system favors calibrated probabilities and ranges over false precision.
- Market data as signal, not truth: bookmaker odds are treated as one input source among many, not as a target to copy.

## Intended Use

This project is meant for serious IPL forecasting workflows where correctness of timing assumptions matters as much as model quality. The value of the system is not only in predictive accuracy, but in maintaining a clean contract around what can be known before the match starts.
