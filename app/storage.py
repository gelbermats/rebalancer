from typing import Dict, List, Optional
from app.modules.marketdata.models import Security, Quote
from app.modules.portfolio.models import Portfolio, Position


class DataManager:
    """
    Centralized data manager that encapsulates all application state.
    Eliminates the need for global variables and provides a clean interface
    for data operations.
    """
    
    def __init__(self):
        # In-memory storage
        self._securities_store: Dict[str, Security] = {}
        self._quotes_store: Dict[str, List[Quote]] = {}
        self._portfolios_store: Dict[int, Portfolio] = {}
        self._positions_store: Dict[int, Position] = {}
        
        # ID counters
        self._next_security_id: int = 1
        self._next_quote_id: int = 1
        self._next_portfolio_id: int = 1
        self._next_position_id: int = 1
    
    # Security operations
    def get_security(self, secid: str) -> Optional[Security]:
        return self._securities_store.get(secid)
    
    def add_security(self, security: Security) -> None:
        self._securities_store[security.secid] = security
    
    def get_all_securities(self) -> List[Security]:
        return list(self._securities_store.values())
    
    def security_exists(self, secid: str) -> bool:
        return secid in self._securities_store
    
    # Quote operations
    def get_quotes(self, secid: str) -> List[Quote]:
        return self._quotes_store.get(secid, [])
    
    def add_quote(self, quote: Quote) -> None:
        if quote.secid not in self._quotes_store:
            self._quotes_store[quote.secid] = []
        self._quotes_store[quote.secid].append(quote)
    
    def get_latest_quote(self, secid: str) -> Optional[Quote]:
        quotes = self._quotes_store.get(secid, [])
        return quotes[-1] if quotes else None
    
    # Portfolio operations
    def get_portfolio(self, portfolio_id: int) -> Optional[Portfolio]:
        return self._portfolios_store.get(portfolio_id)
    
    def add_portfolio(self, portfolio: Portfolio) -> None:
        self._portfolios_store[portfolio.id] = portfolio
    
    def get_all_portfolios(self) -> List[Portfolio]:
        return list(self._portfolios_store.values())
    
    def get_next_portfolio_id(self) -> int:
        next_id = self._next_portfolio_id
        self._next_portfolio_id += 1
        return next_id
    
    # Position operations
    def get_position(self, position_id: int) -> Optional[Position]:
        return self._positions_store.get(position_id)
    
    def add_position(self, position: Position) -> None:
        self._positions_store[position.id] = position
    
    def get_positions_for_portfolio(self, portfolio_id: int) -> List[Position]:
        return [pos for pos in self._positions_store.values() if pos.portfolio_id == portfolio_id]
    
    def get_all_positions(self) -> List[Position]:
        return list(self._positions_store.values())
    
    def get_next_position_id(self) -> int:
        next_id = self._next_position_id
        self._next_position_id += 1
        return next_id
    
    # ID counter operations
    def get_next_security_id(self) -> int:
        next_id = self._next_security_id
        self._next_security_id += 1
        return next_id
    
    def get_next_quote_id(self) -> int:
        next_id = self._next_quote_id
        self._next_quote_id += 1
        return next_id
    
    def clear_all(self) -> None:
        """Clear all data - useful for testing"""
        self._securities_store.clear()
        self._quotes_store.clear()
        self._portfolios_store.clear()
        self._positions_store.clear()
        self._next_security_id = 1
        self._next_quote_id = 1
        self._next_portfolio_id = 1
        self._next_position_id = 1


# Global instance - will be replaced with dependency injection
# This is a temporary bridge during refactoring
_data_manager = DataManager()

def get_data_manager() -> DataManager:
    """Factory function to get the data manager instance"""
    return _data_manager
