from datetime import date, timedelta
import pytest

from model import Batch, OrderLine, allocate, OutOfStock


today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch('instock-1', 'RED-TABLE', 20, eta=None)
    shipment_batch = Batch('shipment-1', 'RED-TABLE', 20, eta=tomorrow)
    line = OrderLine('orderline-1', 'RED-TABLE', 5)
    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 15
    assert shipment_batch.available_quantity == 20


def test_prefers_earlier_batches():
    earliest = Batch('batch-1', 'RED-TABLE', 20, eta=today)
    medium = Batch('batch-2', 'RED-TABLE', 20, eta=tomorrow)
    latest = Batch('batch-3', 'RED-TABLE', 20, eta=later)
    line = OrderLine('orderline-1', 'RED-TABLE', 5)
    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 15
    assert medium.available_quantity == 20
    assert latest.available_quantity == 20


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch('instock-1', 'RED-TABLE', 20, eta=None)
    shipment_batch = Batch('shipment-1', 'RED-TABLE', 20, eta=tomorrow)
    line = OrderLine('orderline-1', 'RED-TABLE', 5)
    allocated_ref = allocate(line, [in_stock_batch, shipment_batch])

    assert allocated_ref == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
