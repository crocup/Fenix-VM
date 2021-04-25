from abc import ABC, abstractmethod
from fpdf import FPDF
from app import app, time
import os, time


class AbstractReport(ABC):

    def template_method(self, data):
        """
        pass
        :return:
        """
        self.create_report(data)

    @abstractmethod
    def create_report(self, data):
        pass


class PDF_Report(AbstractReport):

    def create_report(self, data):
        """

        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{data}", ln=1, align="C")
        pdf.output(f"{app.config['REPORT_FILE']}/{data}.pdf")


class HTML_Report(AbstractReport):

    def create_report(self, data):
        pass


def result_report(abstract_report: AbstractReport, data):
    """

    :param abstract_report:
    :param data:
    :return:
    """
    return abstract_report.template_method(data)


def del_report(data):
    """

    """
    os.remove(f"{app.config['REPORT_FILE']}/{data}")


def list_report():
    """

    """
    data = {}
    dir_list = os.listdir(app.config['REPORT_FILE'])
    for i in dir_list:
        report = {
            "time": time.ctime(os.path.getmtime(app.config['REPORT_FILE'] + '/' + i))
        }
        data[i] = report
    return data
