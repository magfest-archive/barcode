from uber.common import *
from barcode._version import __version__
from uber.reports import *
from barcode import *
from barcode.barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode

config = parse_config(__file__)
mount_site_sections(config['module_root'])
static_overrides(join(config['module_root'], 'static'))
template_overrides(join(config['module_root'], 'templates'))


class BarcodeReportMixin:
    """
    Overridden methods from the Reports base class.
    We will inject a barcode row into the exported data
    """

    def write_row(self, row, out):
        if self._include_badge_nums:
            # add in the barcodes here
            badge_num = row[0]
            barcode = generate_barcode_from_badge_num(badge_num)
            row.append(barcode)

        # TODO: we should call the base class's writeRow(), but that's complex because of our multiple inheritance.
        # this works fine for now.
        out.writerow(row)


class BarcodePrintedBadgeReport(BarcodeReportMixin, uber.reports.PrintedBadgeReport):
    pass


class BarcodePersonalizedBadgeReport(BarcodeReportMixin, uber.reports.PersonalizedBadgeReport):
    pass


uber.reports.printed_badge_report_type = BarcodePrintedBadgeReport
uber.reports.personalized_badge_report_type = BarcodePersonalizedBadgeReport
