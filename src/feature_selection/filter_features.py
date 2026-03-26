"""Feature registry and filtering helpers for IPL model inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal


AvailabilityTiming = Literal["before_toss", "after_toss", "in_match", "post_match"]


@dataclass(frozen=True)
class Feature:
    """Represent a candidate feature and the metadata needed to filter it."""

    name: str
    category: str
    required_data: list[str]
    computation_type: str
    is_pre_match: bool
    description: str
    depends_on_future_data: bool = False
    availability_timing: AvailabilityTiming = "before_toss"


@dataclass
class FeatureRegistry:
    """Store the registry of all candidate features."""

    features: list[Feature] = field(default_factory=list)

    def add(self, feature: Feature) -> None:
        """Append a single feature to the registry."""

        self.features.append(feature)

    def extend(self, features: Iterable[Feature]) -> None:
        """Append multiple features to the registry."""

        self.features.extend(features)

    def all(self) -> list[Feature]:
        """Return a copy of the registered features."""

        return list(self.features)


def build_feature_registry() -> FeatureRegistry:
    """Build the full feature registry used by the filtering layer."""

    registry = FeatureRegistry()
    registry.extend(
        [
            Feature(
                name="team_win_pct_last_5",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Team win percentage across the last five completed matches.",
            ),
            Feature(
                name="team_win_pct_last_10",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Team win percentage across the last ten completed matches.",
            ),
            Feature(
                name="team_net_run_rate_season",
                category="team",
                required_data=["match_data"],
                computation_type="match-level",
                is_pre_match=True,
                description="Season net run rate entering the match.",
            ),
            Feature(
                name="team_powerplay_run_rate",
                category="team",
                required_data=["ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Historical team run rate in overs 1 to 6.",
            ),
            Feature(
                name="team_death_over_run_rate",
                category="team",
                required_data=["ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Historical team run rate in overs 16 to 20.",
            ),
            Feature(
                name="team_powerplay_wicket_loss_rate",
                category="team",
                required_data=["ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Average wickets lost by the team in the powerplay.",
            ),
            Feature(
                name="team_chasing_success_rate",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical win rate while batting second.",
            ),
            Feature(
                name="team_defending_success_rate",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical win rate while defending a total.",
            ),
            Feature(
                name="head_to_head_win_pct",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Head-to-head win rate between the two teams.",
            ),
            Feature(
                name="team_average_margin_of_victory",
                category="team",
                required_data=["match_data"],
                computation_type="match-level",
                is_pre_match=True,
                description="Average historical margin of victory for the team.",
            ),
            Feature(
                name="toss_decision_preference",
                category="team",
                required_data=["match_data"],
                computation_type="match-level",
                is_pre_match=True,
                description="Historical preference to bat or bowl first after winning the toss.",
            ),
            Feature(
                name="team_recent_rest_days",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Number of rest days since the team's previous match.",
            ),
            Feature(
                name="team_home_venue_win_pct",
                category="team",
                required_data=["match_data", "venue_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical win rate for the team at the current venue.",
            ),
            Feature(
                name="team_current_points_table_position",
                category="team",
                required_data=["ranking_api"],
                computation_type="match-level",
                is_pre_match=True,
                description="Live league-table rank before the fixture starts.",
            ),
            Feature(
                name="team_expected_playing_xi_stability",
                category="team",
                required_data=["match_data", "injury_feed"],
                computation_type="derived",
                is_pre_match=True,
                description="Stability score based on repeated player selections and injury news.",
            ),
            Feature(
                name="opener_average_last_10_innings",
                category="player",
                required_data=["player_stats"],
                computation_type="derived",
                is_pre_match=True,
                description="Average runs for the likely opening batter in the last ten innings.",
            ),
            Feature(
                name="opener_powerplay_strike_rate",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Strike rate for the likely opener in overs 1 to 6.",
            ),
            Feature(
                name="captain_batting_average_at_venue",
                category="player",
                required_data=["player_stats", "venue_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical batting average for the captain at the current venue.",
            ),
            Feature(
                name="finisher_death_overs_strike_rate",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Strike rate for the likely finisher in overs 16 to 20.",
            ),
            Feature(
                name="wicketkeeper_dismissals_per_match",
                category="player",
                required_data=["player_stats"],
                computation_type="match-level",
                is_pre_match=True,
                description="Average dismissals per match for the projected wicketkeeper.",
            ),
            Feature(
                name="lead_pacer_powerplay_wickets_per_match",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Wickets per match for the lead pace bowler in the powerplay.",
            ),
            Feature(
                name="lead_spinner_middle_overs_economy",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Economy rate for the lead spinner in overs 7 to 15.",
            ),
            Feature(
                name="death_bowler_yorker_frequency",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Estimated yorker frequency for the main death-over bowler.",
            ),
            Feature(
                name="bowler_vs_opposition_wickets",
                category="player",
                required_data=["player_stats", "match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical wickets for the bowler against the opponent team.",
            ),
            Feature(
                name="player_recent_form_index",
                category="player",
                required_data=["player_stats", "match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Composite form score from recent batting or bowling output.",
            ),
            Feature(
                name="player_injury_risk_flag",
                category="player",
                required_data=["injury_feed"],
                computation_type="match-level",
                is_pre_match=True,
                description="Binary flag based on latest injury or fitness reports.",
            ),
            Feature(
                name="projected_batting_position",
                category="player",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Estimated batting slot for a player from recent lineup patterns.",
            ),
            Feature(
                name="batting_hand_matchup_index",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Historical performance against left-arm and right-arm bowling types.",
            ),
            Feature(
                name="bowler_matchup_dot_ball_pct",
                category="player",
                required_data=["player_stats", "ball_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Dot-ball percentage for the bowler against likely top-order batters.",
            ),
            Feature(
                name="venue_avg_first_innings_score",
                category="venue",
                required_data=["match_data", "venue_data"],
                computation_type="match-level",
                is_pre_match=True,
                description="Average first-innings score at the current venue.",
            ),
            Feature(
                name="venue_avg_powerplay_score",
                category="venue",
                required_data=["ball_data", "venue_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Average powerplay score at the venue.",
            ),
            Feature(
                name="venue_chasing_bias",
                category="venue",
                required_data=["match_data", "venue_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Bias towards teams batting second at the venue.",
            ),
            Feature(
                name="venue_spin_vs_pace_wicket_split",
                category="venue",
                required_data=["ball_data", "venue_data"],
                computation_type="ball-level",
                is_pre_match=True,
                description="Proportion of wickets taken by spin versus pace at the venue.",
            ),
            Feature(
                name="boundary_size_index",
                category="venue",
                required_data=["venue_data"],
                computation_type="match-level",
                is_pre_match=True,
                description="Normalized boundary dimension score for the venue.",
            ),
            Feature(
                name="weather_temperature_c",
                category="weather",
                required_data=["weather_api"],
                computation_type="match-level",
                is_pre_match=True,
                description="Forecast match-start temperature in Celsius.",
            ),
            Feature(
                name="weather_humidity_pct",
                category="weather",
                required_data=["weather_api"],
                computation_type="match-level",
                is_pre_match=True,
                description="Forecast relative humidity at match start.",
            ),
            Feature(
                name="weather_rain_interruption_risk",
                category="weather",
                required_data=["weather_api"],
                computation_type="derived",
                is_pre_match=True,
                description="Probability of rain affecting overs or start time.",
            ),
            Feature(
                name="dew_probability",
                category="weather",
                required_data=["weather_api"],
                computation_type="derived",
                is_pre_match=True,
                description="Estimated chance of dew impacting the second innings.",
            ),
            Feature(
                name="wind_speed_kph",
                category="weather",
                required_data=["weather_api"],
                computation_type="match-level",
                is_pre_match=True,
                description="Forecast wind speed near scheduled start time.",
            ),
            Feature(
                name="market_home_win_odds",
                category="odds",
                required_data=["odds_api"],
                computation_type="match-level",
                is_pre_match=True,
                description="Latest bookmaker odds for the home side.",
            ),
            Feature(
                name="market_away_win_odds",
                category="odds",
                required_data=["odds_api"],
                computation_type="match-level",
                is_pre_match=True,
                description="Latest bookmaker odds for the away side.",
            ),
            Feature(
                name="market_implied_win_probability_gap",
                category="odds",
                required_data=["odds_api"],
                computation_type="derived",
                is_pre_match=True,
                description="Difference in bookmaker implied win probability between teams.",
            ),
            Feature(
                name="odds_movement_last_6_hours",
                category="odds",
                required_data=["odds_api"],
                computation_type="derived",
                is_pre_match=True,
                description="Magnitude of odds drift in the six hours leading to the match.",
            ),
            Feature(
                name="odds_market_overround",
                category="odds",
                required_data=["odds_api"],
                computation_type="derived",
                is_pre_match=True,
                description="Bookmaker margin implied by the current head-to-head market.",
            ),
            Feature(
                name="toss_winner_historical_advantage",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical advantage for the toss winner in similar fixtures.",
                availability_timing="after_toss",
            ),
            Feature(
                name="elected_to_bowl_historical_success_rate",
                category="team",
                required_data=["match_data"],
                computation_type="derived",
                is_pre_match=True,
                description="Historical win rate when the toss winner chooses to bowl first.",
                availability_timing="after_toss",
            ),
            Feature(
                name="first_innings_score_progression_after_10_overs",
                category="team",
                required_data=["ball_data"],
                computation_type="ball-level",
                is_pre_match=False,
                description="Live batting progression after ten overs of the first innings.",
                depends_on_future_data=True,
                availability_timing="in_match",
            ),
            Feature(
                name="live_win_probability_after_powerplay",
                category="odds",
                required_data=["ball_data", "odds_api"],
                computation_type="derived",
                is_pre_match=False,
                description="Updated win probability after the first six overs.",
                depends_on_future_data=True,
                availability_timing="in_match",
            ),
            Feature(
                name="second_innings_required_run_rate_projection",
                category="team",
                required_data=["match_data", "ball_data"],
                computation_type="derived",
                is_pre_match=False,
                description="Required run-rate projection during a live chase.",
                depends_on_future_data=True,
                availability_timing="in_match",
            ),
            Feature(
                name="player_live_form_in_match",
                category="player",
                required_data=["ball_data", "player_stats"],
                computation_type="ball-level",
                is_pre_match=False,
                description="Live confidence proxy derived from the current innings.",
                depends_on_future_data=True,
                availability_timing="in_match",
            ),
            Feature(
                name="post_match_award_probability_update",
                category="odds",
                required_data=["match_data", "odds_api"],
                computation_type="derived",
                is_pre_match=False,
                description="Updated award market after the match result is known.",
                depends_on_future_data=True,
                availability_timing="post_match",
            ),
        ]
    )
    return registry


def get_feature_registry() -> list[Feature]:
    """Return registered features as a flat list.

    This keeps the previous call-site shape while using the stronger registry model.
    """

    return build_feature_registry().all()


def check_feasibility(feature: Feature, available_data_sources: list[str]) -> bool:
    """Return True when all declared data dependencies are available."""

    available_sources = set(available_data_sources)
    return all(source in available_sources for source in feature.required_data)


def check_validity(feature: Feature) -> bool:
    """Return True when a feature is safe to use before match start."""

    allowed_timings = {"before_toss", "after_toss"}
    return (
        feature.is_pre_match
        and not feature.depends_on_future_data
        and feature.availability_timing in allowed_timings
    )


def filter_features(
    features: list[Feature], available_data_sources: list[str]
) -> list[Feature]:
    """Apply feasibility and validity filters to a feature list."""

    feasible_features = [
        feature
        for feature in features
        if check_feasibility(feature, available_data_sources)
    ]
    return [feature for feature in feasible_features if check_validity(feature)]
