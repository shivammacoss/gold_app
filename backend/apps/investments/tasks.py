from celery import shared_task

from .services import InvestmentService


@shared_task(name="process_daily_returns")
def process_daily_returns():
    """Run daily: Credit ROI to all active investments."""
    InvestmentService.process_daily_returns()


@shared_task(name="complete_expired_investments")
def complete_expired_investments():
    """Run daily: Complete expired investments and return principal."""
    InvestmentService.complete_expired_investments()
