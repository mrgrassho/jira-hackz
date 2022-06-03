#! /usr/bin/env python3
import argparse
from calendar import FRIDAY, SATURDAY, SUNDAY, THURSDAY, TUESDAY, WEDNESDAY
from copy import copy
from datetime import datetime
import enum
from dateutil import rrule
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
JIRA_USER = os.environ.get('JIRA_USER')
JIRA_API_KEY = os.environ.get('JIRA_API_KEY')
JIRA_URL = os.environ.get('JIRA_URL', "https://prometeo.atlassian.net")
MAJOR_RELEASE_DESC = os.environ.get('MAJOR_RELEASE_DESC', "Release y Bugs")
MINOR_RELEASE_DESC = os.environ.get('MINOR_RELEASE_DESC', "Bugs")


class Choice(enum.Enum):
    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return Choice[s]
        except KeyError:
            raise ValueError()


class Frequency(Choice):
    WEEKLY = {'freq': rrule.DAILY, 'interval': 7}
    EVERY_TWO_WEEKS = {'freq': rrule.DAILY, 'interval': 14}
    MONTHLY = {'freq': rrule.DAILY, 'interval': 30}


class WeekDay(Choice):
    MONDAY = rrule.MO
    TUESDAY = rrule.TU
    WEDNESDAY = rrule.WE
    THURSDAY = rrule.TH
    FRIDAY = rrule.FR
    SATURDAY = rrule.SA
    SUNDAY = rrule.SU


class VersionNumber:
    def __init__(self, feature, mayor, minor):
        self.feature = int(feature)
        self.mayor = int(mayor)
        self.minor = int(minor)

    def add_mayor(self):
        self.mayor += 1

    def __str__(self):
        return f"{self.feature}.{self.mayor}.{self.minor}"


class FixVersionCreator():
    def __init__(self, jira_project, start_date, end_date, version_number, frequency, major_weekday, minor_weekday):
        self.jira_project = jira_project
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.version_number = VersionNumber(*version_number.split("."))
        self.feature_releases = list(rrule.rrule(
            freq=frequency['freq'],
            interval=frequency['interval'],
            byweekday=[major_weekday],
            dtstart=self.start_date - timedelta(days=frequency['interval']), until=self.end_date
        ))
        self.bug_releases = rrule.rrule(
            freq=frequency['freq'],
            byweekday=[minor_weekday],
            dtstart=self.start_date,
            until=self.end_date
        )

    def _new_version(self, version_number, start_date, release_date, description):
        body = {
            "description": description,
            "name": f"{str(version_number)} - {release_date.strftime('%d%m%Y')}",
            "archived": False,
            "released": False,
            "startDate": start_date.strftime('%Y-%m-%d'),
            "releaseDate": release_date.strftime('%Y-%m-%d'),
            "project": self.jira_project,
        }
        if DEBUG:
            print(body)
        else:
            response = requests.post(f"{JIRA_URL}/rest/api/2/version", auth=(JIRA_USER, JIRA_API_KEY), json=body)
            print(response.json())

    def _gen_feature_releases(self):
        desc = MAJOR_RELEASE_DESC
        v_number = copy(self.version_number)
        for i in range(len(self.feature_releases)-1):
            start_date = self.feature_releases[i]
            release_date = self.feature_releases[i+1]
            v_number.minor = 0
            self._new_version(v_number,start_date, release_date, desc)
            v_number.add_mayor()

    def _gen_bug_releases(self):
        desc = MINOR_RELEASE_DESC
        v_number = copy(self.version_number)
        for release in self.bug_releases:
            v_number.minor = 1
            self._new_version(v_number,release, release, desc)
            v_number.add_mayor()

    def action(self):
        self._gen_feature_releases()
        self._gen_bug_releases()


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('jira_project', type=str, help="Specify Jira project name")
    parser.add_argument('start_date', type=str, help="Specify fix version start date. Format YYYYMMDD")
    parser.add_argument('end_date', type=str, help="Specify fix version end date. Format YYYYMMDD")
    parser.add_argument('version', type=str, help="Specify fix version number. Following this format: 'Feature.Mayor.Minor'. Example: 1.1.0")
    parser.add_argument('-f', '--freq', type=Frequency.from_string, choices=list(Frequency), help="Specify the frequency of release.", default=Frequency.WEEKLY)
    parser.add_argument('-ma', '--major', type=WeekDay.from_string, choices=list(WeekDay), help="Specify the weekday of major release.", default=WeekDay.MONDAY)
    parser.add_argument('-mi', '--minor', type=WeekDay.from_string, choices=list(WeekDay), help="Specify the weekday of minor release.", default=WeekDay.THURSDAY)
    args = parser.parse_args()
    c = FixVersionCreator(
        args.jira_project,
        args.start_date,
        args.end_date,
        args.version,
        args.freq.value,
        args.major.value,
        args.minor.value,
    )
    c.action()

if __name__ == '__main__':
    main()