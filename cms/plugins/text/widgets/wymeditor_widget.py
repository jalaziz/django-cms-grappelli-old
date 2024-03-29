from os.path import join
from django.conf import settings
from django.forms import Textarea
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from cms.plugins.text import settings as text_settings
from django.utils.translation.trans_real import get_language


class WYMEditor(Textarea):
    class Media:
        js = [join(settings.CMS_MEDIA_URL, path) for path in (
            'wymeditor/jquery.wymeditor.js',
            'wymeditor/plugins/resizable/jquery.wymeditor.resizable.js',
            'js/wymeditor.placeholdereditor.js',
            'js/lib/jquery-ui.custom.min.js',
            'js/placeholder_editor_registry.js',
        )]
        css = {
            'all': [join(settings.CMS_MEDIA_URL, path) for path in (
                        'css/jquery/cupertino/jquery-ui.css',
                    )],
        }

    def __init__(self, attrs=None, installed_plugins=None):
        """
        Create a widget for editing text + plugins.

        installed_plugins is a list of plugins to display that are text_enabled
        """
        self.attrs = {'class': 'wymeditor'}
        if attrs:
            self.attrs.update(attrs)
        super(WYMEditor, self).__init__(attrs)
        self.installed_plugins = installed_plugins

    def render_textarea(self, name, value, attrs=None):
        return super(WYMEditor, self).render(name, value, attrs)

    def render_additions(self, name, value, attrs=None):
        language = get_language()
        context = {
            'name': name,
            'language': language,
            'CMS_MEDIA_URL': settings.CMS_MEDIA_URL,
            'WYM_TOOLS': mark_safe(text_settings.WYM_TOOLS),
            'WYM_CONTAINERS': mark_safe(text_settings.WYM_CONTAINERS),
            'WYM_CLASSES': mark_safe(text_settings.WYM_CLASSES),
            'WYM_STYLES': mark_safe(text_settings.WYM_STYLES),
            'WYM_STYLESHEET': mark_safe(text_settings.WYM_STYLESHEET),
            'installed_plugins': self.installed_plugins,
        }
        return mark_safe(render_to_string(
            'cms/plugins/widgets/wymeditor.html', context))

    def render(self, name, value, attrs=None):
        return self.render_textarea(name, value, attrs) + \
            self.render_additions(name, value, attrs)
