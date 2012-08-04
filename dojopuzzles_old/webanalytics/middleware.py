#!-*- coding: utf-8 -*-
from django.conf import settings

class WebAnalyticsMiddleware(object):

    def __init__(self):
        try:
            webanalytics_app = settings.WEBANALYTICS_APP

            if webanalytics_app == 'PIWIK':
                self.process_response = self.insert_piwik
            elif webanalytics_app == 'GOOGLE_ANALYTICS':
                self.process_response = self.insert_google_analytics
            else:
                self.process_response = self.return_unaltered

        except AttributeError:
            self.process_response = self.return_unaltered

    def return_unaltered(self, request, response):
        return response

    def insert_piwik(self, request, response):
        from piwik import WEBANALYTICS_HTML_CODE
        code = WEBANALYTICS_HTML_CODE.format(settings.PIWIK_HOST,
                                             settings.PIWIK_SITE_ID)
        content = response.content
        index = content.upper().find('</BODY>')
        if index == -1:
            return response
        response.content = content[:index] + code + content[index:]
        return response

    def insert_google_analytics(self, request, response):
        from google_analytics import WEBANALYTICS_HTML_CODE
        code = WEBANALYTICS_HTML_CODE.format(settings.GOOGLE_ANALYTICS_ID)
        content = response.content
        index = content.upper().find('</HEAD>')
        if index == -1: 
            return response
        response.content = content[:index] + code + content[index:]
        return response
