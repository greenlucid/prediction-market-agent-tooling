"""
Autogenerated using `datamodel-codegen` from a single Polymarket response. Then adjusted, fixed. 
Keep in mind that not all fields were used so far, so there might be some bugs.

These models are based on what Polymarket's website returns in the response, and `prediction_market_agent_tooling/markets/polymarket/data_models.py` are based on what their API returns.
"""

import json
import typing as t
from datetime import datetime

import requests
from loguru import logger
from pydantic import BaseModel, field_validator

from prediction_market_agent_tooling.gtypes import USDC, HexAddress
from prediction_market_agent_tooling.markets.data_models import Resolution

POLYMARKET_BASE_URL = "https://polymarket.com"
POLYMARKET_TRUE_OUTCOME = "Yes"
POLYMARKET_FALSE_OUTCOME = "No"


class ImageOptimized(BaseModel):
    imageUrlOptimized: str


class IconOptimized(BaseModel):
    imageUrlOptimized: str


class Event(BaseModel):
    id: str
    slug: str
    ticker: str
    title: str
    series: str | None


class Event1(BaseModel):
    startDate: datetime
    slug: str


class Market1(BaseModel):
    slug: str
    question: str
    image: str
    volume: USDC | None
    outcomes: list[str]
    outcomePrices: list[USDC]
    active: bool
    archived: bool
    closed: bool
    orderPriceMinTickSize: USDC
    clobTokenIds: str
    events: list[Event1]


class ResolutionData(BaseModel):
    id: str
    author: str
    lastUpdateTimestamp: datetime
    status: str
    wasDisputed: bool
    price: str
    proposedPrice: str
    reproposedPrice: str
    updates: str
    newVersionQ: bool
    transactionHash: str
    logIndex: str


class Market(BaseModel):
    id: str
    question: str
    conditionId: str
    slug: str
    twitterCardImage: t.Any | None
    resolutionSource: str
    endDate: datetime
    category: t.Any | None
    ammType: t.Any | None
    description: str
    liquidity: str
    startDate: datetime
    createdAt: datetime
    xAxisValue: t.Any | None
    yAxisValue: t.Any | None
    denominationToken: t.Any | None
    fee: str | None
    lowerBound: t.Any | None
    upperBound: t.Any | None
    outcomes: list[str]
    image: str
    icon: str
    imageOptimized: t.Any | None
    iconOptimized: t.Any | None
    outcomePrices: list[USDC]
    volume: USDC | None
    active: bool
    marketType: str | None
    formatType: t.Any | None
    lowerBoundDate: t.Any | None
    upperBoundDate: t.Any | None
    closed: bool
    marketMakerAddress: HexAddress
    closedTime: datetime | None
    wideFormat: bool | None
    new: bool
    sentDiscord: t.Any | None
    mailchimpTag: t.Any | None
    featured: bool
    submitted_by: str
    subcategory: t.Any | None
    categoryMailchimpTag: t.Any | None
    archived: bool
    resolvedBy: str
    restricted: bool
    groupItemTitle: str
    groupItemThreshold: str
    questionID: str
    umaEndDate: t.Any | None
    enableOrderBook: bool
    orderPriceMinTickSize: float
    orderMinSize: int
    umaResolutionStatus: t.Any | None
    curationOrder: t.Any | None
    volumeNum: USDC | None
    liquidityNum: float
    endDateIso: datetime | None
    startDateIso: datetime | None
    umaEndDateIso: datetime | None
    commentsEnabled: bool | None
    disqusThread: t.Any | None
    gameStartTime: datetime | None
    secondsDelay: int | None
    clobTokenIds: list[str]
    liquidityAmm: float
    liquidityClob: float
    makerBaseFee: int | None
    takerBaseFee: int | None
    negRisk: t.Any | None
    negRiskRequestID: t.Any | None
    negRiskMarketID: t.Any | None
    events: list[Event]
    markets: list[Market1]
    lower_bound_date: t.Any | None
    upper_bound_date: t.Any | None
    market_type: str | None
    resolution_source: str
    end_date: str
    amm_type: t.Any | None
    x_axis_value: t.Any | None
    y_axis_value: t.Any | None
    denomination_token: t.Any | None
    resolved_by: str
    upper_bound: t.Any | None
    lower_bound: t.Any | None
    created_at: str
    updated_at: t.Any | None
    closed_time: t.Any | None
    wide_format: bool | None
    volume_num: USDC | None
    liquidity_num: USDC
    image_raw: str
    resolutionData: ResolutionData

    @field_validator("closedTime", mode="before")
    def field_validator_closedTime(cls, v: str | None) -> str | None:
        return v.replace("+00", "") if v else None

    @property
    def resolution(self) -> Resolution | None:
        # If the market is not closed, it doesn't have a resolution.
        if not self.closed:
            return None

        outcome_to_outcome_price: dict[str, USDC] = dict(
            zip(self.outcomes, self.outcomePrices)
        )

        # On Polymarket, we can find out binary market resolution by by checking for the outcome prices.
        # E.g. if `Yes` price (probability) is 1$ and `No` price (probability) is 0$, it means the resolution is `Yes`.
        if (
            outcome_to_outcome_price[POLYMARKET_TRUE_OUTCOME] == 1.0
            and outcome_to_outcome_price[POLYMARKET_FALSE_OUTCOME] == 0.0
        ):
            return Resolution.YES

        elif (
            outcome_to_outcome_price[POLYMARKET_TRUE_OUTCOME] == 0.0
            and outcome_to_outcome_price[POLYMARKET_FALSE_OUTCOME] == 1.0
        ):
            return Resolution.NO

        else:
            raise ValueError(
                f"Unexpected outcome prices {outcome_to_outcome_price} or outcomes {self.outcomes}, please debug."
            )


class Category(BaseModel):
    id: str
    label: str
    parentCategory: str
    slug: str


class PolymarketFullMarket(BaseModel):
    id: str
    ticker: str
    slug: str
    title: str
    subtitle: t.Any | None
    description: str
    commentCount: int
    resolutionSource: str
    startDate: datetime
    endDate: datetime
    image: str
    icon: str
    featuredImage: str | None
    active: bool
    closed: bool
    archived: bool
    new: bool
    featured: bool
    restricted: bool
    liquidity: USDC
    volume: USDC | None
    volume24hr: USDC | None
    competitive: float
    openInterest: int | None
    sortBy: str | None
    createdAt: datetime
    commentsEnabled: bool | None
    disqusThread: t.Any | None
    updatedAt: datetime
    enableOrderBook: bool
    liquidityAmm: float
    liquidityClob: float
    imageOptimized: ImageOptimized | None
    iconOptimized: IconOptimized | None
    featuredImageOptimized: str | None
    negRisk: t.Any | None
    negRiskMarketID: t.Any | None
    negRiskFeeBips: t.Any | None
    markets: list[Market]
    categories: list[Category] | None
    series: t.Any | None
    image_raw: str

    @property
    def url(self) -> str:
        return construct_polymarket_url(self.slug)

    @property
    def is_main_market(self) -> bool:
        # On Polymarket, there are markets that are actually a group of multiple Yes/No markets, for example https://polymarket.com/event/presidential-election-winner-2024.
        # But if there is only 1 market in this list, it should mean it's a "main market", e.g. with only one question.
        return len(self.markets) == 1

    @property
    def main_market(self) -> Market:
        if not self.is_main_market:
            raise ValueError(
                f"Unexpected number of markets in the Polymarket's response, shouldn't happen if you used `is_main_market` filter, please debug: {self.id=}, {self.title=}"
            )
        return self.markets[0]

    @staticmethod
    def fetch_from_url(url: str) -> "PolymarketFullMarket | None":
        """
        Get the full market data from the Polymarket website.

        Returns None if this market's url returns "Oops...we didn't forecast this", see `check_if_its_a_main_market` method for more details.

        Warning: This is a very slow operation, as it requires fetching the website. Use it only when necessary.
        """
        # Fetch the website as a normal browser would.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        content = requests.get(url, headers=headers).text

        # Find the JSON with the data within the content.
        start_tag = """<script id="__NEXT_DATA__" type="application/json" crossorigin="anonymous">"""
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find("</script>", start_idx)
        response_data = content[start_idx:end_idx]

        # Parsing.
        response_dict = json.loads(response_data)
        response_model = PolymarketWebResponse.model_validate(response_dict)

        full_market_queries = [
            q
            for q in response_model.props.pageProps.dehydratedState.queries
            if isinstance(q.state.data, PolymarketFullMarket)
        ]

        # We expect either 0 markets (if it doesn't exist) or 1 market.
        if len(full_market_queries) not in (0, 1):
            raise ValueError(
                f"Unexpected number of queries in the response, please check it out and modify the code accordingly: `{response_dict}`"
            )

        # It will be `PolymarketFullMarket` thanks to the filter above.
        market = (
            t.cast(PolymarketFullMarket, full_market_queries[0].state.data)
            if full_market_queries
            else None
        )

        if market is None:
            logger.warning(f"No polymarket found for {url}")

        return market


class PriceSide(BaseModel):
    price: USDC
    side: t.Literal["BUY", "SELL"]


class State(BaseModel):
    data: (
        PolymarketFullMarket | PriceSide | None
    )  # It's none if you go to the website and it says "Oops...we didn't forecast this".
    dataUpdateCount: int
    dataUpdatedAt: int
    error: t.Any | None
    errorUpdateCount: int
    errorUpdatedAt: int
    fetchFailureCount: int
    fetchFailureReason: t.Any | None
    fetchMeta: t.Any | None
    isInvalidated: bool
    status: str
    fetchStatus: str


class Query(BaseModel):
    state: State
    queryKey: list[str]
    queryHash: str


class DehydratedState(BaseModel):
    mutations: list[t.Any]
    queries: list[Query]


class PageProps(BaseModel):
    key: str
    dehydratedState: DehydratedState
    eslug: str
    mslug: str | None
    isSingleMarket: bool


class Props(BaseModel):
    pageProps: PageProps


class Query1(BaseModel):
    slug: list[str]


class PolymarketWebResponse(BaseModel):
    props: Props
    page: str
    query: Query1
    buildId: str
    isFallback: bool
    gsp: bool
    locale: str
    locales: list[str]
    defaultLocale: str
    scriptLoader: list[t.Any]


def construct_polymarket_url(slug: str) -> str:
    """
    Note: This works only if it's a single main market, not sub-market of some more general question.
    """
    return f"{POLYMARKET_BASE_URL}/event/{slug}"
