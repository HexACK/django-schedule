from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import dateutil

freqs = (   ("YEARLY", _("Yearly")),
            ("MONTHLY", _("Monthly")),
            ("WEEKLY", _("Weekly")),
            ("DAILY", _("Daily")),
            ("HOURLY", _("Hourly")),
            ("MINUTELY", _("Minutely")),
            ("SECONDLY", _("Secondly")))

rule_fields = ('until', 'count', 'interval', 'byminute', 'byhour',
    'byday', 'byweekday', 'bymonthday', 'byyearday', 'byweekno',
    'byweekno', 'bymonth', 'bysetpos', 'wkst')

class Rule(models.Model):
    """
    This defines a rule by which an event will recur.  This is defined by the
    rrule in the dateutil documentation.

    * name - the human friendly name of this kind of recursion.
    * description - a short description describing this type of recursion.
    * frequency - the base recurrence period
    * param - extra params required to define this type of recursion. The params
      should follow this format:

        param = [rruleparam:value;]*
        rruleparam = see list below
        value = int[,int]*

      The options are: (documentation for these can be found at
      http://labix.org/python-dateutil#head-470fa22b2db72000d7abe698a5783a46b0731b57)
        ** count
        ** bysetpos
        ** bymonth
        ** bymonthday
        ** byyearday
        ** byweekno
        ** byweekday
        ** byhour
        ** byminute
        ** bysecond
        ** byeaster
    """
    name = models.CharField(_("name"), max_length=32)
    description = models.TextField(_("description"))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10)
    params = models.TextField(_("params"), null=True, blank=True)

    class Meta:
        verbose_name = _('rule')
        verbose_name_plural = _('rules')
        app_label = 'schedule'

    def get_params(self):
        """
        >>> rule = Rule(params = "count:1;bysecond:1;byminute:1,2,4,5")
        >>> rule.get_params()
        {'count': 1, 'byminute': [1, 2, 4, 5], 'bysecond': 1}
        """
        if self.params is None:
            return {}
        params = self.params.split(';')
        param_dict = []
        for param in params:
            param = param.split(':')
            if len(param) == 2:
                # don't store unmanaged params
                if param[0].lower() not in rule_fields:
                    continue

                if param[0].lower() == 'until':
                    # TODO validdate rfc8601 format with a regex YYYYMMDDTHHMMSS(Z)
                    param = (str(param[0]).lower(), dateutil.parser.parse(param[1])) #, ignoretz=True))
                elif param[0].lower() in ('byday', 'byweekday'):
                    param = ('byweekday', [getattr(dateutil.rrule, p) for p in param[1].split(',')])
                else:
                    param = (str(param[0]).lower(), [int(p) for p in param[1].split(',')])

                param_dict.append(param)
        return dict(param_dict)

    def __unicode__(self):
        """Human readable string for Rule"""
        return self.name
