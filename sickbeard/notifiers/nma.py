import sickbeard

from sickbeard import logger, common
from pynma import pynma


class NMA_Notifier:
    def test_notify(self, nma_api, nma_priority):
        return self._sendNMA(nma_api, nma_priority, event="Test", message="Testing NMA settings from SickRage",
                             force=True)

    def notify_snatch(self, ep_name):
        if sickbeard.NMA_NOTIFY_ONSNATCH:
            self._sendNMA(nma_api=None, nma_priority=None, event=common.notifyStrings[common.NOTIFY_SNATCH],
                          message=ep_name)

    def notify_download(self, ep_name):
        if sickbeard.NMA_NOTIFY_ONDOWNLOAD:
            self._sendNMA(nma_api=None, nma_priority=None, event=common.notifyStrings[common.NOTIFY_DOWNLOAD],
                          message=ep_name)

    def notify_subtitle_download(self, ep_name, lang):
        if sickbeard.NMA_NOTIFY_ONSUBTITLEDOWNLOAD:
            self._sendNMA(nma_api=None, nma_priority=None, event=common.notifyStrings[common.NOTIFY_SUBTITLE_DOWNLOAD],
                          message=ep_name + ": " + lang)

    def notify_git_update(self, new_version = "??"):
        if sickbeard.USE_NMA:
            update_text=common.notifyStrings[common.NOTIFY_GIT_UPDATE_TEXT]
            title=common.notifyStrings[common.NOTIFY_GIT_UPDATE]
            self._sendNMA(nma_api=None, nma_priority=None, event=title, message=update_text + new_version)

    def _sendNMA(self, nma_api=None, nma_priority=None, event=None, message=None, force=False):

        title = 'SickRage'

        if not sickbeard.USE_NMA and not force:
            return False

        if nma_api == None:
            nma_api = sickbeard.NMA_API

        if nma_priority == None:
            nma_priority = sickbeard.NMA_PRIORITY

        batch = False

        p = pynma.PyNMA()
        keys = nma_api.split(',')
        p.addkey(keys)

        if len(keys) > 1: batch = True

        logger.log("NMA: Sending notice with details: event=\"%s\", message=\"%s\", priority=%s, batch=%s" % (event, message, nma_priority, batch), logger.DEBUG)
        response = p.push(application=title, event=event, description=message, priority=nma_priority, batch_mode=batch)

        if not response[nma_api][u'code'] == u'200':
            logger.log(u'Could not send notification to NotifyMyAndroid', logger.ERROR)
            return False
        else:
            logger.log(u"NMA: Notification sent to NotifyMyAndroid", logger.INFO)
            return True


notifier = NMA_Notifier
