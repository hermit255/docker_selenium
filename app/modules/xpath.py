"""nodes"""
LINK_TEXT = 'a[text()]' # テキストを持つa
LINK_IMAGE = 'a[/img]' # 画像リンクのa
TEXT_INPUT = 'input[@type="text"]'
PASSWORD_INPUT = 'input[@type="password"]'
INPUT_RADIOS = 'input[@type="radio"]'
INPUT_CHECKBOXES = 'input[@type="checkbox"]'
SELECT = 'select'
SELECT_OPTION = '%s/option' # ある条件を満たすセレクト配下のオプション

"""options"""
WITH_LABEL = '[@id=ancestor::html//%s/attribute::for]' # input用オプション forでリンクしたlabel(%s labelノード)
WITH_INPUT = '[@for=ancestor::html//%s/attribute::id]' # label用オプション forでリンクしたinputを持つ(%s inputノード)
WRAPPED_BY_LABEL = '[ancestor::%s]' # input用オプション labelに囲まれた(%s labelノード)
WRAPS_INPUT = '[descendant::%s]' # label用オプション inputを囲む(%s inputノード)

WITH_TEXT = '[text()="%s"]' # ノード自身があるテキストを持つ(%s)
WITH_CHILD_TEXT = '[child::*/text()]' # 子要素が任意のテキストを持つ