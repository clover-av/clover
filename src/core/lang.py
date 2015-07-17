import gettext
import locale

current_locale, encoding = locale.getdefaultlocale()
locale_path = 'locale\\'
language = gettext.translation('general', locale_path, [current_locale])
language.install()
_ = language.gettext