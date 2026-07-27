"""
==========================================================
Gold Intelligence System
Recommendation Result Model
==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class RecommendationResult:
    """
    Final recommendation produced by the Recommendation Engine.
    """

    score: int

    confidence: int

    recommendation: str

    reasons: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    analytics: dict = field(default_factory=dict)

    def __str__(self):

        output = []

        output.append("=" * 60)
        output.append("GOLD INTELLIGENCE RECOMMENDATION")
        output.append("=" * 60)

        output.append(f"Recommendation : {self.recommendation}")
        output.append(f"Buy Score      : {self.score}/100")
        output.append(f"Confidence     : {self.confidence}%")

        output.append("")

        if self.reasons:

            output.append("Reasons")

            for reason in self.reasons:
                output.append(f"✔ {reason}")

        if self.warnings:

            output.append("")
            output.append("Warnings")

            for warning in self.warnings:
                output.append(f"⚠ {warning}")

        return "\n".join(output)
