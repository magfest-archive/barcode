from uber.common import *
from barcode._version import __version__
from barcode import *
from barcode.barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode
from barcode.barcode_api import *

config = parse_config(__file__)

c.BARCODE_PREFIX_CHAR = config['barcode_prefix_char']

mount_site_sections(config['module_root'])
static_overrides(join(config['module_root'], 'static'))
template_overrides(join(config['module_root'], 'templates'))


class BarcodeReportMixin:
    """Mixin class with an implementation of write_row that includes barcodes."""
    def write_row(self, row, out):
        if self._include_badge_nums:
            # add in the barcodes here
            badge_num = row[0]
            barcode = generate_barcode_from_badge_num(badge_num)
            row.append(barcode)

        out.writerow(row)


class BarcodePrintedBadgeReport(BarcodeReportMixin, uber.reports.PrintedBadgeReport):
    pass


class BarcodePersonalizedBadgeReport(BarcodeReportMixin, uber.reports.PersonalizedBadgeReport):
    pass


uber.reports.PrintedBadgeReport = BarcodePrintedBadgeReport
uber.reports.PersonalizedBadgeReport = BarcodePersonalizedBadgeReport
