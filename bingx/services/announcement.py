"""
Announcement Service

Handles BingX public announcements and notices.
No authentication required for these endpoints.
"""

from typing import Any, Dict, Optional

from ..http.base_client import BaseHTTPClient


class AnnouncementService:
    """Service for public announcement operations"""

    CONTENT_TYPES = [
        "LatestAnnouncements",
        "LatestPromotions",
        "ProductUpdates",
        "AssetMaintenance",
        "SystemMaintenance",
        "SpotListing",
        "FuturesListing",
        "InnovationListing",
        "FundingRate",
        "Delisting",
        "CryptoScout",
    ]

    LANGUAGES = ["zh-tw", "en-us"]

    def __init__(self, client: BaseHTTPClient):
        """
        Initialize Announcement Service

        Args:
            client: HTTP client instance
        """
        self.client = client

    def get_announcements(
        self,
        content_type: Optional[str] = None,
        language: str = "en-us",
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Get announcements by module type

        Args:
            content_type: Module type (LatestAnnouncements, LatestPromotions, 
                         ProductUpdates, AssetMaintenance, SystemMaintenance,
                         SpotListing, FuturesListing, InnovationListing,
                         FundingRate, Delisting, CryptoScout)
            language: Language code (zh-tw, en-us)
            page: Page number (minimum 1)

        Returns:
            Dictionary with list of announcements (title, time, link)
        """
        params: Dict[str, Any] = {"language": language, "page": page}
        if content_type:
            params["contentType"] = content_type
        return self.client.request("GET", "/openApi/content/v1/announcement", params)

    def get_latest_announcements(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get latest announcements

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("LatestAnnouncements", language, page)

    def get_promotions(self, language: str = "en-us", page: int = 1) -> Dict[str, Any]:
        """
        Get latest promotions

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("LatestPromotions", language, page)

    def get_product_updates(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get product updates

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("ProductUpdates", language, page)

    def get_maintenance_notices(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get system maintenance notices

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("SystemMaintenance", language, page)

    def get_asset_maintenance(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get asset maintenance notices

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("AssetMaintenance", language, page)

    def get_spot_listings(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get spot new listings

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("SpotListing", language, page)

    def get_futures_listings(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get futures new listings

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("FuturesListing", language, page)

    def get_delistings(self, language: str = "en-us", page: int = 1) -> Dict[str, Any]:
        """
        Get delisting notices

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("Delisting", language, page)

    def get_funding_rate_notices(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get funding rate notices

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("FundingRate", language, page)

    def get_crypto_scout(
        self, language: str = "en-us", page: int = 1
    ) -> Dict[str, Any]:
        """
        Get crypto scout announcements

        Args:
            language: Language code (zh-tw, en-us)
            page: Page number
        """
        return self.get_announcements("CryptoScout", language, page)
