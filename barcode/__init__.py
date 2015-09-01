from uber.common import *
from barcode._version import __version__
from uber.reports import *
from barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode

config = parse_config(__file__)
mount_site_sections(config['module_root'])
static_overrides(join(config['module_root'], 'static'))
template_overrides(join(config['module_root'], 'templates'))


class BarcodeReportMixin:
    """
    Overridden methods from the Reports base class.
    We will inject a barcode row into the exported data
    """

    def write_personalized_badge_row(self, row, out):
        if self._include_badge_nums:
            # add in the barcodes here
            badge_num = row[0]
            barcode = generate_barcode_from_badge_num(badge_num)
            row.append(barcode)

        return super.write_row(row, out)


class BarcodePrintedBadgeReport(uber.reports.PrintedBadgeReport, BarcodeReportMixin):
    pass


class BarcodePersonalizedBadgeReport(uber.reports.PersonalizedBadgeReport, BarcodeReportMixin):
    pass


class BarcodeSupporterBadgeReport(uber.reports.SupporterBadgeReport, BarcodeReportMixin):
    pass

uber.reports.printed_badge_report_type = BarcodePrintedBadgeReport
uber.reports.personalized_badge_report_type = BarcodePersonalizedBadgeReport
uber.reports.supporter_badge_report_type = BarcodeSupporterBadgeReport
