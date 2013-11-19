# -*- coding: utf-8 -*-

"""
"""

import datetime

import pprint
pp = pprint.pprint

import pdb

import objc

import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL
NSMutableDictionary = Foundation.NSMutableDictionary
NSUserDefaults = Foundation.NSUserDefaults
NSBundle = Foundation.NSBundle


import AppKit
NSApplication = AppKit.NSApplication
NSWindowController = AppKit.NSWindowController


import CactusOutlineDoc



def daterange(start, stop, step_days=1):
    # John Machin 
    # http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
    current = start
    step = datetime.timedelta(step_days)
    if step_days > 0:
        #forward
        while current <= stop:
            yield current
            current += step
    elif step_days < 0:
        # backward
        while current >= stop:
            yield current
            current += step
    else:
        raise ValueError("daterange() step_days argument must not be zero")

def timerange( starttime, stoptime, increment):
    # generate the hourly entries per day
    # attn 22:00-02:00 becomes 2 ranges:
    # 00:00-02:00 and 22:00-00:00
    # pdb.set_trace()
    current = starttime
    delta = datetime.timedelta(minutes=increment)
    if stoptime < starttime:
        pass
    else:
        yield current
        while current < stoptime:
            current += delta
            # print "CURRENT:", current
            yield current

#
# Calendar Creator Interface
#
class MakeCalendarController(NSWindowController):
    """Present a dialog for entering a URL for http document retrieval."""

    dateFrom = objc.IBOutlet()
    dateUntil = objc.IBOutlet()
    includeDays = objc.IBOutlet()
    includeHours = objc.IBOutlet()
    includeHoursFrom = objc.IBOutlet()
    includeHoursIntervall = objc.IBOutlet()
    includeHoursUntil = objc.IBOutlet()
    separateMonth = objc.IBOutlet()
    separateWeek = objc.IBOutlet()
    separateYear = objc.IBOutlet()
    weekMonday = objc.IBOutlet()
    weekNumber = objc.IBOutlet()
    calDayFormat = objc.IBOutlet()
    calHourFormat = objc.IBOutlet()
    calMonthFormat = objc.IBOutlet()
    calTitle = objc.IBOutlet()
    calWeekFormat = objc.IBOutlet()
    calYearFormat = objc.IBOutlet()

    def __new__(cls):
        return cls.alloc()

    def init(self):
        # pdb.set_trace()
        self = self.initWithWindowNibName_("CalendarCreator")
        window = self.window()
        window.setDelegate_( self )
        window.setTitle_( u"Define Calendar Spec" )
        
        window.makeFirstResponder_(self.dateFrom)

        self.showWindow_(self)
        self.retain()
        return self

    @objc.IBAction
    def makeItSo_(self, sender):

        def getInt(n):
            s = 0
            try:
                s = int(n)
            except ValueError:
                return 0
            return s

        def calInsert( cal, date):
            y = date.year
            m = date.month
            d = date.day
            
            cur = cal
            if not y in cur:
                cur[y] = {'dt':date,
                          'months':{}}
            cur = cur[y]['months']

            if not m in cur:
                cur[m] = {'dt':date,
                          'days': {}}
            cur = cur[m]['days']
            
            if not d in cur:
                cur[d] = {'dt': date,
                          'day': set()}
            cur = cur[d]['day']
            
            if isinstance(date, datetime.datetime):
                #h = str(date.hour).zfill(2)
                #m = str(date.minute).zfill(2)
                #s = u"%s:%s" % (h,m)
                #if not date in cur:
                #    cur[s] = date
                cur.add( date )

        dateFrom = datetime.datetime.strptime(
                        str(self.dateFrom.dateValue())[:10],
                        "%Y-%m-%d")
        yearStart = dateFrom.year
        monthStart = dateFrom.month

        dateUntil = datetime.datetime.strptime(
                        str(self.dateUntil.dateValue())[:10],
                        "%Y-%m-%d")
        yearEnd = dateUntil.year
        monthEnd = dateUntil.month

        includeDays = bool(int(self.includeDays.state()))
        includeHours = bool(int(self.includeHours.state()))
        includeHoursFrom = getInt(str(self.includeHoursFrom.stringValue()))
        includeHoursIntervall = getInt(str(self.includeHoursIntervall.stringValue()))
        includeHoursUntil = getInt(str(self.includeHoursUntil.stringValue()))

        params = {
            "separateMonth": bool(int(self.separateMonth.state())),
            "separateWeek": bool(int(self.separateWeek.state())),
            "separateYear": bool(int(self.separateYear.state())),
            "weekMonday": bool(int(self.weekMonday.state())),
            "weekNumber": bool(int(self.weekNumber.state())),

            "includeDays": bool(int(self.includeDays.state())),
            "calDayFormat": self.calDayFormat.stringValue(),
            "calHourFormat": self.calHourFormat.stringValue(),
            "calMonthFormat": self.calMonthFormat.stringValue(),
            "calTitle": self.calTitle.stringValue(),
            "calWeekFormat": self.calWeekFormat.stringValue(),
            "calYearFormat": self.calYearFormat.stringValue(),
            "includeHours": bool(int(self.includeHours.state()))
            }

        days = daterange(dateFrom, dateUntil, step_days=1)
        result = []
        
        cal = {}
        
        for day in days:
            dayStart = day.replace(hour=includeHoursFrom)
            dayEnd = day.replace(hour=includeHoursUntil)
            
            if includeHours:
                dayItems = timerange( dayStart, dayEnd, includeHoursIntervall)
                for dayItem in dayItems:
                    #result.append( dayItem )
                    calInsert( cal, dayItem)
            else:
                # result.append( day.date() )
                # pp( cal )
                calInsert( cal, day.date())

        app = NSApplication.sharedApplication()
        delg = app.delegate()
        # delg.makeCalendarCurrentOrNewDoc_( cal )
        self.close()
        delg.makeCalendarCurrentOrNewDoc_( (cal, params) )

    def windowWillClose_(self, notification):
        self.autorelease()

    @objc.IBAction
    def Cancel_(self, sender):
        #pdb.set_trace()
        self.close()

