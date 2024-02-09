from decimal import Decimal
from enum import Enum
import typing as t
from pydantic import BaseModel
from web3 import Web3
from prediction_market_agent_tooling.gtypes import (
    USD,
    HexAddress,
    ChecksumAddress,
    Probability,
    Mana,
    OmenOutcomeToken,
    xDai,
    Wei,
)
from datetime import datetime


class Currency(str, Enum):
    xDai = "xDai"
    Mana = "Mana"


class BetAmount(BaseModel):
    amount: Decimal
    currency: Currency


class AgentMarket(BaseModel):
    """
    Common market class that can be created from vendor specific markets.
    Contains everything that is needed for an agent to make a prediction.
    """

    id: str
    question: str
    outcomes: list[str]
    bet_amount_currency: Currency
    original_market: t.Union["OmenMarket", "ManifoldMarket"]


class OmenMarket(BaseModel):
    """
    https://aiomen.eth.limo
    """

    BET_AMOUNT_CURRENCY: t.ClassVar[Currency] = Currency.xDai

    id: HexAddress
    title: str
    collateralVolume: Wei
    usdVolume: USD
    collateralToken: HexAddress
    outcomes: list[str]
    outcomeTokenAmounts: list[OmenOutcomeToken]
    outcomeTokenMarginalPrices: t.Optional[list[xDai]]
    fee: t.Optional[Wei]

    @property
    def market_maker_contract_address(self) -> HexAddress:
        return self.id

    @property
    def market_maker_contract_address_checksummed(self) -> ChecksumAddress:
        return Web3.to_checksum_address(self.market_maker_contract_address)

    @property
    def collateral_token_contract_address(self) -> HexAddress:
        return self.collateralToken

    @property
    def collateral_token_contract_address_checksummed(self) -> ChecksumAddress:
        return Web3.to_checksum_address(self.collateral_token_contract_address)

    @property
    def outcomeTokenProbabilities(self) -> t.Optional[list[Probability]]:
        return (
            [Probability(float(x)) for x in self.outcomeTokenMarginalPrices]
            if self.outcomeTokenMarginalPrices is not None
            else None
        )

    def get_outcome_index(self, outcome: str) -> int:
        try:
            return self.outcomes.index(outcome)
        except ValueError:
            raise ValueError(f"Outcome `{outcome}` not found in `{self.outcomes}`.")

    def get_outcome_str(self, outcome_index: int) -> str:
        n_outcomes = len(self.outcomes)
        if outcome_index >= n_outcomes:
            raise ValueError(
                f"Outcome index `{outcome_index}` not valid. There are only "
                f"`{n_outcomes}` outcomes."
            )
        else:
            return self.outcomes[outcome_index]

    def to_agent_market(self) -> AgentMarket:
        return AgentMarket(
            id=self.id,
            question=self.title,
            outcomes=self.outcomes,
            bet_amount_currency=self.BET_AMOUNT_CURRENCY,
            original_market=self,
        )

    def __repr__(self) -> str:
        return f"Omen's market: {self.title}"


class ManifoldPool(BaseModel):
    NO: float
    YES: float


class ManifoldMarket(BaseModel):
    """
    https://docs.manifold.markets/api#get-v0markets
    """

    BET_AMOUNT_CURRENCY: Currency = Currency.Mana

    id: str
    question: str
    creatorId: str
    closeTime: datetime
    createdTime: datetime
    creatorAvatarUrl: str
    creatorName: str
    creatorUsername: str
    isResolved: bool
    lastBetTime: datetime
    lastCommentTime: t.Optional[datetime] = None
    lastUpdatedTime: datetime
    mechanism: str
    outcomeType: str
    p: float
    pool: ManifoldPool
    probability: Probability
    slug: str
    totalLiquidity: Mana
    uniqueBettorCount: int
    url: str
    volume: Mana
    volume24Hours: Mana

    @property
    def outcomes(self) -> list[str]:
        return list(self.pool.model_fields.keys())

    def to_agent_market(self) -> "AgentMarket":
        return AgentMarket(
            id=self.id,
            question=self.question,
            outcomes=self.outcomes,
            bet_amount_currency=self.BET_AMOUNT_CURRENCY,
            original_market=self,
        )

    def __repr__(self) -> str:
        return f"Manifold's market: {self.question}"


class ProfitCached(BaseModel):
    daily: Mana
    weekly: Mana
    monthly: Mana
    allTime: Mana


class ManifoldUser(BaseModel):
    """
    https://docs.manifold.markets/api#get-v0userusername
    """

    id: str
    createdTime: datetime
    name: str
    username: str
    url: str
    avatarUrl: t.Optional[str] = None
    bio: t.Optional[str] = None
    bannerUrl: t.Optional[str] = None
    website: t.Optional[str] = None
    twitterHandle: t.Optional[str] = None
    discordHandle: t.Optional[str] = None
    isBot: t.Optional[bool] = None
    isAdmin: t.Optional[bool] = None
    isTrustworthy: t.Optional[bool] = None
    isBannedFromPosting: t.Optional[bool] = None
    userDeleted: t.Optional[bool] = None
    balance: Mana
    totalDeposits: Mana
    lastBetTime: t.Optional[datetime] = None
    currentBettingStreak: t.Optional[int] = None
    profitCached: ProfitCached


class ManifoldBetFills(BaseModel):
    amount: Mana
    matchedBetId: t.Optional[str]
    shares: Decimal
    timestamp: int


class ManifoldBetFees(BaseModel):
    platformFee: Decimal
    liquidityFee: Decimal
    creatorFee: Decimal


class ManifoldBet(BaseModel):
    """
    https://docs.manifold.markets/api#get-v0bets
    """

    shares: Decimal
    probBefore: Probability
    isFilled: t.Optional[bool] = None
    probAfter: Probability
    userId: str
    amount: Mana
    contractId: str
    id: str
    fees: ManifoldBetFees
    isCancelled: t.Optional[bool] = None
    loanAmount: Mana
    orderAmount: t.Optional[Mana] = None
    fills: t.Optional[list[ManifoldBetFills]] = None
    createdTime: int
    outcome: str


class Bet(BaseModel):
    amount: BetAmount
    outcome: bool
    created_time: datetime
