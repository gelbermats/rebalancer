import pytest
from datetime import datetime
from decimal import Decimal

from app.modules.portfolio.schemas import PositionBase, PositionCreate, Position


class TestPositionSchemas:
    
    def test_position_base_valid(self):
        position = PositionBase(
            secid="SBER",
            quantity=100,
            avg_price=Decimal("250.00")
        )
        assert position.secid == "SBER"
        assert position.quantity == 100
        assert position.avg_price == Decimal("250.00")
    
    def test_position_create(self):
        position = PositionCreate(
            secid="GAZP",
            quantity=50,
            avg_price=Decimal("180.00"),
            portfolio_id=1
        )
        assert position.secid == "GAZP"
        assert position.quantity == 50
        assert position.portfolio_id == 1
    
    @pytest.fixture
    def sample_position(self):
        return Position(
            id=1,
            secid="SBER",
            quantity=100,
            avg_price=Decimal("250.00"),
            portfolio_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    def test_position_complete(self, sample_position):
        assert sample_position.id == 1
        assert sample_position.secid == "SBER"
        assert sample_position.quantity == 100
        assert isinstance(sample_position.created_at, datetime)
    
    def test_position_calculations(self):
        position = PositionBase(
            secid="SBER",
            quantity=100,
            avg_price=Decimal("250.00")
        )
        total_value = position.quantity * position.avg_price
        assert total_value == Decimal("25000.00")
    
    def test_position_negative_quantity(self):
        position = PositionBase(
            secid="SBER",
            quantity=-50,
            avg_price=Decimal("250.00")
        )
        assert position.quantity == -50
        assert position.avg_price == Decimal("250.00")


class TestPortfolioCalculations:
    
    def test_portfolio_total_value(self):
        positions = [
            PositionBase(secid="SBER", quantity=100, avg_price=Decimal("250.00")),
            PositionBase(secid="GAZP", quantity=50, avg_price=Decimal("180.00")),
        ]
        
        total_value = sum(pos.quantity * pos.avg_price for pos in positions)
        assert total_value == Decimal("34000.00")
    
    def test_portfolio_weighted_average(self):
        positions = [
            PositionBase(secid="SBER", quantity=100, avg_price=Decimal("250.00")),
            PositionBase(secid="GAZP", quantity=200, avg_price=Decimal("180.00")),
        ]
        
        total_quantity = sum(pos.quantity for pos in positions)
        weighted_avg = sum(pos.quantity * pos.avg_price for pos in positions) / total_quantity
        
        assert total_quantity == 300
        assert weighted_avg == Decimal("203.33333333333333333333333333")
