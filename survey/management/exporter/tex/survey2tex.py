# -*- coding: utf-8 -*-

import logging
import os

from django.conf import settings
from django.template.defaultfilters import slugify

from survey.management.exporter.survey2x import Survey2X
from survey.management.exporter.tex.question2tex import Question2Tex
from survey.management.exporter.tex.survey_report_latex_file import (
    SurveyReportLatexFile
)

LOGGER = logging.getLogger(__name__)


class Survey2Tex(Survey2X):

    ANALYSIS_FUNCTION = []

    def _synthesis(self, survey):
        """ Return a String of a synthesis of the report. """
        pass

    def _additional_analysis(self, survey, latex_file):
        """ Perform additional analysis. """
        for function_ in self.ANALYSIS_FUNCTION:
            LOGGER.info("Performing additional analysis with %s", function_)
            latex_file.text += function_(survey)

    def treat_question(self, question, survey):
        LOGGER.info("Treating, %s %s", question.pk, question.text)
        chart = Question2Tex().chart(question)
        section_title = question.text.replace("&", "\&")
        return u"""
\\clearpage{}
\\subsection{%s}

\label{sec:%s}

%s

""" % (section_title, question.pk, chart)

    def generate(self, path, output=None):
        """ Generate the pdf. """
        dir_name, file_name = os.path.split(path)
        os.chdir(dir_name)
        print dir_name
        os.system("pwd")
        print "pdflatex {}".format(file_name)
        #os.system("pdflatex {}".format(file_name))
        os.system("pdflatex {}".format(file_name))
        if output is not None:
            os.system("mv {}.pdf {}".format(file_name[:-3], output))
        os.chdir(settings.ROOT)

    def survey_to_x(self):
        ltxf = SurveyReportLatexFile()
        self._synthesis(self.survey)
        for question in self.survey.questions.all():
            ltxf.text += self.treat_question(question, self.survey)
        self._additional_analysis(self.survey, ltxf)
        return ltxf.document

    def generate_file(self):
        super(Survey2Tex, self).generate_file()
        self.generate(self.file_name())