# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2015 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------

from canopsis.common.utils import ensure_iterable, ensure_unicode
from canopsis.common.utils import singleton_per_scope
from canopsis.common.template import Template
from canopsis.scheduledjobs.decorator import task_handler
from canopsis.organisation.rights import Rights
from canopsis.task.core import register_task

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate

import mimetypes
import smtplib

from sys import version as PYVER

if PYVER >= '3':
    from html.parser import HTMLParser

else:
    from HTMLParser import HTMLParser


@register_task
def sendmail(
    sender,
    recipients,
    subject,
    body,
    attachments=None,
    smtp_host='localhost',
    smtp_port=25,
    html=False
):
    recipients = ', '.join(ensure_iterable(recipients))

    if not html:
        h = HTMLParser()
        body = h.unescape(body)
        subject = h.unescape(subject)

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipients
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    msg.attach(MIMEText(body, 'html' if html else 'plain'))

    if attachments is None:
        attachments = []

    attachments = ensure_iterable(attachments)

    for attachment in attachments:
        attached_file = MIMEBase('application', 'octet-stream')
        attached_file.set_payload(attachment.read())
        attached_file.add_header(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(attachment.name)
        )

        mimetype, _ = mimetypes.guess_type(attachment.name)
        attached_file.add_header('Content-Type', mimetype)

        Encoders.encode_base64(attached_file)

        msg.attach(attached_file)

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()


@task_handler
def job_processing(engine, job, rightsmgr=None, logger=None, **kwargs):
    if rightsmgr is None:
        rightsmgr = singleton_per_scope(Rights)

    # build sender
    username = job.get('user', 'root')
    user = rightsmgr.get_user(username)

    if user is None:
        raise Exception('Impossible to find user: {0}'.format(username))

    sender = '"{0}"" <{1}>'.format(
        user['contact'].get('name', username),
        user['mail']
    )

    # verify recipients
    recipients = job.get('recipients', None)

    if not recipients:
        raise Exception('No recipients configured')

    # build subject and body
    subject_tmpl = ensure_unicode(job.get('subject', ''))
    body_tmpl = ensure_unicode(job.get('body', ''))
    tmpldata = job.get('jobctx', {})

    subject = Template(subject_tmpl)(tmpldata)
    body = Template(body_tmpl)(tmpldata)

    # build sendmail params
    params = {}

    if 'smtp_host' in job:
        params['smtp_host'] = job['smtp_host']

    if 'smtp_port' in job:
        params['smtp_port'] = job['smtp_port']

    if 'html' in job:
        params['html'] = job['html']

    if 'attachments' in job:
        storage = engine['file_storage']
        params['attachments'] = storage.find(names=job['attachments'])

    # send mail
    sendmail(
        sender,
        recipients,
        subject,
        body,
        **params
    )
