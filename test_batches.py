from datetime import date

from model import Batch, OrderLine

today = date.today()


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-01", sku, batch_qty, today),
        OrderLine('orderline-01', sku, line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    large_batch, small_line = make_batch_and_line('SMALL-TABLE', 20, 5)
    large_batch.allocate(small_line)
    assert large_batch.available_quantity == 15


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line('BIG-TABLE', 11, 1)
    assert large_batch.can_allocate(small_line) is True


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line('MEDIUM-TABLE', 9, 10)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line('HIGH-CHAIR', 5, 5)
    assert batch.can_allocate(line) is True


def test_cannot_allocate_if_skus_dont_match():
    batch = Batch('batch-01', 'HIGH-CHAIR', 8, today)
    line = OrderLine('orderline-01', 'MEDIUM-TABLE', 1)
    assert batch.can_allocate(line) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line('RED-LAMP', 4, 1)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 4


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line('BLUE-CAP', 5, 1)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 4


def test_deallocate():
    batch, line = make_batch_and_line('EXPENSIVE-CHAIR', 2, 1)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 2