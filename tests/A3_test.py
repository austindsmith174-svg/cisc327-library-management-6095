from services.library_service import (pay_late_fees, refund_late_fee_payment)
from services.payment_service import PaymentGateway
from unittest.mock import Mock
import pytest
import time




# pay_late_fees tests

def test_success_process_payment(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book').return_value = {'fee_amount': 10}
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    assert success is True
    assert msg == 'Payment successful! Success'
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=10, description="Late fees for 'The Great Gatsby'")

def test_failure_process(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book').return_value = {'fee_amount': 10000} # this value doesn't matter
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    assert success is False
    assert txn is None
    assert msg == "Payment failed: Payment declined: amount exceeds limit"
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=10000, description="Late fees for 'The Great Gatsby'")

def test_invalid_id():
    success, msg, id = pay_late_fees("123abc", 1)
    assert success is False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."

def test_no_fees_due(mocker):
    success, msg, id = pay_late_fees("123456", 0)
    assert success is False
    assert msg == "No late fees to pay for this book."


def test_network_error(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book').return_value = {'fee_amount': 10}
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("network error")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    assert success is False
    assert txn is None
    assert "Payment processing error: network error" in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="123456", amount=10, description="Late fees for 'The Great Gatsby'")


# i made these before seeing the required test scenarios oops
# def test_error_calculating_fees(mocker):
#     mocker.patch('services.library_service.calculate_late_fee_for_book').return_value = None
#     success, msg, id= pay_late_fees("123456", 0)
#     assert success is False
#     assert msg == "Unable to calculate late fees."

# def test_error_calculating_fees2(mocker):
#     mocker.patch('services.library_service.calculate_late_fee_for_book').return_value = {}
#     success, msg, id= pay_late_fees("123456", 0)
#     assert success is False
#     assert msg == "Unable to calculate late fees."

# def test_invalid_book_id(mocker):
#     mocker.patch('services.library_service.calculate_late_fee_for_book').return_value = {'fee_amount': 50}
#     mocker.patch('database.get_book_by_id').return_value = None
#     success, msg, id = pay_late_fees("123456", 124)
#     assert success is False
#     assert msg == "Book not found."

# refund_late_fee_payment tests

def test_success_refund_payment(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, f"Refund of $10 processed successfully. Refund ID: refund_txn_123_{int(time.time())}")
    success, msg = refund_late_fee_payment("txn_123", 10, mock_gateway)
    assert success is True
    assert msg == f"Refund of $10 processed successfully. Refund ID: refund_txn_123_{int(time.time())}"
    mock_gateway.refund_payment.assert_called_once_with("txn_123", 10)

def test_invalid_transaction_id():
    success, msg = refund_late_fee_payment("invalid_txn", 50)
    assert success is False
    assert msg == "Invalid transaction ID."

def test_invalid_refund1():
    success, msg = refund_late_fee_payment(None, 5)
    assert success is False
    assert msg == "Invalid transaction ID."

def test_invalid_refund2():
    success, msg = refund_late_fee_payment("txn_123", -10)
    assert success is False
    assert msg == "Refund amount must be greater than 0."

def test_invalid_refund3():
    success, msg = refund_late_fee_payment("txn_123", 50)
    assert success is False
    assert msg == "Refund amount exceeds maximum late fee."